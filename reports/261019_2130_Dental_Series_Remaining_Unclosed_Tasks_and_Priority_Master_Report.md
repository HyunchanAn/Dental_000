# [ 261019 2130 랩탑 개발팀 ] Dental 시리즈 미종결(Unclosed) 전체 태스크 및 우선순위 마스터 보고서

## 1. 보고서 개요

- 작성 일시: 2026-10-19 21:30 KST
- 작성 주체: 랩탑 개발팀 (`RTX4060Laptop-HC`, Intel Core i5-14450HX, RTX 4060 Laptop GPU 8GB VRAM, 16GB RAM)
- 조사 범위: `Dental_000` ~ `Dental_015`, `Dental_Core`, `Dental_Panoramic_Reader` 총 18개 저장소 전수 (GitHub 원격 오픈 이슈 + 로컬 `plans_replies_walkthrough/`·`reports/` 미종결 문서 + 서브모듈 `development_log.txt`·`README.md` 미체크 항목)
- 기준 상태: 2026-10-19 19:58 KST 기준 기해결·중복·스팸 이슈 10건(`Dental_002#4`, `#5`, `Dental_Core#1`, `Dental_Panoramic_Reader#4`, `#7`, `#11`, `Dental_014#1`, `Dental_000#8`, `#9`, `#10`) 및 로컬 기획서 3건(`260717_0000`, `260917_1335`, `260928_0305`) 종결(`CLOSED`) 반영 완료 후 남아 있는 모든 미종결 과업.

---

## 2. 미종결 과업 총괄 현황 (Executive Summary)

현재 Dental 시리즈 18개 저장소에 남아 있는 미종결(Unclosed) 태스크는 크게 3개 출처에 걸쳐 총 66개 단위 과업(총괄 트래킹 이슈 `#12` 별도)으로 집계된다:

| 구분 | 세부 출처 | 잔여 건수 | 핵심 성격 |
| :--- | :--- | :---: | :--- |
| 1. GitHub 원격 오픈 이슈 | 18개 저장소 Issues (`Grok` 정적 감사 등록분 잔여) | 49건 (+ 총괄 `Dental_000#12` 1건) | `[P0]` 5건, `[P1]` 20건, `[P2]` 24건 (데이터 누수 재측정, 가중치 매니페스트, macOS MPS 이전, 위생/문서 정합성) |
| 2. 로컬 미종결 기획·감사 문서 | `Dental_000/plans_replies_walkthrough/` 및 `reports/` | 3개 문서 스레드 | `260917_1635` (체어사이드 UAT 대기), `260928_0036` (원본 파노라마 GT 대조 및 불확실 치아 수동 보정 UI), `260928_0312` (무누수 재학습 및 미달 모듈 후속 결정) |
| 3. 서브모듈 내부 미체크(`- [ ]`) 백로그 | `Dental_004`, `Dental_006`, `Dental_014` 내 로그/README | 14개 체크박스 항목 | `Dental_004` 체크박스 미갱신 2건, `Dental_006` 고도화 백로그 8건, `Dental_014` 특이도/형태학 퓨전/XAI 연구 과제 4건 |

### 2.1. 수행 주체(R&R) 및 우선순위별 분류 매트릭스

- `[P0 — 최우선 차단 해제 (즉시 수행)]`: 총 6건
  - 성능 지표 왜곡(데이터 누수), E2E 환경 셋업 붕괴(`setup_env.py` 구 HF 저장소 참조), 중앙 CI 테스트 예외 삼킴(`try/except pass`), 백엔드-프론트엔드 상태 상수 불일치.
- `[P1 — 핵심 기능·이식성·법적/데이터 무결성]`: 총 23건
  - MacBook Pro(Apple Silicon `mps`) 이전 호환성(`Dental_Core` 디바이스 공통화, `D:/Github` 하드코딩 제거, `Dental_007` FEniCSx 크로스플랫폼화), 미연동/스텁 모듈(`003`, `010`, `011`, `012`, `013`, `015`) 정리, `Dental_006` Sci-Hub 제거, 데이터셋 라이선스·출처 명시, 임상 체어사이드 UAT.
- `[P2 — 저장소 위생·보조 스크립트·문서 정합성]`: 총 25건
  - 각 서브모듈 내 잔여 산출물(`.coverage`, `egg-info`, `Miniforge3.sh`, `val_predictions` 등) 추적 해제, `LICENSE` 파일 배치, README 지표 해석 및 미체크 백로그 정리.
- `[P3 — 중장기 연구·고도화 백로그]`: 총 12건
  - `Dental_005`(구강 카메라), `Dental_004`(초해상도), `Dental_014`(특이도 17.6% 개선 및 형태학 퓨전) 모델 재설계 및 `Dental_006` NLP 파이프라인 고도화.

---

## 3. 우선순위 `[P0]` 미종결 태스크 상세 (총 6건)

### 3.1. `[P0-1]` 가중치 자동 셋업(`setup_env.py`) 복구 및 단일 매니페스트화
- 관련 이슈: [Dental_Panoramic_Reader#5](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/5)
- 수행 주체: 랩탑 개발팀 (코드 수정 즉시 가능)
- 현황 및 문제점:
  - `Dental_Panoramic_Reader/setup_env.py`가 이미 삭제된 구형 HuggingFace 저장소 11개(`chemahc94/dental-cvm`, `dental-yolo` 등, 모두 HTTP 401)를 참조하고 있어 신규 환경(MacBook 등)에서 가중치 자동 다운로드가 작동하지 않음.
  - (`app.py`의 HF 경로 3건 불일치 및 `token=True` 강제 문제는 금일 커밋 `adcfddc`에서 선행 해결 완료.)
- 종결 조건:
  - 현행 공개 저장소(`chemahc94/Dental-AI-Models`, `Dental_012`, `Dental_013`, `Dental_014`) 기준 `weights_manifest.yaml` 작성 및 `setup_env.py` 개편, SHA-256 검증 추가.

### 3.2. `[P0-2]` 백엔드(`Dental_Panoramic_Reader`) ↔ 프론트엔드(`Dental_015`) 스키마/CORS 최종 정합
- 관련 이슈: [Dental_Panoramic_Reader#6](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/6)
- 수행 주체: 랩탑 개발팀 (코드 수정 즉시 가능)
- 현황 및 문제점:
  - 금일 `adcfddc` 및 `de57062` 커밋으로 `ACTIVE_INFERENCE` / `NOT_AVAILABLE` 상태 연동 및 `use_004` 좌표 정규화는 해결되었으나, `api_server.py`의 CORS 허용 출처(`localhost:3000`, `localhost:5173`) 하드코딩 환경변수화(`ALLOWED_ORIGINS`)와 프론트엔드/백엔드 간 상태 상수(`ONLINE_INFERENCE` vs `ACTIVE_INFERENCE`) 단일화 및 계약 테스트 추가가 남아 있음.
- 종결 조건:
  - `api_server.py` CORS 환경변수 처리, `osteoporosis_predictor.py`와 `api_server.py` 상태 문자열 통일, `tests_reader`에 스키마 계약 테스트 추가 후 이슈 `#6` 종결.

### 3.3. `[P0-3]` 중앙 테스트 스위트(`Dental_000/tests`) 예외 삼킴 제거 및 CI 서브모듈 체크아웃
- 관련 이슈: [Dental_000#7](https://github.com/HyunchanAn/Dental_000/issues/7)
- 수행 주체: 랩탑 개발팀 (코드 수정 즉시 가능)
- 현황 및 문제점:
  - 금일 `tests_011`~`014`의 파일 존재 확인용 스텁 4건은 실체 단위 테스트(10개 케이스)로 개편 완료했으나, `tests_001`~`010` 및 `tests_panoramic_reader` 내 26개 테스트 중 16개가 여전히 `except Exception: pass`로 실패를 삼키고 있음.
  - `.github/workflows/central_ci.yml`에 `submodules: recursive`가 누락되어 원격 CI에서 서브모듈 코드 없이 테스트가 통과 처리됨.
- 종결 조건:
  - `tests_001`~`010`, `tests_panoramic_reader`에서 `except Exception: pass` 제거, `.github/workflows/central_ci.yml`에 `submodules: recursive` 추가 및 `pytest -m "not weights"` 기준 전수 통과 확인.

### 3.4. `[P0-4]` `Dental_008` 무누수 분할(Train 507 / Val 127) 재학습 및 대표 지표 재산출
- 관련 이슈: [Dental_000#6](https://github.com/HyunchanAn/Dental_000/issues/6), [Dental_008#3](https://github.com/HyunchanAn/Dental_008/issues/3)
- 관련 로컬 문서: [260928_0312_Codex_Dental_Module_Weights_Full_Audit.md](file:///D:/Github/Dental_000/plans_replies_walkthrough/260928_0312_Codex_Dental_Module_Weights_Full_Audit.md)
- 수행 주체: 메인 워크스테이션 (`RTX 5080`) 재학습 수행 + 랩탑 개발팀 README/문서 지표 갱신
- 현황 및 문제점:
  - 기존 `yolo_fdi` 검증셋 38장이 훈련셋(596장)에 100% 중복 포함(Data Leakage)된 상태에서 산출된 `Box mAP50 0.995`가 아직 `Dental_000` 및 `Dental_008` README에 대표 성적으로 기재되어 있음.
  - 무누수 분할 매니페스트(`dental_008_dentex_manifest.csv`, Train 507 / Val 127, Overlap 0)는 이미 생성되어 있으나 실제 모델 재학습 및 127장 검증셋 재측정이 수행되지 않음.
- 종결 조건:
  -1) 당장 재학습 전이라도 README의 `0.995` 지표를 「검증셋 중복 오염으로 무효화됨(재측정 대기)」으로 정정 표기하고, 2) 메인 워크스테이션에서 507/127 무누수 분할 재학습 후 실측 지표로 갱신.

### 3.5. `[P0-5]` 오너 체어사이드 임상 UAT 및 원본 문제 파노라마 GT 대조 판정
- 관련 로컬 문서:
  - [260917_1635_Canvas_Letterbox_and_Coordinate_Pipeline_Remediation_Plan.md](file:///D:/Github/Dental_000/plans_replies_walkthrough/260917_1635_Canvas_Letterbox_and_Coordinate_Pipeline_Remediation_Plan.md) (`[CONDITIONAL HOLD]`)
  - [260928_0036_Codex_Dental_Repositories_Status_Security_Report.md](file:///D:/Github/Dental_000/reports/260928_0036_Codex_Dental_Repositories_Status_Security_Report.md) (`[임상 UAT 대기]`)
- 수행 주체: 안현찬 총괄 (임상 검수 및 원본 영상 지정)
- 현황 및 문제점:
  - 레터박스 종횡비 보존, SHA-256 Fail-Closed 가드, 치아 5% 마진 클램핑 등 기술적 조치는 모두 완료되었으나, 1) 깊은 인접면(Proximal) 우식이 5% 마진에 잘리는지 여부, 2) #14/#13·#24/#23 치식 밀림 및 #46 결손 오판이 관찰된 원본 파노라마 영상 대조 검수가 대기 중임.
- 종결 조건:
  - 안현찬 총괄의 체어사이드 UI 검수 승인 시 `260917_1635` 및 `260928_0036` 문서를 최종 `[CLOSED]`로 전환.

---

## 4. 우선순위 `[P1]` 미종결 태스크 상세 (총 23건)

### 4.1. Apple Silicon (`mps`) 이식성 및 하드코딩 절대경로 제거 (5건)
1. [Dental_Core#2](https://github.com/HyunchanAn/Dental_Core/issues/2): `Dental_Core`에 공통 디바이스 선택 헬퍼(`get_device()`: `cuda -> mps -> cpu`) 및 경로 해석 유틸리티 추가, `onnxruntime-gpu==1.19.2` 및 `torch==2.4.0` 엄격 핀을 macOS 호환 조건부 의존성으로 완화.
2. [Dental_Panoramic_Reader#9](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/9): `requirements.txt`의 `onnxruntime-gpu==1.19.2` 플랫폼 분기(`sys_platform != 'darwin'`), `core/model_manager.py` 및 `core/interfaces/*.py`에 `torch.backends.mps.is_available()` 및 `torch.mps.empty_cache()` 추가, `D:/Github` 절대경로 제거.
3. [Dental_005#3](https://github.com/HyunchanAn/Dental_005/issues/3): `scripts/` 내 6개 파일의 `D:/Github/Dental_005` 하드코딩을 `Path(__file__).resolve().parents[1]` 상대경로로 치환 및 MPS 디바이스 지원 추가.
4. [Dental_006#1](https://github.com/HyunchanAn/Dental_006/issues/1): `archive/test_ pipeline.py`(공백 파일명) 정리, `D:\Github\Dental_006` Windows 경로 제거, `requirements.txt`의 미사용 `faiss-cpu`/`spacy` 정리 및 `device="mps"` 지원.
5. [Dental_007#6](https://github.com/HyunchanAn/Dental_007/issues/6): Windows WSL/Mock 전제인 `src/solver.py`에서 macOS/Linux conda-forge `fenics-dolfinx`가 설치된 경우 네이티브 솔버가 즉시 동작하도록 분기 개선 및 `conda-env.yml` 제공.

### 4.2. 모듈별 추론·연동 완결성 및 문서-구현 불일치 해소 (9건)
6. [Dental_Panoramic_Reader#8](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/8):
   - `Dental_003` (`core/interfaces/dental_003.py`의 `UNIMPLEMENTED_MODEL` 스텁 vs `modules/boneloss_predictor.py` 실제 구현 연결)
   - `Dental_011` (치아 연령 추정기 `modules/age_predictor.py`를 `core/pipeline.py` 및 `api_server.py`에 연결할지 여부)
   - `Dental_004` (`core/interfaces/dental_004.py`의 `../../../Dental_004` 상위 경로 참조를 `modules/Dental_004` 서브모듈 참조로 통일)
7. [Dental_003#5](https://github.com/HyunchanAn/Dental_003/issues/5): `Dental_003/api/main.py`가 존재하지 않는 `dummy_yolo.pt`를 로드하고 `PerioLandmarkPredictor(backbone_type="swin")` 잘못된 시그니처를 호출하여 기동 불가한 버그 수정.
8. [Dental_010#1](https://github.com/HyunchanAn/Dental_010/issues/1): `Dental_010` 단독 저장소는 38줄 스텁인데 실제 고도화된 갭 비율(`r_gap`)·정중선 결손치 로직은 `Dental_Panoramic_Reader/api_server.py` 및 `core/interfaces/dental_010.py`에만 존재하는 불일치 해소(로직을 `Dental_010`으로 이관 후 리더가 임포트).
9. [Dental_011#2](https://github.com/HyunchanAn/Dental_011/issues/2): `Dental_011`이 별도 test 분할 없이 validation(800장)에서 체크포인트를 선택하고 동일 val 셋의 MAE(`1.51년`)를 최종 성적으로 보고한 한계 명시 또는 80/10/10 재분할 평가.
10. [Dental_012#1](https://github.com/HyunchanAn/Dental_012/issues/1): `Dental_012` 저장소 내에는 학습 스크립트만 있고 실제 추론·다근치 Apex 앵커링 로직은 `Dental_Panoramic_Reader/modules/periapical_predictor.py`에만 존재하는 구조 정리 및 README의 미구현 `tooth_Association` 설명 정정.
11. [Dental_013#1](https://github.com/HyunchanAn/Dental_013/issues/1): `Dental_000` README의 「31종 YOLOv8-seg 88.5%/84.2%」 설명과 `Dental_013` 단독 저장소 코드(EfficientNet 5클래스 분류기) 간의 불일치 정정.
12. [Dental_015#1](https://github.com/HyunchanAn/Dental_015/issues/1): `Dental_015` 초기 구동 시 `mockFinalReport`로 시작하는 구조를 빈 상태(`emptyReport`) 기본 시작 + 「데모 샘플 불러오기」 클릭 시에만 목업 로드로 변경할지 여부 결정.
13. [Dental_007#7](https://github.com/HyunchanAn/Dental_007/issues/7): `Dental_007`에서 교합점 거리 5mm 이내 노드에 동일한 100N 체적력을 부과하여 메쉬 밀도에 따라 총 하중이 달라지는 유한요소해석(FEA) 경계조건 수식 보정 및 해석적 해(외팔보/축하중 봉) 대비 검증 테스트 추가.
14. [260928_0036 불확실 치아 수동 보정 UI](file:///D:/Github/Dental_000/reports/260928_0036_Codex_Dental_Repositories_Status_Security_Report.md#L470-L472): `uncertain: True`로 플래깅된 치아를 `Dental_015` 화면에서 임상가가 원클릭으로 치식 번호를 수정할 수 있는 인터랙션 구현.

### 4.3. 데이터셋 출처·라이선스·법적 리스크 정리 (9건)
15. [Dental_006#2](https://github.com/HyunchanAn/Dental_006/issues/2): `src/downloader.py`의 Sci-Hub 미러 폴백 다운로드 코드(`_tier3_scihub`) 및 `README.md`의 Sci-Hub 안내 제거 (저작권 및 기관 규정 리스크).
16. [Dental_005#4](https://github.com/HyunchanAn/Dental_005/issues/4): `data/annotated_100/` 커밋된 구강 사진 90장의 원천 데이터셋 출처·라이선스 명시 또는 Git 추적 해제.
17. [Dental_008#4](https://github.com/HyunchanAn/Dental_008/issues/4): DENTEX 데이터셋의 공식 라이선스(`CC BY-NC-SA 4.0`, 비영리·동일조건변경허락)와 레포의 `MIT License` 표기 간 구분 명시(코드 MIT / 데이터·파생 가중치 CC BY-NC-SA 4.0).
18. [Dental_011#3](https://github.com/HyunchanAn/Dental_011/issues/3): `Dental_011`에서 사용한 Kaggle 4,000장 파노라마 데이터셋의 정확한 URL/DOI/라이선스 및 환자 단위 분할 여부 명시.
19. [Dental_012#2](https://github.com/HyunchanAn/Dental_012/issues/2): `Dental_012` 치근단 병소 파노라마 데이터셋의 원천 출처·라이선스·클래스 정의 명시.
20. [Dental_014#2](https://github.com/HyunchanAn/Dental_014/issues/2): `Dental_014`의 「BRAR-anchored 1,104명」 데이터셋 출처(논문/URL/접근 조건) 및 환자 단위 분할 여부 명시.
21. [Dental_Core#3](https://github.com/HyunchanAn/Dental_Core/issues/3): `Dental_Core` 루트 `LICENSE` 파일 추가 및 `pyproject.toml` 버전(`0.1.0`)과 README 배지(`v1.0 Release`) 통일.
22. [Dental_Panoramic_Reader#10](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/10): `Dental_Panoramic_Reader` 루트 `LICENSE` 파일 추가 및 Tufts/DENTEX 비영리 데이터셋 이용 조건 안내 보강.
23. [260928_0312 Codex 감사관 최종 서명](file:///D:/Github/Dental_000/plans_replies_walkthrough/260928_0312_Codex_Dental_Module_Weights_Full_Audit.md#L1852-L1860): `10_cases_quantitative_benchmark.json` 미달 후보 IoU 추적성 보완 완료에 대한 독립 감사관 최종 확인(자체 종결 가능).

---

## 5. 우선순위 `[P2]` 미종결 태스크 상세 (총 25건)

### 5.1. 서브모듈별 저장소 위생 정리 및 불필요 추적 파일 제거 (11건)
1. [Dental_002#7](https://github.com/HyunchanAn/Dental_002/issues/7): `Dental_002` 내 `.coverage`, 비 UTF-8 인코딩으로 `pytest` 수집 오류를 유발하는 `logs/test_results.txt`, `archive/scripts/` 15개 일회성 스크립트 정리 (`#4`, `#5` 중복 이슈 종결은 금일 완료).
2. [Dental_003#7](https://github.com/HyunchanAn/Dental_003/issues/7): `Dental_003` 내 `pano_boneloss.egg-info/` 추적 해제, 학습 스크립트 MPS 지원 및 macOS/Linux 환경변수 안내 추가.
3. [Dental_005#5](https://github.com/HyunchanAn/Dental_005/issues/5): `Dental_005` 내 `dental_005.egg-info/`, `val_predictions/`(45장), `models/classification_report.txt` 추적 해제 및 `LICENSE` 파일 추가, `tests/` 추가.
4. [Dental_006#3](https://github.com/HyunchanAn/Dental_006/issues/3): `Dental_006` 루트의 `commits.json`, `error.log`, `git_log.txt`, `pytest_out.txt` 등 디버그 산출물 9개 삭제, `docs/development_log.txt` 단일화, `LICENSE` 추가.
5. [Dental_007#8](https://github.com/HyunchanAn/Dental_007/issues/8): `Dental_007`에 커밋된 86MB 리눅스 설치 바이너리(`Miniforge3.sh`), `extract.log`, `fenics_test.log` 삭제 및 `.gitignore` 추가, `LICENSE` 추가.
6. [Dental_008#6](https://github.com/HyunchanAn/Dental_008/issues/6): `Dental_008` 내 `test_output.txt`, `train_log*.txt`, `eda_summary.txt`, `dataset/dentex_yolo/` 82개 빈 라벨 파일 및 루트 일회성 스크립트 정리, `LICENSE` 추가.
7. [Dental_010#2](https://github.com/HyunchanAn/Dental_010/issues/2): `Dental_010` 내 `missing_tooth.egg-info/` 추적 해제, `pyproject.toml` 플레이스홀더(`your.email@example.com`, `0.1.0`) 수정, `LICENSE` 추가.
8. [Dental_011#5](https://github.com/HyunchanAn/Dental_011/issues/5): `Dental_011` 내 빈 `data/` 서브모듈 엔트리 제거, `models/sample_xai_heatmap.jpg` 정리, `LICENSE` 추가.
9. [Dental_012#4](https://github.com/HyunchanAn/Dental_012/issues/4): `Dental_012` 내 `data_sample.txt`(ZIP 바이너리 조각), `results.txt`, `train_283.png` 제거 및 `LICENSE` 추가.
10. [Dental_015#2](https://github.com/HyunchanAn/Dental_015/issues/2): `Dental_015` 루트 `LICENSE` 추가, `public/sample_panorama.png` 출처 명시, 프론트엔드 기본 단위 테스트(Vitest) 추가.
11. [Dental_000#11](https://github.com/HyunchanAn/Dental_000/issues/11): `Dental_000` 내 `benchmark_scripts/run_clinical_evaluation.py`의 MPS ExecutionProvider 폴백 보완 및 `setup_workspace.py`/`sync_all.py`를 MacBook에서도 사용할 수 있도록 경로 옵션화 (가짜 수치 출력 제거는 금일 완료).

### 5.2. 서브모듈 보조 스크립트 macOS(`mps`) 디바이스 지원 (7건)
12. [Dental_001#9](https://github.com/HyunchanAn/Dental_001/issues/9): `Dental_001` `.env.example`(`DEVICE=auto`), `tools/inference.py`에 `cuda` 분기 추가(`cuda -> mps -> cpu`), `scripts/evaluate.py` MPS 지원.
13. [Dental_002#6](https://github.com/HyunchanAn/Dental_002/issues/6): `Dental_002` `data.yaml`/`data_refined.yaml` 절대경로(`D:/Github`, `C:/Users/...`)를 상대경로로 수정, `app.py` macOS 한글 폰트(`AppleSDGothicNeo.ttc`) 폴백 추가, `core.py` MPS 지원.
14. [Dental_008#5](https://github.com/HyunchanAn/Dental_008/issues/5): `Dental_008` `src/train.py`, `src/inference.py` 등에 `cuda -> mps -> cpu` 자동 선택 적용 및 `scripts/download_data.py` 안내 개선.
15. [Dental_009#1](https://github.com/HyunchanAn/Dental_009/issues/1): `Dental_009` `LICENSE` 추가, `pyproject.toml` 버전 정합화, 규칙 기반 알고리즘의 검증 한계 README 명시.
16. [Dental_011#4](https://github.com/HyunchanAn/Dental_011/issues/4): `Dental_011` `src/train.py`, `evaluate.py`, `inference.py`, `explain.py`, `export_onnx.py`에 MPS 디바이스 지원 추가.
17. [Dental_012#3](https://github.com/HyunchanAn/Dental_012/issues/3): `Dental_012` `src/train.py`(`device=0` 하드코딩) 및 `prepare_data.py`(`C:\Users\...` 경로 주석)에 크로스플랫폼/MPS 지원 추가.
18. [Dental_014#3](https://github.com/HyunchanAn/Dental_014/issues/3): `Dental_014` `scripts/train.py`, `train_unet.py`, `eval.py`, `src/dental_014/inference.py` 등 6개 파일에 MPS 디바이스 지원 추가.

### 5.3. 서브모듈 문서·지표·라이선스 설명 정합화 (7건)
19. [Dental_001#8](https://github.com/HyunchanAn/Dental_001/issues/8): `Dental_001` Aariz 데이터셋 라이선스·출처 표기, `models/hrnet_w32_512x512.onnx` Git LFS 또는 HF 이관 검토, `LICENSE` 파일 추가.
20. [Dental_001#10](https://github.com/HyunchanAn/Dental_001/issues/10): `Dental_001` README의 `MRE 3.8612 px (< 4.6 px = 2.0mm)` 픽셀-mm 환산 기준 명시 및 CVM Accuracy 45.05%(QWK 0.6123) 한계 설명 보강.
21. [Dental_003#6](https://github.com/HyunchanAn/Dental_003/issues/6): `Dental_003` README의 데이터셋 표기(UFBA-UESC vs 실제 `download_dataset.py`의 Zenodo 4457648 CC BY 4.0) 일치화 및 `LICENSE` 추가.
22. [Dental_004#10](https://github.com/HyunchanAn/Dental_004/issues/10): `Dental_004` `samples/ex_pano01~05.jpeg`(스톡 워터마크 포함 웹 수집 이미지)를 공개 데이터셋 샘플로 교체 및 `LICENSE` 추가.
23. [Dental_004#11](https://github.com/HyunchanAn/Dental_004/issues/11) + `Dental_004/development_log.txt` 미체크 2건: `Dental_004` README의 SSIM `0.8413` 문구 조정 및 `development_log.txt` 73~74행의 이미 완료된 체크박스 2건(`- [x] 커뮤니티 및 협업 준비`, `- [x] 문서 고도화`) 갱신.
24. [Dental_Core#4](https://github.com/HyunchanAn/Dental_Core/issues/4): `Dental_Core` 자체 `tests/` 폴더에 `preprocess_panoramic_image` 단위 테스트 추가.
25. [Dental_000#12](https://github.com/HyunchanAn/Dental_000/issues/12): 전체 시리즈 총괄 트래킹 이슈 (하위 이슈 종결 시 체크리스트 연동 갱신).

---

## 6. 우선순위 `[P3]` 중장기 모델 재설계 및 서브모듈 고도화 백로그 (총 12건)

개별 저장소의 `development_log.txt` 및 `README.md`에 체크박스(`- [ ]`)로 기록되어 있는 중장기 연구·엔지니어링 백로그이다:

### 6.1. `Dental_014` (`README.md` Future Roadmap 미체크 4건)
1. `- [ ] 특이도(Specificity) 개선`: 정상군(C1) 특이도 17.6% 한계 극복을 위한 클래스 불균형 해소 및 정상 데이터 증강.
2. `- [ ] 형태학적 특징 결합 (Morphological Fusion)`: `morphology_analyzer.py`의 하악 피질골 두께(MCW) 지표를 ViT 임베딩과 결합하여 Mode Collapse 해결.
3. `- [ ] 설명 가능한 AI (XAI) 파이프라인 연동`: Grad-CAM 또는 Attention Map 시각화를 추론 결과와 함께 출력.
4. `- [ ] 최종 목표 지표 달성`: Macro F1 Score 0.70 이상 달성 및 일반화 성능 벤치마크 확립.

### 6.2. `Dental_006` (`development_log.txt` 고도화 백로그 미체크 8건)
5. `- [ ] README.md 업그레이드` (Installation, Quick Start, Usage, Mermaid 아키텍처 다이어그램, 한계점 명시)
6. `- [ ] 주요 함수 및 클래스에 Google/NumPy 스타일 docstring 작성 및 Type Hints 90% 이상 적용`
7. `- [ ] pydantic-settings 및 .env.example 활용 환경변수/시크릿 관리 일원화`
8. `- [ ] loguru 기반 구조화 로깅(Structured Logging) 도입`
9. `- [ ] PRISMA flow diagram 자동 생성 기능 및 테스트 보강`
10. `- [ ] 합성 데이터(Synthetic Data)를 활용한 End-to-End 통합 파이프라인 테스트 작성`
11. `- [ ] Semantic Versioning (SemVer) 준수 및 CHANGELOG.md 관리 자동화`
12. `- [ ] 의료 도메인 Model Card 및 RoB 평가 정확도/신뢰성 검증 리포트 작성`

---

## 7. 단계별 권장 실행 로드맵 (Execution Plan)

1. `[1단계 — 랩탑 개발팀 단독 즉시 종결 가능 P0/P1 패치]`:
   - `Dental_Panoramic_Reader#5` (`setup_env.py` 현행 HF 저장소 매핑 복구)
   - `Dental_Panoramic_Reader#6` (CORS 환경변수화 및 상태 상수 통일)
   - `Dental_000#7` (`tests_001`~`010` `except Exception: pass` 제거 및 `central_ci.yml` `submodules: recursive` 추가)
   - `Dental_006#2` (`src/downloader.py` Sci-Hub 폴백 코드 즉시 제거)
   - `Dental_003#5` (`api/main.py` 생성자 시그니처 수정)
2. `[2단계 — 크로스플랫폼(macOS MPS) 및 상대경로 일괄 정비]`:
   - `Dental_Core#2`, `#3`, `#4` (`get_device()` 공통 함수 및 `LICENSE`, 단위 테스트 추가)
   - `Dental_Panoramic_Reader#9`, `Dental_001#9`, `Dental_002#6`, `Dental_005#3`, `Dental_006#1`, `Dental_007#6`, `Dental_008#5`, `Dental_011#4`, `Dental_012#3`, `Dental_014#3` 일괄 처리.
3. `[3단계 — 전 서브모듈 위생(`.gitignore` / 불필요 산출물 / `LICENSE` / 데이터 출처) 일괄 정리]`:
   - `Dental_001#8`, `#10`, `Dental_002#7`, `Dental_003#6`, `#7`, `Dental_004#10`, `#11`, `Dental_005#4`, `#5`, `Dental_006#3`, `Dental_007#8`, `Dental_008#4`, `#6`, `Dental_009#1`, `Dental_010#1`, `#2`, `Dental_011#2`, `#3`, `#5`, `Dental_012#1`, `#2`, `#4`, `Dental_013#1`, `Dental_014#2`, `Dental_015#1`, `#2`, `Dental_Panoramic_Reader#8`, `#10`, `Dental_000#11` 순차 종결.
4. `[4단계 — 메인 워크스테이션(RTX 5080) 연산 과제]`:
   - `Dental_000#6` / `Dental_008#3`: `dental_008_dentex_manifest.csv`(Train 507 / Val 127) 무누수 분할 재학습 및 127장 검증셋 실측 지표로 README 갱신.
5. `[5단계 — 안현찬 총괄 임상 UAT 및 최종 Sign-off]`:
   - `260917_1635` 및 `260928_0036` 체어사이드 시각 검증 후 전체 스레드 최종 종결.
