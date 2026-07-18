import os
import torch
import urllib.request
from huggingface_hub import hf_hub_download, HfApi

# Map modules to their original HF backup repos (from setup_env.py) and their architecture types.
# This fixes the two fatal errors: missing .pt files and incorrect YOLO() loading for CNNs.
MODULE_INFO = {
    "Dental_001": {
        "repo": "live-track/dental-yolo", "filename": "yolov8m_custom.pt", "type": "yolo"
    },
    "Dental_002": {
        "repo": "live-track/dental-caries", "filename": "best_refined.pt", "type": "yolo"
    },
    "Dental_003": {
        "repo": "live-track/dental-boneloss", "filename": "best.pt", "type": "yolo"
    },
    "Dental_004": {
        "repo": "live-track/dental-sr", "filename": "best_swinir.pth", "type": "custom"
    },
    "Dental_008": {
        "repo": "live-track/dental-seg", "filename": "yolov8m-seg.pt", "type": "yolo"
    },
    "Dental_011": {
        "repo": "live-track/dental-age", "filename": "best_hybrid_age_model.pth", "type": "classifier"
    },
    "Dental_012": {
        "repo": "live-track/dental-periapical", "filename": "best.pt", "type": "yolo"
    },
    "Dental_013": {
        "repo": "live-track/dental-restoration", "filename": "best.pt", "type": "yolo"
    },
    "Dental_014": {
        "repo": None, "filename": "weights/best.pt", "type": "classifier" # Exists locally, but is a CNN
    }
}

def master_export():
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Add Dental_Core to path so we can use our ONNX exporters
    sys.path.append(os.path.join(base_dir, "Dental_Core"))
    try:
        from core.onnx_exporter import export_yolov8_to_onnx, export_classifier_to_onnx
    except ImportError:
        print("Please ensure Dental_Core is available.")
        return

    api = HfApi()

    for module, info in MODULE_INFO.items():
        module_dir = os.path.join(base_dir, module)
        if not os.path.exists(module_dir):
            continue
            
        print(f"\n{'='*40}\nProcessing {module}...\n{'='*40}")
        
        # 1. Recover original weights if needed
        pt_path = os.path.join(module_dir, info["filename"])
        if info["repo"] and not os.path.exists(pt_path):
            print(f"[{module}] Recovering {info['filename']} from HuggingFace ({info['repo']})...")
            os.makedirs(os.path.dirname(pt_path), exist_ok=True)
            try:
                downloaded = hf_hub_download(repo_id=info["repo"], filename=info["filename"])
                # Copy from cache to local repo so export can work
                import shutil
                shutil.copy(downloaded, pt_path)
                print(f"[{module}] Recovery successful.")
            except Exception as e:
                print(f"[{module}] Failed to recover weights: {e}")
                continue
                
        if not os.path.exists(pt_path):
            print(f"[{module}] Weights not found locally. Skipping.")
            continue

        # 2. Export to ONNX based on CORRECT architecture type
        onnx_path = None
        print(f"[{module}] Exporting as {info['type'].upper()} architecture...")
        
        try:
            if info["type"] == "yolo":
                onnx_path = export_yolov8_to_onnx(pt_path)
            elif info["type"] == "classifier":
                # For standard CNNs, we need a dummy input. Assuming (1, 3, 224, 224) generic input.
                import torch
                # Load state dict without YOLO
                state_dict = torch.load(pt_path, map_location="cpu")
                print(f"[{module}] Note: Need specific model definition for this CNN. Bypassing generic YOLO loader to prevent KeyError.")
                # Implement specific export logic or skip for now to prevent crash
                print(f"[{module}] Classifier requires custom dummy_input. Please use manual script.")
            elif info["type"] == "custom":
                print(f"[{module}] Custom architecture (e.g. SwinIR) requires manual export script.")
        except Exception as e:
            print(f"[{module}] Export failed: {e}")
            continue
            
        # 3. Upload to HyunchanAn HF org and delete local
        target_repo_id = f"HyunchanAn/{module}"
        if onnx_path and os.path.exists(onnx_path):
            print(f"[{module}] Uploading {onnx_path} to {target_repo_id}...")
            try:
                api.upload_file(
                    path_or_fileobj=onnx_path,
                    path_in_repo="weights/best.onnx",
                    repo_id=target_repo_id,
                    repo_type="model"
                )
                print(f"[{module}] Upload successful. Deleting local .pt to save space.")
                os.remove(pt_path)
                os.remove(onnx_path)
            except Exception as e:
                print(f"[{module}] Upload failed (Make sure repo exists and token is valid): {e}")

if __name__ == "__main__":
    master_export()
