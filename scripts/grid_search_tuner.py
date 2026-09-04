#!/usr/bin/env python3
"""
Grid Search Hyperparameter Tuner for Dental AI Models (Ground Truth Evaluator Connected)
Real inference evaluation over PyTorch/YOLO/ONNX models against validation datasets.
Supports F1, F2 (Recall-weighted), and Recall-Constrained (Recall >= 0.80) optimization.
Designed for Main Workstation (RTX 5080) execution.
"""

import argparse
import json
import os
import sys
import time
import numpy as np
import cv2
from glob import glob
from typing import Dict, Any, List, Tuple

try:
    import torch
    from ultralytics import YOLO
except ImportError:
    torch = None
    YOLO = None


def parse_args():
    parser = argparse.ArgumentParser(description="Real Grid Search Hyperparameter Tuner for Dental AI Models")
    parser.add_argument("--module", type=str, required=True, choices=["002", "008", "012"], help="Target module ID (002, 008, 012)")
    parser.add_argument("--weights", type=str, required=True, help="Path to actual model weights (.pt / .onnx)")
    parser.add_argument("--val-data", type=str, required=True, help="Path to validation dataset directory containing images and annotations")
    parser.add_argument("--iou-min", type=float, default=0.10, help="Min NMS IoU threshold")
    parser.add_argument("--iou-max", type=float, default=0.50, help="Max NMS IoU threshold")
    parser.add_argument("--iou-step", type=float, default=0.10, help="NMS IoU step size")
    parser.add_argument("--conf-min", type=float, default=0.10, help="Min Detection confidence threshold")
    parser.add_argument("--conf-max", type=float, default=0.90, help="Max Detection confidence threshold")
    parser.add_argument("--conf-step", type=float, default=0.10, help="Detection confidence step size")
    parser.add_argument("--metric", type=str, default="f2", choices=["f1", "f2", "recall_constrained"], help="Optimization target metric")
    parser.add_argument("--min-recall", type=float, default=0.80, help="Min recall threshold for recall_constrained metric")
    parser.add_argument("--output-json", type=str, default="optimal_thresholds.json", help="Output path for optimal thresholds JSON")
    return parser.parse_args()


def compute_iou(boxA: np.ndarray, boxB: np.ndarray) -> float:
    """Compute Intersection over Union (IoU) between two bounding boxes [x1, y1, x2, y2]"""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    # Hotfix: Correct index for height (y2 - y1) from index 3 - index 1
    boxAArea = max(0, boxA[2] - boxA[0]) * max(0, boxA[3] - boxA[1])
    boxBArea = max(0, boxB[2] - boxB[0]) * max(0, boxB[3] - boxB[1])

    iou = interArea / float(boxAArea + boxBArea - interArea + 1e-6)
    return float(iou)


def load_ground_truth(val_data_path: str) -> List[Dict[str, Any]]:
    """
    Load ground truth dataset (Images and matching BBox label files).
    Supports YOLO format label text files (.txt) or COCO format JSON files.
    """
    gt_dataset = []
    
    img_extensions = ["*.png", "*.jpg", "*.jpeg", "*.bmp"]
    img_paths = []
    for ext in img_extensions:
        img_paths.extend(glob(os.path.join(val_data_path, "**", ext), recursive=True))
        img_paths.extend(glob(os.path.join(val_data_path, ext)))
        
    img_paths = sorted(list(set(img_paths)))
    
    if not img_paths:
        raise FileNotFoundError(f"No validation image files found in path: {val_data_path}")

    for img_path in img_paths:
        label_path = os.path.splitext(img_path)[0] + ".txt"
        if not os.path.exists(label_path):
            alt_path = img_path.replace(f"{os.sep}images{os.sep}", f"{os.sep}labels{os.sep}").rsplit(".", 1)[0] + ".txt"
            if os.path.exists(alt_path):
                label_path = alt_path

        gt_boxes = []
        gt_labels = []
        
        if os.path.exists(label_path):
            img = cv2.imread(img_path)
            if img is None:
                continue
            h, w = img.shape[:2]
            
            with open(label_path, "r", encoding="utf-8") as lf:
                for line in lf:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        cls_id = int(parts[0])
                        coords = np.array(list(map(float, parts[1:])))
                        if len(coords) == 4:
                            cx, cy, bw, bh = coords
                            x1 = (cx - bw / 2.0) * w
                            y1 = (cy - bh / 2.0) * h
                            x2 = (cx + bw / 2.0) * w
                            y2 = (cy + bh / 2.0) * h
                        else:
                            xs = coords[0::2] * w
                            ys = coords[1::2] * h
                            x1 = float(np.min(xs))
                            y1 = float(np.min(ys))
                            x2 = float(np.max(xs))
                            y2 = float(np.max(ys))
                        gt_boxes.append([x1, y1, x2, y2])
                        gt_labels.append(cls_id)
                        
        gt_dataset.append({
            "img_path": img_path,
            "gt_boxes": np.array(gt_boxes) if gt_boxes else np.zeros((0, 4)),
            "gt_labels": np.array(gt_labels) if gt_labels else np.zeros(0),
        })

    return gt_dataset


def calculate_metrics(precision: float, recall: float) -> Tuple[float, float]:
    f1 = (2.0 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    f2 = (5.0 * precision * recall / (4.0 * precision + recall)) if (4.0 * precision + recall) > 0 else 0.0
    return f1, f2


def run_real_grid_search(args):
    if not os.path.exists(args.weights):
        raise FileNotFoundError(f"Model weights file not found: {args.weights}")
    if not os.path.exists(args.val_data):
        raise FileNotFoundError(f"Validation dataset directory not found: {args.val_data}")

    print(f"=== Starting Real Ground-Truth Grid Search for Module {args.module} ===")
    print(f"Weights: {args.weights}")
    print(f"Validation Data: {args.val_data}")
    print(f"Target Metric: {args.metric} (Min Recall: {args.min_recall})")

    gt_dataset = load_ground_truth(args.val_data)
    print(f"Loaded {len(gt_dataset)} validation samples.")

    device = "cuda" if (torch and torch.cuda.is_available()) else "cpu"
    print(f"Loading Model on Device: {device}")
    
    model_task = "segment" if ("seg" in args.weights.lower() or args.module == "008") else "detect"
    try:
        model = YOLO(args.weights, task=model_task) if YOLO else None
    except Exception:
        model = YOLO(args.weights) if YOLO else None
    if model is None:
        raise RuntimeError("PyTorch or Ultralytics package unavailable for inference.")

    iou_grid = np.arange(args.iou_min, args.iou_max + 1e-5, args.iou_step)
    conf_grid = np.arange(args.conf_min, args.conf_max + 1e-5, args.conf_step)

    best_result = {
        "module": args.module,
        "weights": args.weights,
        "metric_target": args.metric,
        "best_iou_threshold": None,
        "best_conf_threshold": None,
        "best_score": -1.0,
        "precision": 0.0,
        "recall": 0.0,
        "f1_score": 0.0,
        "f2_score": 0.0,
        "tp": 0,
        "fp": 0,
        "fn": 0,
    }

    grid_summary_matrix = []
    total_start = time.time()

    for iou_thresh in iou_grid:
        for conf_thresh in conf_grid:
            tp, fp, fn = 0, 0, 0
            
            for item in gt_dataset:
                img_path = item["img_path"]
                gt_boxes = item["gt_boxes"]
                
                results = model(img_path, conf=float(conf_thresh), iou=float(iou_thresh), verbose=False)[0]
                pred_boxes = results.boxes.xyxy.cpu().numpy() if (results.boxes and len(results.boxes) > 0) else np.zeros((0, 4))
                
                gt_matched = [False] * len(gt_boxes)
                
                for p_box in pred_boxes:
                    best_iou = 0.0
                    best_gt_idx = -1
                    for g_idx, g_box in enumerate(gt_boxes):
                        if not gt_matched[g_idx]:
                            iou_val = compute_iou(p_box, g_box)
                            if iou_val > best_iou:
                                best_iou = iou_val
                                best_gt_idx = g_idx
                                
                    if best_iou >= 0.5:
                        tp += 1
                        if best_gt_idx >= 0:
                            gt_matched[best_gt_idx] = True
                    else:
                        fp += 1
                        
                fn += gt_matched.count(False)

            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1, f2 = calculate_metrics(precision, recall)

            if args.metric == "f1":
                score = f1
            elif args.metric == "f2":
                score = f2
            elif args.metric == "recall_constrained":
                score = precision if recall >= args.min_recall else -1.0

            entry = {
                "iou": round(float(iou_thresh), 3),
                "conf": round(float(conf_thresh), 3),
                "tp": tp,
                "fp": fp,
                "fn": fn,
                "precision": round(float(precision), 4),
                "recall": round(float(recall), 4),
                "f1": round(float(f1), 4),
                "f2": round(float(f2), 4),
                "score": round(float(score), 4),
            }
            grid_summary_matrix.append(entry)

            if score > best_result["best_score"]:
                best_result["best_score"] = round(float(score), 4)
                best_result["best_iou_threshold"] = round(float(iou_thresh), 3)
                best_result["best_conf_threshold"] = round(float(conf_thresh), 3)
                best_result["precision"] = round(float(precision), 4)
                best_result["recall"] = round(float(recall), 4)
                best_result["f1_score"] = round(float(f1), 4)
                best_result["f2_score"] = round(float(f2), 4)
                best_result["tp"] = tp
                best_result["fp"] = fp
                best_result["fn"] = fn

    elapsed_time = round(time.time() - total_start, 2)
    output_payload = {
        "optimal_config": best_result,
        "grid_summary": {
            "total_evaluations": len(grid_summary_matrix),
            "total_val_samples": len(gt_dataset),
            "total_execution_time_sec": elapsed_time,
        },
        "evaluations": grid_summary_matrix,
    }

    output_dir = os.path.dirname(os.path.abspath(args.output_json))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)

    print(f"\n[Real Ground-Truth Grid Search Complete in {elapsed_time}s]")
    print(f"Optimal IoU: {best_result['best_iou_threshold']}, Optimal Conf: {best_result['best_conf_threshold']}")
    print(f"TP: {best_result['tp']}, FP: {best_result['fp']}, FN: {best_result['fn']}")
    print(f"Precision: {best_result['precision']}, Recall: {best_result['recall']}, F2-Score: {best_result['f2_score']}")
    print(f"Optimal threshold saved to: {args.output_json}")
    
    return output_payload


if __name__ == "__main__":
    args = parse_args()
    run_real_grid_search(args)
