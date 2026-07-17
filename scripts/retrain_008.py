import os
import json
import cv2
import shutil
import yaml
from ultralytics import YOLO

def convert_hitl_to_yolo(json_path, output_dir):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    images_dir = os.path.join(output_dir, 'images', 'train')
    labels_dir = os.path.join(output_dir, 'labels', 'train')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    
    # Validation split could be added, but we'll put everything in train for fine-tuning
    os.makedirs(os.path.join(output_dir, 'images', 'val'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'val'), exist_ok=True)
    
    val_count = 0
    for img_data in data:
        img_path = img_data['image_path']
        if not os.path.exists(img_path):
            continue
            
        img = cv2.imread(img_path)
        if img is None:
            continue
            
        h, w = img.shape[:2]
        base_name = os.path.basename(img_path)
        name_no_ext = os.path.splitext(base_name)[0]
        
        # Decide split (put 10% into val)
        if val_count < len(data) * 0.1:
            split_img_dir = os.path.join(output_dir, 'images', 'val')
            split_lbl_dir = os.path.join(output_dir, 'labels', 'val')
            val_count += 1
        else:
            split_img_dir = images_dir
            split_lbl_dir = labels_dir
            
        # Copy image
        dst_img = os.path.join(split_img_dir, base_name)
        if not os.path.exists(dst_img):
            shutil.copy(img_path, dst_img)
            
        # Write label
        label_path = os.path.join(split_lbl_dir, f"{name_no_ext}.txt")
        with open(label_path, 'w') as lf:
            for ann in img_data['annotations']:
                # All teeth are class 0
                cls_id = 0
                if 'segmentation' in ann and ann['segmentation']:
                    poly = ann['segmentation'][0]
                    # Normalize polygon coordinates
                    norm_poly = []
                    for i in range(0, len(poly), 2):
                        nx = poly[i] / w
                        ny = poly[i+1] / h
                        norm_poly.extend([nx, ny])
                    
                    poly_str = " ".join([f"{coord:.6f}" for coord in norm_poly])
                    lf.write(f"{cls_id} {poly_str}\n")
                elif 'bbox' in ann:
                    bx, by, bw, bh = ann['bbox']
                    cx = (bx + bw/2) / w
                    cy = (by + bh/2) / h
                    nw = bw / w
                    nh = bh / h
                    lf.write(f"{cls_id} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}\n")

    # Create dataset.yaml
    yaml_path = os.path.join(output_dir, 'dataset.yaml')
    dataset_dict = {
        'path': os.path.abspath(output_dir).replace('\\', '/'),
        'train': 'images/train',
        'val': 'images/val', # Need an empty dir at least
        'names': {0: 'tooth'}
    }
    with open(yaml_path, 'w') as f:
        yaml.dump(dataset_dict, f, sort_keys=False)
        
    return yaml_path

if __name__ == "__main__":
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "edge_cases_fdi.json"))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "yolo_fdi"))
    
    print(f"Converting HiTL JSON ({json_path}) to YOLO format...")
    yaml_path = convert_hitl_to_yolo(json_path, output_dir)
    print(f"Dataset prepared at {yaml_path}")
    
    print("Starting YOLOv8 Fine-tuning...")
    # Load the base model
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Dental_008", "yolov8m-seg.pt"))
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}. Falling back to default yolov8m-seg.pt")
        model = YOLO('yolov8m-seg.pt')
    else:
        model = YOLO(model_path)
        
    results = model.train(
        data=yaml_path,
        epochs=100, # RTX 5080 환경 본학습용 (Early Stopping 적용)
        imgsz=640,
        batch=8,   # 다른 학습과의 OOM 방지를 위해 보수적 배치 설정
        device=0,
        project='runs/segment',
        name='hitl_finetune'
    )
    print("Fine-tuning complete. Use the new weights for Dental_008.")
