#!/usr/bin/env python3
"""
Dental_012 Periapical Lesion Retraining on RTX 5080 (Negative Sample Augmented Dataset)
"""
import os
import sys
from pathlib import Path
import torch
from ultralytics import YOLO

repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
from config.paths import RUNS_ROOT, resolve_module_dir

def main():
    print(f"=== Starting Dental_012 Periapical Retraining (Augmented 4,264 Images) ===")
    device = "0" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")
    
    data_yaml = str(resolve_module_dir("Dental_012") / "data" / "yolo_dataset_augmented" / "data.yaml")
    project_dir = str(RUNS_ROOT)
    run_name = "periapical_augmented_v1"

    # YOLO11s as backbone
    model = YOLO("yolo11s.pt")

    results = model.train(
        data=data_yaml,
        epochs=50,
        batch=16,
        imgsz=1024,
        device=device,
        project=project_dir,
        name=run_name,
        patience=10,
        save=True,
        save_period=5,
        workers=4,
        verbose=True,
        weight_decay=0.0005,
        mosaic=0.5,
        mixup=0.1,
        degrees=5.0,
        fliplr=0.5,
    )

    print("=== Training Complete ===")
    best_pt = os.path.join(project_dir, run_name, "weights", "best.pt")
    print(f"Best weight saved at: {best_pt}")

    # Export to ONNX
    if os.path.exists(best_pt):
        print("Exporting best weight to ONNX...")
        best_model = YOLO(best_pt)
        best_model.export(format="onnx", imgsz=1024)
        print("ONNX export complete.")

if __name__ == "__main__":
    main()