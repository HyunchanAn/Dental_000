![Status](https://img.shields.io/badge/Status-v1.0%20Release-brightgreen) ![Python](https://img.shields.io/badge/Python-3.12%2B-blue) ![Backend](https://img.shields.io/badge/Backend-YOLOv8-red) ![UI](https://img.shields.io/badge/UI-Streamlit-orange) ![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD%20Pipeline-passing-brightgreen?logo=github)

# Dental_000: Centralized Test Repository

## 개요

**Dental_000** 모듈은 전체 Dental 프로젝트(001 ~ 008)의 품질 보증(QA)과 안정성을 담당하는 중앙 집중형 테스트 코드 저장소입니다. 각 모듈에 분산되어 있던 테스트 코드들을 한 곳에 모아, 통합적인 파이프라인 관리와 E2E 검증을 효율적으로 수행하기 위해 구축되었습니다.

현재 각 프로젝트 모듈에 대한 유닛 테스트(Unit Test) 및 종단간 성능 평가(E2E Evaluation) 스크립트가 모듈별 디렉터리(tests_00X/) 하위에 체계적으로 구성되어 있습니다.

## 📊 진단 모듈별 성능 지표 (Diagnostic Performance Metrics)

각 진단 보조 AI 모듈별 최신 벤치마크 평가 결과입니다. (본 수치는 원본 리포지토리의 E2E 테스트를 거쳐 도출된 신뢰 가능한 최신 성적입니다.)

| 모듈 | 질환명 (Task) | 민감도(Sensitivity / Recall) | 특이도(Specificity) / 정밀도(Precision) | 기타 지표 |
| :--- | :--- | :---: | :---: | :--- |
| **Dental_002** | 치아 우식증 (Caries Detection) | **90.0%** | (정밀도) 36.3% | F1 Score: 0.517 (SAHI 앙상블 적용) |
| **Dental_003** | 치조골 소실 (Bone Loss) | **87.1%** | (정밀도) 85.0% | 임상 스크리닝용 적합 |
| **Dental_008** | 치아 인스턴스 분할 (Dentex) | **95.1%** | (정밀도) 12.9% | Box IoU: 0.82 (탐지 민감도 극대화) |
| **Dental_012** | 치근단 병변 (Periapical Lesion) | **64.3%** | (정밀도) 69.2% | YOLOv11s 적용 (특이도 안정화) |
| **Dental_013** | 치성 낭종/종양 (Cyst & Tumor) | **90.1%** | (정밀도) 12.3% | EfficientNet 기반 민감도 최적화 세팅 |
| **Dental_014** | 골다공증 (Osteoporosis) | **73.1%** (C3 기준)<br>**91.5%** (비정상 전체) | **17.6%** (특이도) | Accuracy: 36.0% (모드 붕괴 완치) |

> 💡 **참고 (Metrics Guide)**
> 객체 탐지(Object Detection) 및 분할(Segmentation)을 수행하는 모듈(002, 003, 008, 012, 013)은 해부학적 특성상 진음성(True Negative)의 면적 정의가 불분명하여 특이도 계산이 무의미합니다. 따라서 임상적 효용성을 대변하는 **정밀도(Precision)**로 대체 기재하였습니다. 
> 영상 전체를 분류(Classification)하는 014 모듈은 진양성/진음성 판단이 명확하므로 **특이도(Specificity)**를 직접 산출하여 기재했습니다.

## 폴더 구조
- tests_001/: Dental_001 (Aariz Cephalometric Dataset) 관련 API 및 모델 평가 테스트
- tests_002/: Dental_002 (Caries Detection) 관련 모델/파이프라인 평가 테스트
- tests_003/: Dental_003 (Pano BoneLoss Measurement) 관련 지오메트리 및 API 서버 테스트
- tests_004/: Dental_004 (SR Iterative Dataset) 관련 초해상화 파이프라인/데이터셋 테스트
- tests_005/: Dental_005 (AlphaDent UI) 관련 Streamlit 및 배포 환경 임포트 테스트
- tests_006/: Dental_006 (PICO Extractor / Pubmed) 관련 스크래퍼 및 논문 파싱 파이프라인 테스트
- tests_008/: Dental_008 (DENTEX Instance Segmentation) 관련 E2E 모델 성능 평가 테스트

## 단일 소스 저장소 (SSOT) 정책
모든 테스트 리소스(테스트 이미지 세트 등), 테스트 스크립트, 그리고 보고서(`reports_archive/`)는 개별 모듈이 아닌 오직 **본 레포지토리(`Dental_000`)**에서만 중앙 관리됩니다.
이러한 설계(QA Monorepo 방식)를 통해 통합 파이프라인은 다음과 같이 동작합니다.

### 1. 로컬 환경에서의 테스트 (수동 실행)
각 개별 모듈(`Dental_001` ~ `Dental_008`)에는 더 이상 자체 테스트 폴더(`tests/`)가 존재하지 않습니다.
따라서 로컬에서 버그를 검출하거나 모델 성능 지표를 뽑아보고 싶을 때는, 본 레포지토리(`Dental_000`)에 작성된 검증 스크립트를 실행해야 합니다.

### 2. 자동화된 CI/CD 파이프라인 (GitHub Actions)
코드를 개발하고 푸시하는 작업은 평소처럼 **해당 개별 모듈 레포지토리(`Dental_001` 등)에서 수행**하시면 됩니다.
개별 레포지토리에 푸시가 발생하면, 해당 레포의 GitHub Actions가 백그라운드에서 **자동으로 본 레포지토리(`Dental_000`)의 최신 테스트 코드들을 Clone해 와서 자체 검사를 수행**합니다. 
결과적으로 개발자는 개별 모듈 로직 구현에만 집중하고, 테스트 규격과 채점 기준은 오직 000에서 완벽하게 통제됩니다.

## 설치 및 실행 방법
본 레포지토리의 테스트 스크립트들은 각 원본 모듈의 소스 폴더를 참조하도록 설정되어 있습니다. 
개별 모듈의 루트 디렉터리에서 `Dental_000`의 테스트 스크립트를 실행하는 방식으로 동작합니다.

### 환경 설정
의존성 설치 (일반적으로 각 프로젝트의 의존성과 Pytest가 필요합니다)
```bash
pip install pytest
```

### 테스트 실행 (예시: Dental_001 테스트)
해당 대상 프로젝트(`Dental_001`)의 루트 디렉터리에서 실행하거나, PYTHONPATH를 지정하여 실행해야 모듈 참조 오류를 피할 수 있습니다.

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "C:\경로\Dental_001"
python -m pytest C:\경로\Dental_000\tests_001
```

**Linux/macOS:**
```bash
PYTHONPATH=/경로/Dental_001 pytest /경로/Dental_000/tests_001/ -v
```
