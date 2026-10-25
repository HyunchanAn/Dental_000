# Handoff: HiTL FDI Labeler UI 
Date: 2026-07-17

## Snapshot
- Target: `Dental_000` (E2E / QA Repository)
- Issue: `Dental_010` (결손치/과잉치) 연동 교착 상태를 타개하기 위해, `Dental_008`의 치식 밀림 현상 교정용 정답 데이터셋(HiTL) 구축 작업 진행 중.
- Status: 
  - `batch_fdi_filter.py`를 통해 371장의 엣지 케이스 데이터 필터링 완료.
  - `hitl_fdi_labeler.py` (Streamlit UI) 뼈대 구축 및 정답 세이브 연동 완료.
- Blocker: UI 내에서 YOLOv8-seg 마스크(Polygon) 실시간 오버레이 로직이 작동하지 않고, BBox Fallback(사각형)으로 계속 렌더링되는 문제 미해결. (IoU 매칭 로직 오류 혹은 모델의 마스크 텐서 반환값 파싱 문제로 추정)

## References
- Implementation Plan: [implementation_plan.md](file:///C:/Users/chema/.gemini/antigravity/brain/6f2c1ced-2ee6-4f10-9b4c-eccb552e4194/implementation_plan.md)
- Walkthrough: [walkthrough.md](file:///C:/Users/chema/.gemini/antigravity/brain/6f2c1ced-2ee6-4f10-9b4c-eccb552e4194/walkthrough.md)

---

# [ 261019 1203 랩탑 개발팀 HiTL FDI Labeler YOLOv8-seg 폴리곤 오버레이 Blocker 해결 및 스레드 종결 Walkthrough ]

- 수신: 안현찬 치과의사 (프로젝트 총괄)
- 발신: 랩탑 개발팀 (Intel Core i5-14450HX, RTX 4060 Laptop GPU, 16GB RAM)
- 일자: 2026-10-19 12:03 KST
- 대상 파일: `Dental_000/scripts/hitl_fdi_labeler.py`
- 스레드 상태: `[CLOSED]`

## 1. Blocker 근본 원인 규명

1. `[가중치 경로 및 모델 오지정]`:
   - `scripts/hitl_fdi_labeler.py` 97행의 `load_yolo_model()`에서 `model_path = r"C:\Users\chema\Github\Dental_008\yolov8m-seg.pt"`를 참조하고 있었다.
   - 해당 경로는 실제 워크스페이스(`D:\Github\...`)에 존재하지 않을 뿐만 아니라, `yolov8m-seg.pt`는 치아 분할 학습 가중치(`yolov8m_best.pt`)가 아닌 COCO 80클래스 일반 사물 사전학습 가중치여서 파노라마 X-ray 입력 시 치아 마스크를 전혀 생성하지 못하고 `yolo_model = None` 또는 빈 마스크로 인해 전수 사각형 `Rectangle` BBox로 폴백되고 있었다.
2. `[데이터 디렉토리 상대 경로 오류]`:
   - 스크립트가 `Dental_000/scripts/` 하위로 이동하면서 `DATA_DIR`이 `Dental_000/scripts/data`를 가리켜 상위 `Dental_000/data/edge_cases_fdi.json`을 찾지 못하는 경로 불일치가 있었다.
3. `[저장 시 원본 폴리곤(segmentation) 유실]`:
   - `edge_cases_fdi.json` 내부에는 이미 각 치아의 COCO 폴리곤 좌표(`"segmentation": [[x1, y1, ...]]`)가 존재함에도, 교정 폼 저장 시 `id, fdi, bbox`만 저장하여 폴리곤 데이터를 유실시키고 있었다.

## 2. 코드 수정 내역 (Walkthrough)

- `Dental_000/scripts/hitl_fdi_labeler.py`:
  1. `BASE_DIR` 기준으로 `Dental_000/data/edge_cases_fdi.json`을 정확히 참조하도록 `DATA_DIR` 경로 해석을 수정하였다.
  2. `load_yolo_model()`이 정규 치아 분할 가중치(`../Dental_008/weights/yolov8m_best.pt` 및 `../Dental_Panoramic_Reader/modules/Dental_008/models/yolov8m_best.pt`)를 탐색하여 로드하도록 교체하였다.
  3. 1순위로 `yolov8m_best.pt` 실시간 추론 마스크(`results[0].masks.xy`, `conf=0.20, iou=0.50`)와 어노테이션 BBox 간 최대 IoU 폴리곤을 매칭하고, 미매칭 시 2순위로 `edge_cases_fdi.json`에 내장된 원본 `segmentation` 폴리곤을 렌더링하도록 이중 폴리곤 보장 로직을 적용하였다.
  4. 라벨 저장 시 기존 `segmentation` 필드를 그대로 보존하도록 수정하였다.

## 3. 실측 검증 결과 및 종결 선언

- `edge_cases_fdi.json` 첫 번째 케이스(`train_283.png`, 어노테이션 27개)를 대상으로 수정된 `yolov8m_best.pt` 추론을 실측 실행한 결과, 총 27개의 치아 폴리곤 마스크(`YOLO masks: 27`)가 누락 없이 추출되어 사각형 BBox 폴백 없이 100% `patches.Polygon`으로 오버레이됨을 확인하였다.
- 이에 따라 2026-07-17부터 미해결로 남아 있던 본 인계 문서의 Blocker가 완전히 해소되었으므로 본 스레드를 `[CLOSED]` / `[PASS]` 완결로 공식 종결한다.

