#!/usr/bin/env python3
"""
Dental_002 2-Stage High-Resolution Tooth Patch Dataset Generator
Integrates Dental_008 tooth bounding boxes and Ground Truth caries lesions (DENTEX).
Performs exact coordinate transformation into patch-relative YOLO format (cls cx cy bw bh),
applies CLAHE preprocessing, and incorporates normal teeth as negative background samples.
"""

import os
import sys
import glob
import json
import argparse
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add Dental_008 to sys.path for DENTEXDataset
core_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dental_008_src = os.path.abspath(os.path.join(core_root, "..", "Dental_008", "src"))
if dental_008_src not in sys.path:
    sys.path.append(dental_008_src)

try:
    from dentex_seg.dataset import DENTEXDataset
except ImportError:
    DENTEXDataset = None


def apply_clahe(img_bgr: np.ndarray) -> np.ndarray:
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)
    to improve tooth-interproximal boundary contrast.
    """
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


def compute_relative_caries_bbox(
    tooth_patch_box: Tuple[float, float, float, float],
    caries_box: Tuple[float, float, float, float],
) -> Tuple[float, float, float, float]:
    """
    Transform global coordinates to patch-relative normalized coordinates [0.0, 1.0].
    
    tooth_patch_box: [patch_x1, patch_y1, patch_x2, patch_y2]
    caries_box: [caries_x1, caries_y1, caries_x2, caries_y2]
    
    Returns:
        (cx_rel, cy_rel, bw_rel, bh_rel)
    """
    px1, py1, px2, py2 = tooth_patch_box
    pw = px2 - px1
    ph = py2 - py1

    cx1, cy1, cx2, cy2 = caries_box
    
    # Clip caries box to patch boundary
    cx1_clipped = max(px1, cx1)
    cy1_clipped = max(py1, cy1)
    cx2_clipped = min(px2, cx2)
    cy2_clipped = min(py2, cy2)

    caries_w = max(0.0, cx2_clipped - cx1_clipped)
    caries_h = max(0.0, cy2_clipped - cy1_clipped)
    caries_cx = (cx1_clipped + cx2_clipped) / 2.0
    caries_cy = (cy1_clipped + cy2_clipped) / 2.0

    cx_rel = (caries_cx - px1) / pw
    cy_rel = (caries_cy - py1) / ph
    bw_rel = caries_w / pw
    bh_rel = caries_h / ph

    # Clamp to [0.0, 1.0]
    cx_rel = max(0.0, min(1.0, cx_rel))
    cy_rel = max(0.0, min(1.0, cy_rel))
    bw_rel = max(0.0, min(1.0, bw_rel))
    bh_rel = max(0.0, min(1.0, bh_rel))

    return cx_rel, cy_rel, bw_rel, bh_rel


def generate_patch_dataset(
    split: str = "val",
    output_dir: str = r"D:\Github\Dental_000\data\caries_patches\val",
    margin_ratio: float = 0.15,
    include_negative_ratio: float = 1.0,
    max_samples: int = None,
) -> Dict[str, Any]:
    """
    Main execution pipeline for 2-Stage patch dataset generation.
    Reads DENTEX ground truth (tooth bboxes + disease annotations),
    crops CLAHE-enhanced tooth patches, and saves relative YOLO labels.
    """
    if DENTEXDataset is None:
        raise RuntimeError("DENTEXDataset could not be loaded from Dental_008/src")

    print(f"=== Generating 2-Stage High-Resolution Caries Patch Dataset ({split}) ===")
    print(f"Output Directory: {output_dir}")
    print(f"Tooth Margin Ratio: {margin_ratio * 100}%")

    images_out = os.path.join(output_dir, "images")
    labels_out = os.path.join(output_dir, "labels")
    os.makedirs(images_out, exist_ok=True)
    os.makedirs(labels_out, exist_ok=True)

    dataset = DENTEXDataset(split=split)
    img_ids = dataset.img_ids
    if max_samples:
        img_ids = img_ids[:max_samples]

    total_caries_patches = 0
    total_negative_patches = 0
    generated_samples = []

    for img_id in img_ids:
        img_info = dataset.images.get(img_id)
        if not img_info:
            continue
        file_name = img_info["file_name"]
        img_path = os.path.join(dataset.img_dir, file_name)
        if not os.path.exists(img_path):
            continue

        raw_img = cv2.imread(img_path)
        if raw_img is None:
            continue

        h_img, w_img = raw_img.shape[:2]
        clahe_img = apply_clahe(raw_img)

        # Get all tooth annotations for this image
        anns = dataset.img_to_anns.get(img_id, [])
        if not anns:
            continue

        base_stem = os.path.splitext(os.path.basename(file_name))[0]

        for tooth_idx, ann in enumerate(anns):
            bbox = ann.get("bbox")  # [x_min, y_min, w, h]
            cat3 = ann.get("category_id_3")  # 0: Impacted, 1: Caries, 2: Periapical, 3: Deep Caries

            if not bbox or len(bbox) < 4:
                continue

            bx, by, bw, bh = bbox
            if bw <= 0 or bh <= 0:
                continue

            # Tooth patch coordinates with margin
            margin_x = bw * margin_ratio
            margin_y = bh * margin_ratio
            px1 = max(0, int(bx - margin_x))
            py1 = max(0, int(by - margin_y))
            px2 = min(w_img, int(bx + bw + margin_x))
            py2 = min(h_img, int(by + bh + margin_y))

            pw = px2 - px1
            ph = py2 - py1
            if pw <= 5 or ph <= 5:
                continue

            patch_img = clahe_img[py1:py2, px1:px2]
            if patch_img.size == 0:
                continue

            is_caries = cat3 in [1, 3]  # Caries or Deep Caries
            patch_name = f"{base_stem}_tooth_{tooth_idx}_{'caries' if is_caries else 'normal'}.png"
            label_name = f"{base_stem}_tooth_{tooth_idx}_{'caries' if is_caries else 'normal'}.txt"

            patch_img_path = os.path.join(images_out, patch_name)
            patch_lbl_path = os.path.join(labels_out, label_name)

            if is_caries:
                # Calculate relative bounding box for caries lesion
                tooth_patch_box = (float(px1), float(py1), float(px2), float(py2))
                caries_box = (float(bx), float(by), float(bx + bw), float(by + bh))
                cx_rel, cy_rel, bw_rel, bh_rel = compute_relative_caries_bbox(tooth_patch_box, caries_box)

                # YOLO label: class 0 = Caries
                label_line = f"0 {cx_rel:.6f} {cy_rel:.6f} {bw_rel:.6f} {bh_rel:.6f}\n"
                
                cv2.imwrite(patch_img_path, patch_img)
                with open(patch_lbl_path, "w", encoding="utf-8") as lf:
                    lf.write(label_line)

                total_caries_patches += 1
                generated_samples.append({
                    "patch_image": patch_name,
                    "label_file": label_name,
                    "type": "caries",
                    "rel_box": f"0 {cx_rel:.4f} {cy_rel:.4f} {bw_rel:.4f} {bh_rel:.4f}",
                    "patch_size": f"{pw}x{ph}",
                })

            else:
                # Negative background patch (Empty label file in YOLO format)
                # Controls false positive rate
                if np.random.rand() <= include_negative_ratio:
                    cv2.imwrite(patch_img_path, patch_img)
                    with open(patch_lbl_path, "w", encoding="utf-8") as lf:
                        pass  # Empty file signals no foreground objects (Negative sample)

                    total_negative_patches += 1
                    generated_samples.append({
                        "patch_image": patch_name,
                        "label_file": label_name,
                        "type": "negative_background",
                        "rel_box": "(empty)",
                        "patch_size": f"{pw}x{ph}",
                    })

    summary = {
        "split": split,
        "total_caries_patches": total_caries_patches,
        "total_negative_patches": total_negative_patches,
        "total_generated": total_caries_patches + total_negative_patches,
        "output_dir": output_dir,
        "samples": generated_samples[:10],
    }

    print("\n=== 2-Stage Patch Dataset Generation Complete ===")
    print(f"Caries Patches (Positive): {total_caries_patches}")
    print(f"Normal Patches (Negative Background): {total_negative_patches}")
    print(f"Total Saved Samples: {total_caries_patches + total_negative_patches}")

    return summary


def parse_args():
    parser = argparse.ArgumentParser(description="2-Stage Caries Patch Dataset Generator")
    parser.add_argument("--split", type=str, default="val", choices=["val", "train"])
    parser.add_argument("--output-dir", type=str, default=r"D:\Github\Dental_000\data\caries_patches\val")
    parser.add_argument("--margin", type=float, default=0.15, help="Tooth bbox margin ratio (default: 0.15)")
    parser.add_argument("--neg-ratio", type=float, default=1.0, help="Negative normal tooth inclusion ratio")
    parser.add_argument("--max-samples", type=int, default=None, help="Max images to process for quick verification")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate_patch_dataset(
        split=args.split,
        output_dir=args.output_dir,
        margin_ratio=args.margin,
        include_negative_ratio=args.neg_ratio,
        max_samples=args.max_samples,
    )
