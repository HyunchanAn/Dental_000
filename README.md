![Status](https://img.shields.io/badge/Status-v1.0%20QA%20Verified%20%28UAT%20Ready%29-brightgreen "Status") ![Python](https://img.shields.io/badge/Python-3.12%2B-blue "Python") ![Backend](https://img.shields.io/badge/Backend-YOLOv8%20%2F%20ONNX-red "Backend") ![UI](https://img.shields.io/badge/UI-Streamlit%20%7C%20React-orange "UI") ![License](https://img.shields.io/badge/License-MIT-green "License") ![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD%20Pipeline-passing-brightgreen?logo=github "CI/CD Pipeline")

# Dental_000: Centralized QA & Test Orchestration Repository (중앙 집중형 품질 보증 및 통합 검증 관제소)

## 개요

`Dental_000` 모듈은 전체 Dental AI 생태계(`Dental_000` ~ `Dental_015`, `Dental_Core`, `Dental_Panoramic_Reader`)의 품질 보증(QA)과 아키텍처 무결성을 총괄하는 중앙 집중형 테스트 및 검증 제어 저장소입니다. 각 모듈에 분산되어 있던 단위·통합 테스트 코드와 벤치마크 리포트를 한 곳에 모아 파이프라인 무결성 관리와 End-to-End 검증을 수행합니다.

- [학습 및 추론 하드웨어 환경]:
  - Training Env (메인 워크스테이션): AMD Ryzen 9 9900X, NVIDIA GeForce RTX 5080 (16GB VRAM), 64GB DDR5 RAM
  - Development / Inference Env (랩탑 워크스테이션): Intel Core i5-14450HX, NVIDIA GeForce RTX 4060 Laptop GPU (8GB VRAM), 16GB DDR5 RAM
- [2대 제품군 아키텍처 구분]:
  - [파노라마 임상 진단 통합 스택]: `Dental_002`, `003`, `004`, `008`, `009`, `010`, `011`, `012`, `013`, `014`, `Dental_Panoramic_Reader`, `Dental_015`
  - [독립 전문 서브 제품군]: `Dental_001` (세팔로 29-랜드마크 및 CVM 계측), `Dental_005` (구강 임상 사진 우식 분할), `Dental_006` (체계적 문헌고찰 자동화), `Dental_007` (치과 생체역학 유한요소해석)

---

## 주요 기능 및 아키텍처

모든 테스트 리소스, 설계·감사 계획 문서, 그리고 정량 벤치마크 보고서는 본 저장소(`Dental_000`)를 단일 진실 공급원(SSOT)으로 하여 관리됩니다:

- `plans_replies_walkthrough/`: 작업계획서, 승인/반려 회신서, 작업지시서, 워크스루 기록 전용 (`[CLOSED]` / `[PASS]` 상태 관리)
- `reports/`: E2E 검증 결과서, 벤치마크 성적표, 라이선스 매트릭스 및 코드 리뷰 마크다운 전용
- `reports_archive/`: 비정형 원천 산출물(JSON, CSV, 매니페스트, 검증 스크립트 등) 보존 전용
- `tests/`: 각 서브 모듈별 유닛 및 통합 테스트 코드 (`tests_001/` ~ `tests_014/`, `tests_panoramic_reader/`)
- `scripts/`: 그리드 서치 튜너, 데이터셋 전처리, 증강 및 검증 스크립트 모음
- `modules/`: 전체 서브모듈(`Dental_001` ~ `Dental_014`, `Dental_Core`, `Dental_Panoramic_Reader`) Git Submodule 바인딩

---

## 벤치마크 및 검증 성능

실제 메인 워크스테이션(`RTX 5080`) 학습 결과, 모듈별 검증 리포트 및 10례 정량 벤치마크(`reports_archive/10_cases_quantitative_benchmark.json`)에서 도출된 최신 성적표입니다.

| 모듈 ID | 질환 및 과업명 (Task) | 검증 지표 (Validated Metrics) | 파이프라인 연동 상태 | 최신 모델 아키텍처 및 근거 아티팩트 |
| :--- | :--- | :---: | :---: | :--- |
| `Dental_008` | 치아 인스턴스 분할 및 FDI 치식 식별 | Box P 99.1% / R 99.1% / mAP@50 99.2% (mAP@50:95 60.4%) / Mask P 97.8% / R 97.8% / mAP@50 98.6% (mAP@50:95 55.6%) | `ACTIVE` (`YOLOv8m-seg` + 2-Stage FDI) | 무누수 분할(`dental_008_dentex_manifest.csv`, Train 507 / Val 127, SHA-256 교집합 0) RTX 5080 100ep 재학습 실측 (`best.pt` `88db875a...`). 독립 무치악 홀드아웃 15장 평균 0.20 FP/img (무오탐 영상 비율 86.7%, 13/15장) |
| `Dental_002` | 치아 우식증 (2-Stage 고해상도 패치) | Recall 94.1% / Precision 83.3% (mAP@50 91.5%) | `ACTIVE` (`512px` 치아 패치 추론) | 환자단위 엄격분리 512 패치 모델 (`reports/260917_2120_Dental002_2Stage_Patch_Benchmark_Report.md`) |
| `Dental_012` | 치근단 병소 (음성 배경 증강) | Recall 66.9% / Precision 71.7% (mAP@50 73.7%) | `ACTIVE` (치근단 Apex 앵커링) | YOLO11s 정상 음영 340장 주입 (`reports/260917_2105_Dental012_Negative_Aug_Benchmark_Report.md`) |
| `Dental_003` | 치조골 소실 (Bone Loss) 계측 | 단위/통합 테스트 검증 (`11 passed`) 및 Stage II~III 결손 폴리곤 실추론 | `ACTIVE` (`YOLOv8m-OBB` + `SAM` + 치간 방사선 밀도 RBL v2.0) | 2018 AAP/EFP 치주 병기 산출 및 치간부 `CLAHE` 방사선 밀도 프로파일 기반 CEJ/치조정 검출 엔진 (`radiographic_densitometric_cej_crest_v2`) |
| `Dental_009` | 매복 제3대구치 기하학적 난이도 분석 | 10례 정량 벤치마크 검출률 80.0% (TheGem 사랑니 4/4건 Recall 100%) | `ACTIVE` (Rule-based Geometry) | `Dental_008` 치아 윤곽 기반 Winter's Classification & Pell-Gregory 장축 각도 분석 엔진 |
| `Dental_010` | 결손치 (Missing Teeth) 식별 | 10례 정량 벤치마크 검출률 70.0% (확정/유보 분리) | `ACTIVE` (Rule-based Gap Heuristic) | `Dental_008` FDI 치식 및 동적 정중선(Midline) 기반 인접치 갭 비율 휴리스틱 (`modules/dental_010_heuristic.py`) |
| `Dental_013` | 치과 수복물 및 보철물 (Restoration) | 10례 정량 벤치마크 검출률 100.0% (평균 5.30개/증례) | `ACTIVE` (`YOLOv8-seg` ONNX + Contour) | 31-Class `YOLOv8-seg` 기반 4대 임상 범주(`Inlay/Onlay`, `Crown/Bridge`, `Implant`, `Endodontic (RCT)`) 분류 (`clinical_criteria_v1.json`) |
| `Dental_014` | 하악 피질골 골다공증 위험도 스크리닝 | Holdout Test Acc 54.79% / Macro-F1 0.4832 (Round 3 C3 민감도 73.1%, 특이도 17.6%) | `ACTIVE` (`OsteoMAENet` `best.pt`) | ViT-Small (`vit_small_patch16_224`) + 하악 피질골 형태학적 특징 융합 및 XAI Saliency 오버레이 (`reports/260712_1825_Dental014_Osteoporosis_Report.md`) |

> [지표 및 데이터 무결성 가이드]:
> - `Dental_008`: 과거 표기되었던 누수 검증셋(`data/yolo_fdi/images/val` 38장 중복) 기반 수치를 폐기하고, 결정론적 무누수 분할 매니페스트(`reports_archive/dental_008_dentex_manifest.csv`, Train 507장 / Val 127장, 파일명 및 SHA-256 해시 교집합 0건)와 무치악 Hard Negative 홀드아웃 분리(Train 60장 / 독립 Holdout 15장, 교집합 0건) 기준으로 메인 워크스테이션(RTX 5080) 100 에포크 재학습을 완료한 실측치입니다(`reports_archive/dental_008_leak_free_val_metrics.json`).
> - `Dental_003`: 기존의 고정 비율(`30%/40%`) 상수 휴리스틱을 폐기하고, 래스터화된 치아 마스크 행 스캔과 전체 치아 마스크(`all_teeth_mask`) 배제 치간부 `CLAHE` 방사선 밀도 프로파일 분석(`radiographic_densitometric_cej_crest_v2`)을 통해 실제 치조골 흡수 부위(`RBL >= 15%`, `loss_mm >= 2.0mm`)를 검출합니다.
> - `Dental_009` 및 `Dental_010`: 독립 학습 가중치를 가진 신경망이 아니라 `Dental_008`이 검출한 치아 BBox/Mask 및 FDI 번호 시퀀스 위에서 동작하는 기하학적 규칙 기반(Rule-based Heuristic) 모듈입니다.
> - `Dental_014`: `OsteoMAENet`(`best.pt`)과 하악 하연 형태학적 지표 융합으로 실추론(`ACTIVE_INFERENCE`)을 수행하며, 특이도 한계를 고려해 단독 확진이 아닌 임상 스크리닝 참고 지표로 제공됩니다.

### 거버넌스 및 릴리스 판정 현황 (Governance & Release Status)
- 기술 및 정량 감사 상태: `[PASS — ALL P0/P1/P2 ISSUES RESOLVED]`
  - `260928_0312` 가중치 전수 감사에서 제기되었던 `Dental_008` 검증셋 누수(38/38 중복) 및 무치악 Hard Negative 분리는 무누수 507/127 분할 100 에포크 재학습과 독립 홀드아웃(15장) 평가로 완전 해소되어 `[CLOSED]` 처리되었습니다.
  - `Dental_Panoramic_Reader` API 게이트웨이의 8개 진단 모듈(`008, 002, 012, 010, 003, 009, 013, 014`)이 모두 `ONLINE` (`8/8 ACTIVE`) 상태로 실가동됩니다.
  - `Dental_015` 임상 대시보드는 초기 빈 리포트 분리(`isDemoMode`), 업로드 파일 브라우저 SHA-256 해시 불일치 차단 게이트, 레터박스 종횡비 보존, `uncertain` 치아 수동 FDI 보정 UI를 완비하여 `v1.0 QA Verified (UAT Ready)` 상태로 운영됩니다.

---

## 데이터셋 출처 및 라이선스

- [소스 코드 라이선스]: 본 저장소(`Dental_000`) 및 시리즈 공통 파이프라인·테스트 스위트 소스 코드는 [LICENSE](LICENSE)에 명시된 `MIT License` (`Copyright (c) 2026 Hyunchan An`)를 따릅니다.
- [데이터셋 및 파생 라벨 라이선스 (`CC BY-NC-SA 4.0`)]:
  - `data/yolo_fdi/`에 수록된 파노라마 영상 및 FDI 32클래스 세그멘테이션 라벨과 `reports_archive/dental_008_dentex_manifest.csv`는 `DENTEX (Dental Enumeration and Diagnosis on Panoramic X-rays Challenge, Hamamci et al., 2023)` 데이터셋에서 파생되었으며, 원본과 동일하게 `Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)` 라이선스가 적용됩니다(상세 고지: [data/yolo_fdi/README.md](data/yolo_fdi/README.md)).
  - 비영리(`NonCommercial`) 조건이 포함된 데이터셋으로 학습된 가중치(`chemahc94/Dental-AI-Models` 등)는 학술 연구 및 비영리 교육 목적으로만 사용할 수 있습니다.
- [웹 수집 로컬 테스트 이미지 Git 추적 제외 정책]:
  - 로컬 기능 점검용으로 수집된 비공식 파노라마·세팔로 테스트 이미지(`Test_pano/`, `tests/tests_panoramic_reader/test_images_PANO/`, `tests/tests_002/test_images/`, `tests/tests_004/test_images_260608/`, `tests/tests_001/test_image_cephalo/`)는 저작권 및 출처 위생 준수를 위해 공개 Git 버전 관리에서 전면 제외(`.gitignore` 등록 및 `git rm --cached`)되었으며 로컬 개발 환경에서만 참조됩니다.
- [전체 18개 저장소 및 Hugging Face 가중치 라이선스 매트릭스]:
  - 시리즈 전체의 코드·데이터셋·가중치 라이선스 SSOT 매트릭스는 [reports/261020_0205_Dental_Series_License_and_Data_Provenance_Matrix.md](reports/261020_0205_Dental_Series_License_and_Data_Provenance_Matrix.md)에서 확인할 수 있습니다.

---

## 설치 및 실행 방법

### 1. 환경 설정 및 의존성 설치
```bash
pip install -r requirements.txt
pip install pytest
```

### 2. 모듈별 및 통합 테스트 실행
```bash
# 치아 분할 및 FDI 식별 테스트
pytest tests/tests_008/ -v

# 2-Stage 우식 검출 파이프라인 테스트
pytest tests/tests_002/ -v

# 치조골 소실 계측 및 병기 판별 테스트
pytest tests/tests_003/ -v

# 전체 파노라마 리더 통합 E2E 검증 테스트
pytest tests/tests_panoramic_reader/ -v
```

---

## 참고 문헌 및 연구용 실행 주의사항

- [DENTEX Challenge 2023]: Hamamci, I. E. et al. (2023). DENTEX: An Abnormal Tooth Detection with Dental Enumeration and Diagnosis Benchmark for Panoramic X-rays. MICCAI 2023.
- [연구용 실행 주의사항]:
  - 기본 실행 주소: `127.0.0.1` (로컬 전용)
  - 외부 공개/상용 배포 금지 및 오픈 데이터셋 외 민감 의료데이터 사용 금지
  - API 키·토큰은 환경변수로만 관리하며, 외부 접근이 필요하면 `ALLOW_EXTERNAL_ACCESS=true`로만 명시적 허용
