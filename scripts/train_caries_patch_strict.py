#!/usr/bin/env python3
"""
Dental_002 2-Stage Caries Patch YOLO Retraining with Strict Train/Val Split (Zero Leakage)
"""
import os
import sys
import torch
from ultralytics import YOLO

def main():
    print(f"=== Starting Strict 2-Stage Caries Patch Retraining (Zero Leakage) ===")
    device = "0" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")
    
    data_yaml = r"Y:/Dental_000/data/caries_patches_split/caries_patch_split.yaml"
    project_dir = r"Y:/Dental_000/runs"
    run_name = "caries_patch_strict_v2"

    # Pretrained YOLOv8s as backbone
    model = YOLO("yolov8s.pt")

    results = model.train(
        data=data_yaml,
        epochs=50,
        batch=16,
        imgsz=512,
        device=device,
        project=project_dir,
        name=run_name,
        patience=10,             # Early stopping on overfitting
        save=True,
        save_period=5,
        workers=4,
        verbose=True,
        weight_decay=0.0005,     # L2 Regularization to prevent overfitting
        dropout=0.1,             # Dropout to prevent memorization
        mosaic=0.5,              # Data augmentation
        mixup=0.1,
        degrees=10.0,
        fliplr=0.5,
    )

    print("=== Training Complete ===")
    best_pt = os.path.join(project_dir, run_name, "weights", "best.pt")
    print(f"Best weight saved at: {best_pt}")

    # Export to ONNX
    if os.path.exists(best_pt):
        print("Exporting best weight to ONNX...")
        best_model = YOLO(best_pt)
        best_model.export(format="onnx", imgsz=512)
        print("ONNX export complete.")

if __name__ == "__main__":
    main()