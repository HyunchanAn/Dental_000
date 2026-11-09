# [ 260817 1826 랩탑 개발팀 ] Security & Hygiene Audit Report (Closed)

- 상태: Closed (2026-08-17 점검 및 Phase 2 패치 완료)

## Dental_000
- [Secrets Found]: [OK] None
- [Large Models in History]: [!] YES
  - runs/segment/runs/segment/hitl_finetune4/weights/last.pt
  - weights/yolo26n.pt
  - runs/segment/runs/segment/hitl_finetune2/weights/best.pt
  - yolov8m_seg_scratch/weights/last.pt
  - runs/segment/runs/segment/hitl_finetune4/weights/best.pt
  - ... (more)
- [.env Ignored]: [!] No
- [README Warning]: [!] No
- [Streamlit Bind]: N/A

## Dental_001
- [Secrets Found]: [OK] None
- [Large Models in History]: [!] YES
  - checkpoints/best_model.pth
  - checkpoints/legacy/cephnet_model.pth
  - checkpoints/best_unet_transfer_model_512px.pth
  - last.pt
  - yolo_runs/cvm_detector/weights/best.pt
  - ... (more)
- [.env Ignored]: [OK] Yes
- [README Warning]: [!] No
- [Streamlit Bind]: N/A

## Dental_002
- [Secrets Found]: [OK] None
- [Large Models in History]: [!] YES
  - models/best.pt
  - yolo11s.pt
  - models/best_refined.pt
- [.env Ignored]: [OK] Yes
- [README Warning]: [!] No
- [Streamlit Bind]: Missing explicit bind

## Dental_003
- [Secrets Found]: [OK] None
- [Large Models in History]: [OK] None
- [.env Ignored]: [OK] Yes
- [README Warning]: [!] No
- [Streamlit Bind]: Missing explicit bind

## Dental_004
- [Secrets Found]: [OK] None
- [Large Models in History]: [!] YES
  - checkpoints/pano_swinir_epoch_30.pth
  - checkpoints/pano_swinir_epoch_60.pth
  - checkpoints/pano_swinir_epoch_40.pth
  - checkpoints/pano_swinir_epoch_80.pth
  - checkpoints/pano_swinir_epoch_20.pth
  - ... (more)
- [.env Ignored]: [!] No
- [README Warning]: [!] No
- [Streamlit Bind]: Missing explicit bind

## Dental_005
- [Secrets Found]: [OK] None
- [Large Models in History]: [!] YES
  - weights/yolov8x_AlphaDent_9_classes_960px.pt
  - weights/yolov8x_AlphaDent_4_classes_960px.pt
  - weights/yolov8x_AlphaDent_9_classes_640px.pt
- [.env Ignored]: [OK] Yes
- [README Warning]: [!] No
- [Streamlit Bind]: N/A

## Dental_006
- [Secrets Found]: [OK] None
- [Large Models in History]: [OK] None
- [.env Ignored]: [!] No
- [README Warning]: [!] No
- [Streamlit Bind]: Missing explicit bind

## Dental_007
- [Secrets Found]: [!] YES
  - [private-key] in Miniforge3-Linux-x86_64.sh.1 (Commit: b877ed7) - Value: [REDACTED]
  - [private-key] in Miniforge3-Linux-x86_64.sh (Commit: b877ed7) - Value: [REDACTED]
- [Large Models in History]: [OK] None
- [.env Ignored]: [OK] Yes
- [README Warning]: [!] No
- [Streamlit Bind]: N/A

## Dental_008
- [Secrets Found]: [OK] None
- [Large Models in History]: [!] YES
  - weights/yolov8m-seg.pt
- [.env Ignored]: [OK] Yes
- [README Warning]: [!] No
- [Streamlit Bind]: N/A

## Dental_009
- [Secrets Found]: [OK] None
- [Large Models in History]: [OK] None
- [.env Ignored]: [OK] Yes
- [README Warning]: [!] No
- [Streamlit Bind]: N/A

## Dental_010
- [Secrets Found]: [OK] None
- [Large Models in History]: [OK] None
- [.env Ignored]: [OK] Yes
- [README Warning]: [!] No
- [Streamlit Bind]: N/A

## Dental_011
- [Secrets Found]: [OK] None
- [Large Models in History]: [!] YES
  - src/weights/last_age_model.pth
  - src/weights/best_age_model.pth
  - src/weights/best_hybrid_age_model.pth
  - classifier_best.pth
  - src/weights/last_hybrid_age_model.pth
  - ... (more)
- [.env Ignored]: [!] No
- [README Warning]: [!] No
- [Streamlit Bind]: N/A

## Dental_012
- [Secrets Found]: [OK] None
- [Large Models in History]: [!] YES
  - models/best.onnx
- [.env Ignored]: [!] No
- [README Warning]: [!] No
- [Streamlit Bind]: N/A

## Dental_013
- [Secrets Found]: [OK] None
- [Large Models in History]: [OK] None
- [.env Ignored]: [!] No
- [README Warning]: [!] No
- [Streamlit Bind]: N/A

## Dental_014
- [Secrets Found]: [OK] None
- [Large Models in History]: [OK] None
- [.env Ignored]: [OK] Yes
- [README Warning]: [!] No
- [Streamlit Bind]: Missing explicit bind

## Dental_Core
- [Secrets Found]: [OK] None
- [Large Models in History]: [OK] None
- [.env Ignored]: [!] No
- [README Warning]: [!] No
- [Streamlit Bind]: N/A

## Dental_Panoramic_Reader
- [Secrets Found]: [OK] None
- [Large Models in History]: [OK] None
- [.env Ignored]: [OK] Yes
- [README Warning]: [!] No
- [Streamlit Bind]: Missing explicit bind
