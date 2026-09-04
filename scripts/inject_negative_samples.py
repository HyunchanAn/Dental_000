#!/usr/bin/env python3
"""
Dental_012 Negative Background Sample Augmentation Pipeline
Enriches Dental_012 training/validation dataset with verified normal anatomical structures
(Mental Foramen, Mandibular Canal, Maxillary Sinus floor, Incisive Foramen)
to suppress false positive detections (FP 406 cases -> Precision >= 80%).
"""

import os
import sys
import shutil
import argparse
from glob import glob
from typing import Dict, Any, List

core_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dental_008_src = os.path.abspath(os.path.join(core_root, "..", "Dental_008", "src"))
if dental_008_src not in sys.path:
    sys.path.append(dental_008_src)

try:
    from dentex_seg.dataset import DENTEXDataset
except ImportError:
    DENTEXDataset = None


def inject_negative_samples(
    dataset_dir: str = r"D:\Github\Dental_012\data\yolo_dataset",
    output_dir: str = r"D:\Github\Dental_012\data\yolo_dataset_augmented",
    train_negative_count: int = 300,
    val_negative_count: int = 40,
) -> Dict[str, Any]:
    """
    Copies existing positive periapical samples and injects normal anatomical panoramas
    as empty YOLO label (.txt) files (official YOLO standard for background negative samples).
    """
    print("=== Dental_012 Negative Sample Augmentation Pipeline ===")
    print(f"Source Dataset: {dataset_dir}")
    print(f"Target Augmented Dataset: {output_dir}")

    for split in ["train", "val"]:
        os.makedirs(os.path.join(output_dir, "images", split), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "labels", split), exist_ok=True)

    # 1. Copy existing positive samples
    copied_stats = {"train_pos": 0, "val_pos": 0}
    for split in ["train", "val"]:
        src_img_dir = os.path.join(dataset_dir, "images", split)
        src_lbl_dir = os.path.join(dataset_dir, "labels", split)
        dst_img_dir = os.path.join(output_dir, "images", split)
        dst_lbl_dir = os.path.join(output_dir, "labels", split)

        if not os.path.exists(src_img_dir):
            continue

        lbl_files = glob(os.path.join(src_lbl_dir, "*.txt"))
        for lbl_path in lbl_files:
            base_stem = os.path.splitext(os.path.basename(lbl_path))[0]
            # check image
            img_cand = glob(os.path.join(src_img_dir, base_stem + ".*"))
            if img_cand:
                shutil.copy2(img_cand[0], os.path.join(dst_img_dir, os.path.basename(img_cand[0])))
                shutil.copy2(lbl_path, os.path.join(dst_lbl_dir, os.path.basename(lbl_path)))
                if split == "train":
                    copied_stats["train_pos"] += 1
                else:
                    copied_stats["val_pos"] += 1

    print(f"Copied Positive Samples -> Train: {copied_stats['train_pos']}, Val: {copied_stats['val_pos']}")

    # 2. Inject Normal Panoramas from DENTEX as Negative Background Samples (Empty .txt)
    injected_stats = {"train_neg": 0, "val_neg": 0}
    sample_evidences = []

    # Validation Negatives
    d_val = DENTEXDataset(split="val")
    val_neg_imgs = []
    for img_id in d_val.img_ids:
        anns = d_val.img_to_anns.get(img_id, [])
        if not any(a.get("category_id_3") == 2 for a in anns):  # 2: Periapical Lesion
            val_neg_imgs.append(d_val.images[img_id])

    val_target = min(val_negative_count, len(val_neg_imgs))
    for i in range(val_target):
        info = val_neg_imgs[i]
        src_img = os.path.join(d_val.img_dir, info["file_name"])
        if os.path.exists(src_img):
            dst_name = f"neg_val_normal_{i:04d}.png"
            lbl_name = f"neg_val_normal_{i:04d}.txt"
            dst_img_path = os.path.join(output_dir, "images", "val", dst_name)
            dst_lbl_path = os.path.join(output_dir, "labels", "val", lbl_name)
            
            shutil.copy2(src_img, dst_img_path)
            with open(dst_lbl_path, "w", encoding="utf-8") as f:
                pass  # Empty file = YOLO Negative Sample
            injected_stats["val_neg"] += 1
            if len(sample_evidences) < 3:
                sample_evidences.append({
                    "type": "val_negative",
                    "img": dst_name,
                    "lbl": lbl_name,
                    "size": os.path.getsize(dst_img_path),
                })

    # Train Negatives
    d_train = DENTEXDataset(split="train")
    train_neg_imgs = []
    for img_id in d_train.img_ids:
        anns = d_train.img_to_anns.get(img_id, [])
        if not any(a.get("category_id_3") == 2 for a in anns):
            train_neg_imgs.append(d_train.images[img_id])

    train_target = min(train_negative_count, len(train_neg_imgs))
    for i in range(train_target):
        info = train_neg_imgs[i]
        src_img = os.path.join(d_train.img_dir, info["file_name"])
        if os.path.exists(src_img):
            dst_name = f"neg_train_normal_{i:04d}.png"
            lbl_name = f"neg_train_normal_{i:04d}.txt"
            dst_img_path = os.path.join(output_dir, "images", "train", dst_name)
            dst_lbl_path = os.path.join(output_dir, "labels", "train", lbl_name)

            shutil.copy2(src_img, dst_img_path)
            with open(dst_lbl_path, "w", encoding="utf-8") as f:
                pass  # Empty file = YOLO Negative Sample
            injected_stats["train_neg"] += 1

    print(f"Injected Negative Background Samples -> Train: {injected_stats['train_neg']}, Val: {injected_stats['val_neg']}")

    # 3. Generate data.yaml for retraining
    norm_path = output_dir.replace("\\", "/")
    yaml_content = f"path: {norm_path}\ntrain: images/train\nval: images/val\n\nnames:\n  0: Periapical_Lesion\n"
    yaml_path = os.path.join(output_dir, "data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)

    print(f"Generated Dataset Config: {yaml_path}")

    summary = {
        "dataset_dir": output_dir,
        "train_total": copied_stats["train_pos"] + injected_stats["train_neg"],
        "train_pos": copied_stats["train_pos"],
        "train_neg": injected_stats["train_neg"],
        "val_total": copied_stats["val_pos"] + injected_stats["val_neg"],
        "val_pos": copied_stats["val_pos"],
        "val_neg": injected_stats["val_neg"],
        "yaml_path": yaml_path,
        "sample_evidences": sample_evidences,
    }
    return summary


def parse_args():
    parser = argparse.ArgumentParser(description="Dental_012 Negative Sample Augmentation")
    parser.add_argument("--src-dir", type=str, default=r"D:\Github\Dental_012\data\yolo_dataset")
    parser.add_argument("--out-dir", type=str, default=r"D:\Github\Dental_012\data\yolo_dataset_augmented")
    parser.add_argument("--train-neg", type=int, default=300)
    parser.add_argument("--val-neg", type=int, default=40)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    inject_negative_samples(args.src_dir, args.out_dir, args.train_neg, args.val_neg)
