#!/usr/bin/env python3
"""
Strict Patient-Level Train/Val Split for 2-Stage Caries Patch Dataset (8:2)
Zero Data Leakage: Patches from the same panorama NEVER cross train and val.
"""
import os
import shutil
import glob
import random

random.seed(42)  # Fixed seed for reproducibility

src_images = r"Y:\Dental_000\data\caries_patches\val\images"
src_labels = r"Y:\Dental_000\data\caries_patches\val\labels"
base_out = r"Y:\Dental_000\data\caries_patches_split"

# Group patches by panorama base name (e.g., 'val_0', 'val_10')
pano_groups = {}
for img_path in glob.glob(os.path.join(src_images, "*.png")):
    fname = os.path.basename(img_path)
    # format: {pano_id}_tooth_{idx}_{type}.png
    parts = fname.split("_tooth_")
    pano_id = parts[0]
    
    if pano_id not in pano_groups:
        pano_groups[pano_id] = []
    pano_groups[pano_id].append(fname)

all_panos = sorted(list(pano_groups.keys()))
random.shuffle(all_panos)

# 80% train, 20% val by panorama patient ID
split_idx = int(len(all_panos) * 0.8)
train_panos = set(all_panos[:split_idx])
val_panos = set(all_panos[split_idx:])

print(f"Total Panoramas: {len(all_panos)}")
print(f"Train Panoramas: {len(train_panos)} ({len(train_panos)/len(all_panos)*100:.1f}%)")
print(f"Val Panoramas (Unseen): {len(val_panos)} ({len(val_panos)/len(all_panos)*100:.1f}%)")

# Ensure clean directories
for split in ["train", "val"]:
    os.makedirs(os.path.join(base_out, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(base_out, split, "labels"), exist_ok=True)

train_count = 0
val_count = 0

for pano_id, fnames in pano_groups.items():
    target_split = "train" if pano_id in train_panos else "val"
    for fname in fnames:
        stem = os.path.splitext(fname)[0]
        lbl_name = stem + ".txt"
        
        src_img_file = os.path.join(src_images, fname)
        src_lbl_file = os.path.join(src_labels, lbl_name)
        
        dst_img_file = os.path.join(base_out, target_split, "images", fname)
        dst_lbl_file = os.path.join(base_out, target_split, "labels", lbl_name)
        
        shutil.copy2(src_img_file, dst_img_file)
        if os.path.exists(src_lbl_file):
            shutil.copy2(src_lbl_file, dst_lbl_file)
            
        if target_split == "train":
            train_count += 1
        else:
            val_count += 1

print(f"Split Complete!")
print(f"Train Patches: {train_count} images")
print(f"Validation Patches (Pure Unseen Test): {val_count} images")

# Generate strict dataset yaml
yaml_content = f"""path: Y:/Dental_000/data/caries_patches_split
train: train/images
val: val/images
names:
  0: Caries
"""
yaml_path = os.path.join(base_out, "caries_patch_split.yaml")
with open(yaml_path, "w", encoding="utf-8") as yf:
    yf.write(yaml_content)

print(f"Strict YAML created at: {yaml_path}")