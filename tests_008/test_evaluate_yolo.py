import torch
import torchvision
import numpy as np
import cv2
import os
import time
from tqdm import tqdm
from ultralytics import YOLO

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dental_008/src')))
from dentex_seg.dataset import DENTEXDataset
from numbering.arch_sequence_matcher import assign_fdi_labels
from numbering.fdi_corrector import correct_fdi_numbers

def compute_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = box1_area + box2_area - inter_area
    
    if union_area == 0:
        return 0
    return inter_area / union_area

def compute_mask_iou(mask1, mask2):
    intersection = np.logical_and(mask1, mask2).sum()
    union = np.logical_or(mask1, mask2).sum()
    if union == 0:
        return 0
    return intersection / union

def determine_dentition_type(gt_labels, id_to_fdi):
    has_deciduous = False
    has_permanent = False
    for lbl in gt_labels:
        fdi = id_to_fdi.get(lbl.item(), 0)
        if 51 <= fdi <= 85:
            has_deciduous = True
        elif 11 <= fdi <= 48:
            has_permanent = True
            
    if has_deciduous and has_permanent:
        return "mixed"
    elif has_deciduous:
        return "deciduous"
    elif has_permanent:
        return "permanent"
    return "unknown"

def evaluate_yolo():
    print("========================================")
    print("DENTEX YOLOv8 2-Stage E2E Benchmark Evaluation")
    print("========================================")
    
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    dataset_val = DENTEXDataset(split='val')
    
    # YOLO Model Load
    weight_path = r"\\rtx4060laptop-hc\Users\chema\Github\Dental_000\runs\segment\runs\segment\hitl_finetune4\weights\best.pt"
    if not os.path.exists(weight_path):
        print(f"Error: {weight_path} not found. Training might not be completed.")
        return
        
    model = YOLO(weight_path)
    
    # Metrics
    total_time = 0
    TP = 0
    FP = 0
    FN = 0
    
    TP_agnostic = 0
    FP_agnostic = 0
    FN_agnostic = 0
    
    total_box_iou = 0
    total_mask_iou = 0
    num_matches = 0
    
    num_eval = len(dataset_val)
    print(f"평가 대상 이미지 수: {num_eval}")
    
    for idx in tqdm(range(num_eval)):
        img_id = dataset_val.img_ids[idx]
        img_info = dataset_val.images[img_id]
        img_path = os.path.join(dataset_val.img_dir, img_info['file_name'])
        
        # Load raw image for YOLO
        cv_img = cv2.imread(img_path)
        h, w, _ = cv_img.shape
        
        # Ground Truths from dataset
        _, target = dataset_val[idx]
        gt_boxes = target['boxes'].to(device)
        gt_masks = target['masks'].to(device)
        gt_labels = target['labels'].to(device)
        
        start_time = time.time()
        # YOLO inference (conf=0.25 is default, but we can adjust. NMS is handled by YOLO)
        results = model(cv_img, verbose=False, conf=0.5, iou=0.4)[0]
        
        pred_boxes = results.boxes.xyxy.to(device) if results.boxes else torch.zeros(0,4).to(device)
        pred_scores = results.boxes.conf.to(device) if results.boxes else torch.zeros(0).to(device)
        pred_cls = results.boxes.cls.to(device) if results.boxes else torch.zeros(0).to(device)
        
        # Resize masks to original image shape since YOLO returns them in different resolution (imgsz)
        if results.masks is not None:
            pred_masks_resized = torch.nn.functional.interpolate(
                results.masks.data.float().unsqueeze(1), 
                size=(h, w), 
                mode='bilinear', 
                align_corners=False
            ).squeeze(1).to(device)
        else:
            pred_masks_resized = torch.zeros((0, h, w)).to(device)
            
        end_time = time.time()
        total_time += (end_time - start_time)
        
        # 2-Stage Sequence Matcher for FDI Numbering (Initial guess)
        pred_labels_fdi = assign_fdi_labels(pred_boxes, pred_scores, w, h)
        
        # Apply FDI Correction!
        pred_labels_fdi = correct_fdi_numbers(pred_boxes, pred_labels_fdi)
        
        # Filter valid labels (> 0)
        valid_mask = pred_labels_fdi > 0
        pred_boxes = pred_boxes[valid_mask]
        pred_masks_resized = pred_masks_resized[valid_mask]
        pred_labels_fdi = pred_labels_fdi[valid_mask]
        pred_scores = pred_scores[valid_mask]
        
        # --- Class-Agnostic Evaluation (Detection Only) ---
        gt_matched_agnostic = [False] * len(gt_labels)
        
        for i in range(len(pred_boxes)):
            best_iou = 0
            best_gt_idx = -1
            for j in range(len(gt_boxes)):
                if not gt_matched_agnostic[j]:
                    iou = compute_iou(pred_boxes[i].cpu().numpy(), gt_boxes[j].cpu().numpy())
                    if iou > best_iou:
                        best_iou = iou
                        best_gt_idx = j
            
            if best_iou > 0.5:
                TP_agnostic += 1
                gt_matched_agnostic[best_gt_idx] = True
            else:
                FP_agnostic += 1
        
        FN_agnostic += gt_matched_agnostic.count(False)
        
        # --- Class-Aware Evaluation (Detection + Classification) ---
        gt_matched = [False] * len(gt_labels)
        
        for i, p_label_fdi in enumerate(pred_labels_fdi):
            # p_label_fdi is 11~48. Convert to 1~52 to compare with gt_labels
            p_label_id = dataset_val.fdi_to_id.get(int(p_label_fdi.item()), -1)
            best_iou = 0
            best_gt_idx = -1
            for j, g_label in enumerate(gt_labels):
                if p_label_id == g_label.item() and not gt_matched[j]:
                    iou = compute_iou(pred_boxes[i].cpu().numpy(), gt_boxes[j].cpu().numpy())
                    if iou > best_iou:
                        best_iou = iou
                        best_gt_idx = j
            
            if best_iou > 0.5:
                TP += 1
                gt_matched[best_gt_idx] = True
                m_iou = compute_mask_iou(pred_masks_resized[i].cpu().numpy() > 0.5, gt_masks[best_gt_idx].cpu().numpy() > 0.5)
                total_box_iou += best_iou
                total_mask_iou += m_iou
                num_matches += 1
            else:
                FP += 1
                
        FN += gt_matched.count(False)

    avg_time = total_time / num_eval if num_eval > 0 else 0
    fps = 1.0 / avg_time if avg_time > 0 else 0
    avg_box_iou = total_box_iou / num_matches if num_matches > 0 else 0
    avg_mask_iou = total_mask_iou / num_matches if num_matches > 0 else 0
    
    # Class-Aware Metrics
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    # Class-Agnostic Metrics
    precision_agn = TP_agnostic / (TP_agnostic + FP_agnostic) if (TP_agnostic + FP_agnostic) > 0 else 0
    recall_agn = TP_agnostic / (TP_agnostic + FN_agnostic) if (TP_agnostic + FN_agnostic) > 0 else 0
    f1_score_agn = 2 * (precision_agn * recall_agn) / (precision_agn + recall_agn) if (precision_agn + recall_agn) > 0 else 0

    print("========================================")
    print("E2E YOLOv8 2-Stage Benchmark Results:")
    print(f"Evaluated Images: {num_eval}")
    print(f"Average Inference Time: {avg_time:.4f} s/image ({fps:.2f} FPS)")
    print(f"Average Bounding Box IoU (True Positives): {avg_box_iou:.4f}")
    print(f"Average Mask IoU (True Positives): {avg_mask_iou:.4f}")
    print("----------------------------------------")
    print("[Class-Agnostic] (Tooth Detection Only):")
    print(f"  TP: {TP_agnostic}, FP: {FP_agnostic}, FN: {FN_agnostic}")
    print(f"  Precision: {precision_agn:.4f}, Recall: {recall_agn:.4f}, F1: {f1_score_agn:.4f}")
    print("----------------------------------------")
    print("[Class-Aware] (Detection + FDI Classification):")
    print(f"  TP: {TP}, FP: {FP}, FN: {FN}")
    print(f"  Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1_score:.4f}")
    print("========================================")

if __name__ == "__main__":
    evaluate_yolo()
