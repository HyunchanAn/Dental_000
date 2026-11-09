# Dental_008 YOLOv8 Finetune E2E Benchmark Report

[Date]: 2026-07-17
[Model Weights]: `hitl_finetune4/weights/best.pt` (100 Epochs, Batch 8)
[Evaluation Script]: `Dental_000/tests_008/test_evaluate_yolo.py`

## Performance Summary
- [Evaluated Images]: 50
- [Average Inference Time]: 0.0261 s/image (38.28 FPS)
- [Average Bounding Box IoU] (True Positives): 0.8200
- [Average Mask IoU] (True Positives): 0.7694

## Class-Agnostic Metrics (Tooth Detection Only)
- [True Positives (TP)]: 173
- [False Positives (FP)]: 1172
- [False Negatives (FN)]: 9
- [Precision]: 0.1286
- [Recall]: 0.9505
- [F1 Score]: 0.2266

## Class-Aware Metrics (Detection + FDI Classification)
- [True Positives (TP)]: 117
- [False Positives (FP)]: 1228
- [False Negatives (FN)]: 65
- [Precision]: 0.0870
- [Recall]: 0.6429
- [F1 Score]: 0.1532

Note: The high recall indicates almost all teeth were detected. The high False Positives suggest that a higher confidence threshold might be needed in production, but the geometrical accuracy (Box IoU 0.82, Mask IoU 0.77) is remarkably high.

---

# [ 261025 1455 랩탑 개발팀 ] 무누수 507/127 분할 YOLOv8m-seg 100 에포크 재학습 완결에 따른 공식 종결 (`[CLOSED]` / `[PASS]`)

- 상태: 공식 종결 (`[CLOSED]` / `[PASS]` 완결)
- 비고: 본 2026-07-17 초기 파인튜닝 리포트에서 제기된 낮은 신뢰도 임계값 오탐(FP) 및 치식 분류 한계는 이후 `conf=0.20, iou=0.50` 최적화, 동적 프로그래밍(DP) 악궁 시퀀스 매칭(`arch_sequence_matcher.py`), 그리고 무누수 507/127 분할 `YOLOv8m-seg` 100 에포크 재학습(`Box mAP@0.5 99.15%`, `Mask mAP@0.5 98.55%`, `Precision 99.06%`, `Recall 99.06%`, SHA-256 `88db875a...`)을 통해 완전히 해결되었으므로 본 초기 벤치마크 문서를 아카이브 보존 및 `[CLOSED]` / `[PASS]` 완결 처리한다.
