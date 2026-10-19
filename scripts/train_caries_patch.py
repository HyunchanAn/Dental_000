#!/usr/bin/env python3
"""
Dental_002 2-Stage Caries Patch YOLO Retraining on RTX 5080
"""
import os
import sys
from pathlib import Path
import torch
from ultralytics import YOLO

repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
from config.paths import DATA_ROOT, RUNS_ROOT

def main():
    print(f"=== Starting 2-Stage Caries Patch Retraining ===")
    device = "0" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")
    
    data_yaml = str(DATA_ROOT / "caries_patches" / "caries_patch.yaml")
    project_dir = str(RUNS_ROOT)
    run_name = "caries_patch_v1"

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
        patience=15,
        save=True,
        save_period=10,
        workers=4,
        verbose=True,
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