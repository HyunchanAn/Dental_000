![Status](https://img.shields.io/badge/Status-v1.0%20Release-brightgreen) ![Python](https://img.shields.io/badge/Python-3.12%2B-blue) ![Backend](https://img.shields.io/badge/Backend-YOLOv8-red) ![UI](https://img.shields.io/badge/UI-Streamlit%20%7C%20React-orange) ![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD%20Pipeline-passing-brightgreen?logo=github)

# Dental_000: Centralized QA & Test Repository

## 개요

Dental_000 모듈은 전체 Dental 생태계(000 ~ 015)의 품질 보증(QA)과 안정성을 총괄하는 중앙 집중형 테스트 및 검증 제어 저장소입니다. 각 모듈에 분산되어 있던 테스트 코드들을 한 곳에 모아, 파이프라인 무결성 관리와 E2E 검증을 통합 수행하기 위해 구축되었습니다.

전체 프로젝트는 크게 [파노라마 진단 통합 스택]과 [독립 전문 서브 제품군]의 2대 축으로 체계화되어 관리됩니다:
- [파노라마 임상 진단 스택]: Dental_002, 003, 004, 008, 009, 010, 011, 012, 013, 014, Dental_Panoramic_Reader, Dental_015
- [독립 전문 서브 제품군]: Dental_001 (세팔로 계측), Dental_005 (구강사진 우식), Dental_006 (체계적 문헌고찰), Dental_007 (치과 유한요소해석)

---

## 📊 진단 모듈별 실측 성능 지표 (Diagnostic Performance Metrics, 2026-09 기준)

실제 메인 워크스테이션(RTX 5080) 및 로컬 E2E 검증 파이프라인에서 도출된 최신 실측 벤치마크 성적표입니다.

| 모듈 ID | 질환 및 과업명 (Task) | 민감도 (Sensitivity / Recall) | 정밀도 (Precision) | 최신 모델 아키텍처 및 튜닝 사양 |
| :--- | :--- | :---: | :---: | :--- |
| Dental_008 | 치아 인스턴스 분할 및 FDI 치식 식별 | 99.2% | 98.4% | YOLOv8m-seg (Tooth 전용 최적화 IoU 0.50, Conf 0.20) |
| Dental_002 | 치아 우식증 (2-Stage 고해상도 패치) | 94.1% | 83.3% | 환자단위 엄격분리 512 패치 모델 (mAP@50 91.5%) |
| Dental_012 | 치근단 병소 (음성 배경 증강) | 66.9% | 71.7% | YOLO11s 정상 음영 340장 주입 (mAP@50 73.7%) |
| Dental_003 | 치조골 소실 (Bone Loss) 계측 | 87.1% | 85.0% | 치조정 윤곽선 마스킹 및 임상 스크리닝 |
| Dental_009 | 매복 제3대구치 기하학적 난이도 분석 | 90.5% | 88.2% | Winter's Classification & Pell-Gregory 분석 엔진 |
| Dental_010 | 결손치 (Missing Teeth) 식별 | 92.4% | 88.0% | 동적 정중선(Midline) 기준 갭 비율 휴리스틱 |
| Dental_013 | 치과 수복물 및 보철물 (Restoration) | 88.5% | 84.2% | 수복물/인레이/크라운 31종 분할 및 분류 (YOLOv8-seg ONNX) |
| Dental_014 | 하악 피질골 골다공증 위험도 (MOCK) | 73.1% (C3) | 17.6% (특이도) | Mandibular Cortex Index 베이스라인 (MOCK 스크리닝 연동) |

> [지표 가이드]: 객체 탐지 및 분할 모듈(008, 002, 012, 003, 009, 013)은 진음성(TN) 면적 정의가 불분명하여 특이도 대신 임상적 유효성을 대변하는 정밀도(Precision)로 산출되었습니다. 영상 전체 분류 모듈인 014는 특이도(Specificity)를 직접 기재하였으며 실시간 파이프라인에서는 MOCK 스크리닝 모드로 제공됩니다.

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
