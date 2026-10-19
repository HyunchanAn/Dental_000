# DENTEX Derived FDI Tooth Segmentation Dataset (`data/yolo_fdi`)

## 1. 원본 데이터셋 출처 및 인용 (Provenance & Citation)
- 원본 데이터셋: `DENTEX (Dental Enumeration and Diagnosis on Panoramic X-rays Challenge)`
- 공식 저장소 및 배포처:
  - Hugging Face Datasets: `https://huggingface.co/datasets/ibrahimhamamci/DENTEX`
  - Zenodo / Challenge Portal: MICCAI 2023 DENTEX Challenge
- 대표 논문 인용:
  - Hamamci, I. E., Er, S., Simsar, E., Yuksel, A. E., Gultekin, S., Ozdemir, S. D., Yang, K., Li, H. B., Pati, S., Stadlinger, B., Mehl, A., Gunduz, D., & Menze, B. (2023). `DENTEX: An Abnormal Tooth Detection with Dental Enumeration and Diagnosis Benchmark for Panoramic X-rays`. arXiv preprint `arXiv:2305.19112`.

## 2. 라이선스 및 이용 조건 (License: CC BY-NC-SA 4.0)
- 본 디렉터리(`data/yolo_fdi/`)에 포함된 파노라마 방사선 영상 및 파생 YOLO 세그멘테이션 라벨(`labels/`)은 원본 DENTEX 데이터셋의 라이선스인 `Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)` 조건을 그대로 승계합니다.
- 라이선스 전문: `https://creativecommons.org/licenses/by-nc-sa/4.0/`
- 핵심 준수 사항:
  1. [저작자 표시 (Attribution)]: 원 저작자(Hamamci et al., 2023) 및 DENTEX 데이터셋 출처를 명시해야 합니다.
  2. [비영리 목적 한정 (NonCommercial)]: 본 데이터셋, 파생 라벨(`labels/train`, `labels/val`), 그리고 이를 학습하여 생성된 파생 모델 가중치는 학술 연구 및 비영리 교육 목적으로만 사용할 수 있으며, 상업적 목적의 재배포나 상용 서비스 직접 투입을 금지합니다.
  3. [동일조건변경허락 (ShareAlike)]: 본 데이터셋이나 라벨을 수정·보정한 2차적 저작물 역시 동일한 `CC BY-NC-SA 4.0` 라이선스로 배포해야 합니다.

## 3. 원본 대비 변경 사항 및 재배포 정책 (Modifications & Redistribution Record)
1. [클래스 체계 및 포맷 변환]:
   - 원본 DENTEX `quadrant_enumeration` COCO JSON 어노테이션을 FDI 32개 영구치 클래스(`0`~`31` 인덱스, FDI `11`~`48`)의 YOLOv8-seg 폴리곤 정규화 포맷(`.txt`)으로 변환하고, HiTL(Human-in-the-Loop) 검수를 통해 오라벨을 정제하였습니다.
2. [데이터 누수(Data Leakage) 완전 제거]:
   - 과거 `images/val`(38장)과 중복되던 `images/train` 내부의 동일 이미지 38장 및 라벨을 물리적으로 삭제하여, 현재 `train`(462장)과 `val`(38장) 간 파일명 및 SHA-256 바이트 해시 교집합이 `0건`(완전 분리)임을 보장합니다.
   - 전체 634장 기준의 표준 무누수 분할(Train 507장 / Val 127장, 바이트 해시 교집합 `0건`) 매니페스트는 `Dental_000/reports_archive/dental_008_dentex_manifest.csv`에서 관리합니다.
3. [재배포 정책 기록]:
   - 중앙 CI/CD 회귀 검증 및 HiTL 검수 재현성을 위해 정제된 서브셋을 `CC BY-NC-SA 4.0` 명시 하에 유지하되, 신규 대규모 학습 시에는 원본 DENTEX 배포처(`ibrahimhamamci/DENTEX`)에서 다운로드 후 `reports_archive/dental_008_dentex_manifest.csv` 기준으로 분할을 재구성하도록 표준화하였습니다.
