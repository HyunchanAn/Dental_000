# Dental_008 YOLOv8 Finetune E2E Benchmark Report

**Date**: 2026-07-17
**Model Weights**: `hitl_finetune4/weights/best.pt` (100 Epochs, Batch 8)
**Evaluation Script**: `Dental_000/tests_008/test_evaluate_yolo.py`

## Performance Summary
- **Evaluated Images**: 50
- **Average Inference Time**: 0.0261 s/image (38.28 FPS)
- **Average Bounding Box IoU** (True Positives): 0.8200
- **Average Mask IoU** (True Positives): 0.7694

## Class-Agnostic Metrics (Tooth Detection Only)
- **True Positives (TP)**: 173
- **False Positives (FP)**: 1172
- **False Negatives (FN)**: 9
- **Precision**: 0.1286
- **Recall**: 0.9505
- **F1 Score**: 0.2266

## Class-Aware Metrics (Detection + FDI Classification)
- **True Positives (TP)**: 117
- **False Positives (FP)**: 1228
- **False Negatives (FN)**: 65
- **Precision**: 0.0870
- **Recall**: 0.6429
- **F1 Score**: 0.1532

*Note: The high recall indicates almost all teeth were detected. The high False Positives suggest that a higher confidence threshold might be needed in production, but the geometrical accuracy (Box IoU 0.82, Mask IoU 0.77) is remarkably high.*
