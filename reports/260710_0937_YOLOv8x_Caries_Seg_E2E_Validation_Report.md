# 260710_0937_YOLOv8x_Caries_Seg_E2E_Validation_Report

## 작성일: 2026-07-10 09:37 (Update: 10:01)
## 작성자: 안현찬 (Hyunchan An)

***

### 1. 개요 (Executive Summary)
본 보고서는 치아 우식증(충치) 분할 및 진단 보조를 위한 Dental_005 시스템(YOLOv8x-seg 모델 기반)의 E2E(End-to-End) 파이프라인 검증 결과를 기술합니다. 이번 검증에서는 AlphaDent 오픈 데이터셋을 사용한 모델의 로컬 인퍼런스 성능 및 CI/CD 파이프라인 정합성을 확인하고자 하였습니다.

***

### 2. 패키지 및 환경 구성 리팩토링 내역
- **Python 의존성 충돌 해결:** alphadent 패키지가 3.12 이상의 파이썬 버전을 강제하여 로컬 3.11 환경에서 설치되지 않는 문제가 발생했습니다. 이를 해결하기 위해 pyproject.toml의 requires-python 범위를 >=3.11로 하향 조정하여 성공적으로 로컬 의존성 패키징(pip install -e .)을 완료했습니다.
- **데이터셋 경로 참조 오류 보정:** 기존 data/raw/yolo_seg_train.yaml의 path가 상대 경로(./AlphaDent/)로 잘못 지정되어 검증 스크립트가 이미지를 로드하지 못하는 오류가 있었습니다. 이를 data/raw 절대 경로를 향하도록 dataset.yaml을 루트에 복제 생성하여 데이터 파이프라인을 복원했습니다.

***

### 3. 검증 결과 및 메트릭 (Validation Results & Metrics)

로컬 GPU(NVIDIA GeForce RTX 4060 Laptop GPU, 8GB VRAM)를 활용하여 `valid.py`를 수행하였습니다.
평가 과정에서 원본 이미지의 극고해상도(3000x4000 픽셀 이상)로 인해 세그멘테이션 마스크 보간 과정에서 10GB 이상의 메모리 할당이 요구되며 CUDA OOM 에러가 거듭 발생하였습니다.
이를 해결하기 위해 시각화 리포트 산출(plots=False, save_json=False)을 비활성화하고 연산 부하를 최소화하여 모델 자체의 정량적 평가 지표(mAP) 산출에 집중하였습니다.

최종 산출된 모델(YOLOv8x-seg)의 검증 지표는 다음과 같습니다.

#### Bounding Box (탐지)
- **Precision:** 0.533
- **Recall:** 0.447
- **mAP50:** 0.453
- **mAP50-95:** 0.276

#### Segmentation Mask (분할)
- **Precision:** 0.523
- **Recall:** 0.437
- **mAP50:** 0.446
- **mAP50-95:** 0.244

#### 클래스별 검증 수 (Instances)
- Abrasion (409건)
- Filling (186건)
- Crown (19건)
- Caries 1 class ~ 6 class (총 195건)

***

### 4. 추후 개선 방향 (Future Work)
1. **데이터셋 전처리 (Resize & Padding):** 검증 시 VRAM 초과 현상을 근본적으로 해결하기 위해 추론 전 모든 이미지를 특정 최대 해상도(예: 1024x1024) 이하로 일괄 축소(Resize)하여 디스크에 캐싱하는 로직 도입이 필요합니다. 
2. **클래스 불균형 해소:** Caries 클래스별 인스턴스 개수 차이가 매우 크므로 모델의 성능(Recall)이 특정 클래스에서 낮게 측정되고 있습니다. 데이터 증강(Augmentation) 또는 Loss 가중치 조정이 권장됩니다.
***

### 5. 결론
Dental_005 모델의 패키징 오류 수정과 파이프라인 정합성 확보는 완료되었습니다. 초기 발생했던 OOM 이슈 또한 평가 옵션 최적화를 통해 로컬 환경에서 정상적으로 구동되도록 해결되었으며, Bbox 및 Mask mAP 결과를 성공적으로 확보했습니다.
