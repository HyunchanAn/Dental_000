![Status](https://img.shields.io/badge/Status-v1.0%20Release-brightgreen) ![Python](https://img.shields.io/badge/Python-3.12%2B-blue) ![Backend](https://img.shields.io/badge/Backend-YOLOv8-red) ![UI](https://img.shields.io/badge/UI-Streamlit-orange) ![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD%20Pipeline-passing-brightgreen?logo=github)

# Dental_000: Centralized Test Repository

## 개요

**Dental_000** 모듈은 전체 Dental 프로젝트(001 ~ 008)의 품질 보증(QA)과 안정성을 담당하는 중앙 집중형 테스트 코드 저장소입니다. 각 모듈에 분산되어 있던 테스트 코드들을 한 곳에 모아, 통합적인 파이프라인 관리와 E2E 검증을 효율적으로 수행하기 위해 구축되었습니다.

현재 각 프로젝트 모듈에 대한 유닛 테스트(Unit Test) 및 종단간 성능 평가(E2E Evaluation) 스크립트가 모듈별 디렉터리(tests_00X/) 하위에 체계적으로 구성되어 있습니다.

## 폴더 구조
- tests_001/: Dental_001 (Aariz Cephalometric Dataset) 관련 API 및 모델 평가 테스트
- tests_002/: Dental_002 (Caries Detection) 관련 모델/파이프라인 평가 테스트
- tests_003/: Dental_003 (Pano BoneLoss Measurement) 관련 지오메트리 및 API 서버 테스트
- tests_004/: Dental_004 (SR Iterative Dataset) 관련 초해상화 파이프라인/데이터셋 테스트
- tests_005/: Dental_005 (AlphaDent UI) 관련 Streamlit 및 배포 환경 임포트 테스트
- tests_006/: Dental_006 (PICO Extractor / Pubmed) 관련 스크래퍼 및 논문 파싱 파이프라인 테스트
- tests_008/: Dental_008 (DENTEX Instance Segmentation) 관련 E2E 모델 성능 평가 테스트

## 설치 및 실행 방법
본 레포지토리의 테스트 스크립트들은 각 원본 모듈의 src 폴더를 참조하도록 설정되어 있습니다. 따라서, 로컬 환경에서 테스트를 실행하기 위해서는 원본 레포지토리들과 함께 관리되어야 합니다.

### 환경 설정
의존성 설치 (일반적으로 각 프로젝트의 의존성과 Pytest가 필요합니다)
pip install pytest

### 테스트 실행
원하는 프로젝트의 테스트 폴더를 지정하여 pytest로 실행할 수 있습니다.
python -m pytest tests_006/
python tests_008/test_evaluate.py
