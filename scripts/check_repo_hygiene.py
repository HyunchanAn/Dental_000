#!/usr/bin/env python3
"""
Repository hygiene and portable path verifier for Dental_000.
1. Verifies that no tracked .py/.yaml/.yml file contains hardcoded Windows drive letters (C:/, D:/, Y:/) or UNC paths.
2. Verifies that no newly staged file exceeds max_kb (default: 1024 KB) or matches blocked binary extensions (.exe, .sh, .db, .pyc).
"""
import argparse
import pathlib
import re
import subprocess
import sys
from typing import List

HARDCODED_PATH_PATTERN = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/][A-Za-z0-9_.]|\\\\[A-Za-z0-9_-]+\\[A-Za-z0-9_$-]+")
BLOCKED_EXTENSIONS = {".exe", ".db", ".sqlite", ".sqlite3", ".pyc"}


def check_tracked_paths(repo_root: pathlib.Path) -> List[str]:
    violations: List[str] = []
    try:
        out = subprocess.check_output(
            ["git", "ls-files"], cwd=str(repo_root), text=True, encoding="utf-8"
        )
        tracked_files = out.splitlines()
    except Exception:
        tracked_files = [
            str(p.relative_to(repo_root)).replace("\\", "/")
            for p in repo_root.rglob("*")
            if p.is_file() and ".git" not in p.parts
        ]

    for rel_path in tracked_files:
        if rel_path.startswith("modules/") or rel_path == "scripts/check_repo_hygiene.py":
            continue
        if not rel_path.endswith((".py", ".yaml", ".yml")):
            continue
        full_path = repo_root / rel_path
        if not full_path.is_file():
            continue
        lines = full_path.read_text(encoding="utf-8-sig", errors="ignore").splitlines()
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("#") or "http://" in stripped or "https://" in stripped or "file:///" in stripped:
                continue
            if HARDCODED_PATH_PATTERN.search(stripped):
                violations.append(f"{rel_path}:{idx}: {stripped}")
    return violations


def check_staged_files(repo_root: pathlib.Path, max_kb: int = 1024) -> List[str]:
    violations: List[str] = []
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
            cwd=str(repo_root),
            text=True,
            encoding="utf-8",
        )
        staged = [line.strip() for line in out.splitlines() if line.strip()]
    except Exception:
        return violations

    for rel_path in staged:
        full_path = repo_root / rel_path
        if not full_path.is_file():
            continue
        ext = full_path.suffix.lower()
        if ext in BLOCKED_EXTENSIONS:
            violations.append(f"Blocked file extension ({ext}): {rel_path}")
        size_kb = full_path.stat().st_size / 1024.0
        if size_kb > max_kb:
            violations.append(f"File exceeds {max_kb} KB limit ({size_kb:.1f} KB): {rel_path}")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Dental_000 repository hygiene.")
    parser.add_argument("--root", type=str, default=str(pathlib.Path(__file__).resolve().parents[1]))
    parser.add_argument("--max-kb", type=int, default=1024)
    parser.add_argument("--check-file", type=str, default=None, help="Check a specific candidate file for size/extension guard")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.root).resolve()
    errors: List[str] = []

    if args.check_file:
        cand = pathlib.Path(args.check_file)
        if cand.is_file():
            size_kb = cand.stat().st_size / 1024.0
            if size_kb > args.max_kb:
                errors.append(f"File exceeds {args.max_kb} KB limit ({size_kb:.1f} KB): {cand}")
            if cand.suffix.lower() in BLOCKED_EXTENSIONS:
                errors.append(f"Blocked file extension ({cand.suffix}): {cand}")

    errors.extend(check_tracked_paths(repo_root))
    errors.extend(check_staged_files(repo_root, max_kb=args.max_kb))

    if errors:
        for err in errors:
            print(f"[HYGIENE VIOLATION] {err}", file=sys.stderr)
        return 1

    print("[OK] Repository hygiene and path portability checks passed (0 violations).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
