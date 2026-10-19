![Status](https://img.shields.io/badge/Status-v1.0%20Release-brightgreen) ![Python](https://img.shields.io/badge/Python-3.12%2B-blue) ![Backend](https://img.shields.io/badge/Backend-YOLOv8-red) ![UI](https://img.shields.io/badge/UI-Streamlit%20%7C%20React-orange) ![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD%20Pipeline-passing-brightgreen?logo=github)

# Dental_000: Centralized QA & Test Repository

## 개요

Dental_000 모듈은 전체 Dental 생태계(000 ~ 015)의 품질 보증(QA)과 안정성을 총괄하는 중앙 집중형 테스트 및 검증 제어 저장소입니다. 각 모듈에 분산되어 있던 테스트 코드들을 한 곳에 모아, 파이프라인 무결성 관리와 E2E 검증을 통합 수행하기 위해 구축되었습니다.

전체 프로젝트는 크게 [파노라마 진단 통합 스택]과 [독립 전문 서브 제품군]의 2대 축으로 체계화되어 관리됩니다:
- [파노라마 임상 진단 스택]: Dental_002, 003, 004, 008, 009, 010, 011, 012, 013, 014, Dental_Panoramic_Reader, Dental_015
- [독립 전문 서브 제품군]: Dental_001 (세팔로 계측), Dental_005 (구강사진 우식), Dental_006 (체계적 문헌고찰), Dental_007 (치과 유한요소해석)

---

## 📊 진단 모듈별 실측 성능 및 구현 상태 (Diagnostic Performance & Implementation Status, 2026-10 기준)

실제 메인 워크스테이션(RTX 5080) 학습 결과, 모듈별 검증 리포트 및 10례 정량 벤치마크(`reports_archive/10_cases_quantitative_benchmark.json`)에서 도출된 최신 성적표입니다.

| 모듈 ID | 질환 및 과업명 (Task) | 검증 지표 (Validated Metrics) | 파이프라인 연동 상태 | 최신 모델 아키텍처 및 근거 아티팩트 |
| :--- | :--- | :---: | :---: | :--- |
| Dental_008 | 치아 인스턴스 분할 및 FDI 치식 식별 | Box IoU 0.8245 / Mask IoU 0.7965 (10례 검출률 100%, 평균 28.9개) | ACTIVE (YOLOv8m-seg + 2-Stage FDI) | 기존 `data/yolo_fdi` 38장 검증셋 수치(99.2%/98.4%)는 Train-Val 중복 누수로 무효화 처리됨. 무누수 매니페스트(`dental_008_dentex_manifest.csv`, 507/127 분할) 재학습 대기 |
| Dental_002 | 치아 우식증 (2-Stage 고해상도 패치) | Recall 94.1% / Precision 83.3% (mAP@50 91.5%) | ACTIVE (512px 치아 패치 추론) | 환자단위 엄격분리 512 패치 모델 (`reports/260917_2120_Dental002_2Stage_Patch_Benchmark_Report.md`) |
| Dental_012 | 치근단 병소 (음성 배경 증강) | Recall 66.9% / Precision 71.7% (mAP@50 73.7%) | ACTIVE (치근단 Apex 앵커링) | YOLO11s 정상 음영 340장 주입 (`reports/260917_2105_Dental012_Negative_Aug_Benchmark_Report.md`) |
| Dental_003 | 치조골 소실 (Bone Loss) 계측 | 단위 테스트 검증 (RBL/Staging 기하 연산) | STANDBY (`UNIMPLEMENTED_MODEL`) | 2018 AAP/EFP 치주 병기 산출 엔진 구현 완료, 통합 파이프라인 내 랜드마크 가중치 연동 대기 |
| Dental_009 | 매복 제3대구치 기하학적 난이도 분석 | 10례 정량 벤치마크 검출률 80.0% (평균 1.30개/증례) | ACTIVE (Rule-based Geometry) | `Dental_008` 치아 윤곽 기반 Winter's Classification & Pell-Gregory 장축 각도 분석 엔진 |
| Dental_010 | 결손치 (Missing Teeth) 식별 | 10례 정량 벤치마크 검출률 70.0% (확정/유보 분리) | ACTIVE (Rule-based Gap Heuristic) | 독립 딥러닝 모델이 아닌 `Dental_008` FDI 치식 및 동적 정중선(Midline) 기반 인접치 갭 비율 휴리스틱 (`modules/dental_010_heuristic.py`) |
| Dental_013 | 치과 수복물 및 보철물 (Restoration) | 10례 정량 벤치마크 검출률 100.0% (평균 5.30개/증례) | ACTIVE (YOLOv8-seg + Contour) | 치아 ROI 크롭 기반 4대 임상 범주(`Inlay/Onlay`, `Crown/Bridge`, `Implant`, `Endodontic (RCT)`) 분류 (`clinical_criteria_v1.json`) |
| Dental_014 | 하악 피질골 골다공증 위험도 스크리닝 | Holdout Test Acc 54.79% / Macro-F1 0.4832 (MCI 베이스라인 민감도 73.1%, 특이도 17.6%) | ACTIVE (`OsteoMAENet` `best.pt`) | ViT-Small (`vit_small_patch16_224`) + 임상 변수(연령/성별) 퓨전 (`reports/260712_1825_Dental014_Osteoporosis_Report.md`) |

> [지표 및 데이터 무결성 가이드]:
> - `Dental_008`: 과거 표기되었던 Recall 99.2% / Precision 98.4% (mAP50 0.995) 수치는 `data/yolo_fdi/images/val`(38장)이 `images/train`(595장)의 부분집합이었던 데이터 누수(Leakage)로 확인되어 공식 지표에서 폐기하였습니다. 현재 결정론적 무누수 분할 매니페스트(`reports_archive/dental_008_dentex_manifest.csv`, Train 507장 / Val 127장, 교집합 0)가 구축되어 메인 워크스테이션 재학습 후 갱신될 예정입니다.
> - `Dental_009` 및 `Dental_010`: 독립 학습 가중치를 가진 신경망이 아니라 `Dental_008`이 검출한 치아 BBox/Mask 및 FDI 번호 시퀀스 위에서 동작하는 기하학적 규칙 기반(Rule-based Heuristic) 모듈입니다.
> - `Dental_014`: 기존 MCI(Mandibular Cortex Index) 기하 휴리스틱 베이스라인(C3 민감도 73.1%, 특이도 17.6%)에서 `OsteoMAENet`(`best.pt`) 실모델 추론(`ACTIVE_INFERENCE`)으로 전환되었습니다.

---

## 디렉터리 구조 및 단일 소스 저장소 (SSOT) 정책

모든 테스트 리소스, 계획 문서, 그리고 결과 보고서는 본 저장소(Dental_000)를 기준으로 중앙 집중 관리됩니다:

- plans_replies_walkthrough/: 작업계획서, 승인/반려 회신서, 작업지시서, 워크스루 기록 전용
- reports/: E2E 검증 결과서, 벤치마크 성적표, 코드 리뷰 마크다운 전용
- reports_archive/: 비정형 원천 산출물(JSON, CSV, 검증 스크립트 등) 보존 전용
- tests/: 각 서브 모듈별 유닛 및 통합 테스트 코드 (tests_001/ ~ tests_014/, tests_panoramic_reader/)
- scripts/: 그리드 서치 튜너, 데이터셋 전처리, 증강 스크립트 모음

---

## 설치 및 실행 방법

### 1. 환경 설정
```bash
pip install -r requirements.txt
pip install pytest
```

### 2. 모듈별 테스트 실행 (예시)
```bash
# 치아 분할 및 FDI 식별 테스트
pytest tests/tests_008/ -v

# 2-Stage 우식 검출 파이프라인 테스트
pytest tests/tests_002/ -v

# 전체 통합 E2E 검증 테스트
pytest tests/tests_panoramic_reader/ -v
```
