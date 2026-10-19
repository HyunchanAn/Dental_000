"""Centralized path configuration for Dental_000 scripts and evaluation pipelines."""
from pathlib import Path
import os

REPO_ROOT: Path = Path(os.environ.get("DENTAL_000_ROOT", Path(__file__).resolve().parents[1]))
DENTAL_ROOT: Path = Path(os.environ.get("DENTAL_ROOT", REPO_ROOT.parent))
MODULES_ROOT: Path = Path(os.environ.get("DENTAL_MODULES_ROOT", REPO_ROOT / "modules"))
DATA_ROOT: Path = Path(os.environ.get("DATA_ROOT", REPO_ROOT / "data"))
WEIGHTS_ROOT: Path = Path(os.environ.get("WEIGHTS_ROOT", REPO_ROOT / "weights"))
RUNS_ROOT: Path = Path(os.environ.get("RUNS_ROOT", REPO_ROOT / "runs"))


def resolve_module_dir(module_name: str) -> Path:
    """Resolve a module directory from internal submodules first, then sibling workspace."""
    sub_dir = MODULES_ROOT / module_name
    if sub_dir.is_dir():
        return sub_dir
    sib_dir = DENTAL_ROOT / module_name
    return sib_dir
