# Dental 아키텍처 실무 작업 지시서 (ONNX 마이그레이션 및 Core 분리)

## 1. 개요 및 목표
기존의 지루했던 논의는 모두 아카이브하고, 본 문서는 현재 확정된 아키텍처 개선안을 실무 코드로 구현하기 위한 액션 아이템만을 명시합니다. 

[최종 목표]
1. Dental_Core 패키지 구축으로 중복 로직 제거
2. PyTorch 종속성 극복을 위한 전면 ONNX 마이그레이션
3. 파노라마 리더기의 단일 고속 런타임(onnxruntime-gpu) 환경 확보

## 2. 세부 액션 아이템

### Phase 1: Dental_Core 인프라 구축
- 대상: 신규 생성된 `Dental_Core` 리포지토리
- 작업 내용:
  1. 14개 모듈에 산재한 DICOM 로드, 이미지 리사이즈/크롭, 히스토그램 평활화, 로깅 등의 공통 함수들을 추출하여 모듈화합니다.
  2. 파이썬 표준 `setup.py` 또는 `pyproject.toml`을 작성하여, 다른 모듈들이 패키지 형태로 손쉽게 주입받아 사용할 수 있도록 구성합니다.

### Phase 2: 개별 모듈 ONNX Export 스크립트 작성
- 대상: `Dental_001` ~ `Dental_014`
- 작업 내용:
  1. 각 모듈 디렉터리 내에 `export_onnx.py` 스크립트를 새로 작성합니다.
  2. 스크립트 역할: 기존 훈련된 PyTorch 가중치(`.pt`, `.pth`)를 로드한 뒤, `torch.onnx.export()`를 사용하여 `.onnx` 파일로 변환 및 저장합니다.
  3. 변환이 완료된 ONNX 파일은 HuggingFace Hub 모델 레지스트리로 업로드하여 중앙 집중화하고, 로컬 디스크 및 커밋 트리에서는 용량 절약을 위해 즉각 삭제합니다.

### Phase 3: Panoramic_Reader 런타임 교체
- 대상: `Dental_Panoramic_Reader`
- 작업 내용:
  1. `requirements.txt`에서 무거운 `torch`, `torchvision` 의존성을 완전히 도려내고, 가벼운 `onnxruntime-gpu` 단 하나로 교체합니다.
  2. `app.py` 및 `registry.py` 리팩토링: 기존 PyTorch 모델 객체(`nn.Module`)를 14번 메모리에 올리던 로직을 지우고, 허깅페이스에서 다운로드한 ONNX 가중치를 `ort.InferenceSession()`으로 순차/병렬 로드하여 고속 추론하는 코드로 전면 개편합니다.

## 3. 작업 검수 기준
위 3단계 작업이 완료되면 다음 조건을 충족해야 합니다.
- 16GB RAM 환경에서 파노라마 리더기를 실행했을 때 OOM(메모리 초과) 셧다운 현상이 발생하지 않아야 함.
- 각 모듈 저장소에서 `.pt` 파일이 모두 사라지고, 코드 변경 없이도 ONNX 기반의 일관된 추론 결과가 출력되어야 함.

---

## 4. 작업 수행 결과 보고 (AI Assistant)

> **[보고 일시]** 2026-07-19
> 원장님께서 하달하신 위 작업 지시서(Phase 1 ~ 3)에 대한 코드 레벨의 기반 공사를 모두 완료하였습니다.

### ✅ 구현 완료 사항
1. **Phase 1 완료:** `Dental_Core` 리포지토리에 `setup.py`를 작성하여 정식 파이썬 패키지화 완료. 14개 개별 모듈 및 관제탑의 `requirements.txt`에 `git+https://...` 형태로 전역 의존성 주입 완료.
2. **Phase 2 완료:** 14개 모든 모듈(001~014) 폴더 내부에 `export_onnx.py` 자동화 스크립트 작성 및 배포 완료. (변환 로직, HuggingFace 업로드 로직, 로컬 가중치 삭제 로직 모두 포함됨)
3. **Phase 3 완료:** `Dental_Panoramic_Reader`의 종속성에서 파이토치를 완전히 제거하고, `onnx_manager.py` 엔진에 HuggingFace 스마트 캐싱 다운로드(`hf_hub_download`) 로직을 탑재 완료.

### 🚀 원장님 (메인 워크스테이션) 다음 수행 가이드
이제 원장님께서 메인 워크스테이션(GPU 및 데이터가 있는 환경)에서 **각 모듈을 순회하며 변환 스크립트를 실행**해 주시면 됩니다.

1. 터미널에서 `huggingface-cli login` 명령어로 토큰 로그인이 되어 있는지 확인합니다.
2. 각 모듈 디렉터리로 이동하여 아래 명령어를 차례대로 실행합니다.
   ```bash
   cd C:\Users\chema\Github\Dental_008   # (예시: 008 모듈)
   git pull
   python export_onnx.py
   ```
3. 변환된 가중치가 HuggingFace로 업로드되고 로컬 파일이 삭제되는 것을 확인합니다.
4. 모든 모듈(14개)의 작업이 끝나면, 관제탑(`Dental_Panoramic_Reader`)을 실행하여 OOM 없이 쾌적하게 14개 모델이 돌아가는지 최종 E2E 테스트를 수행해 주십시오!
