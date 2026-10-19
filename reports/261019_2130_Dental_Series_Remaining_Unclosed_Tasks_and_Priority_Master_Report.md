# [ 261019 2130 랩탑 개발팀 ] Dental 시리즈 미종결(Unclosed) 전체 태스크 및 우선순위 마스터 보고서

## 1. 보고서 개요

- 작성 일시: 2026-10-19 21:30 KST
- 작성 주체: 랩탑 개발팀 (`RTX4060Laptop-HC`, Intel Core i5-14450HX, RTX 4060 Laptop GPU 8GB VRAM, 16GB RAM)
- 조사 범위: `Dental_000` ~ `Dental_015`, `Dental_Core`, `Dental_Panoramic_Reader` 총 18개 저장소 전수 (GitHub 원격 오픈 이슈 + 로컬 `plans_replies_walkthrough/`·`reports/` 미종결 문서 + 서브모듈 `development_log.txt`·`README.md` 미체크 항목)
- 기준 상태: 2026-10-19 19:58 KST 기준 기해결·중복·스팸 이슈 10건(`Dental_002#4`, `#5`, `Dental_Core#1`, `Dental_Panoramic_Reader#4`, `#7`, `#11`, `Dental_014#1`, `Dental_000#8`, `#9`, `#10`) 및 로컬 기획서 3건(`260717_0000`, `260917_1335`, `260928_0305`) 종결(`CLOSED`) 반영 완료 후 남아 있는 모든 미종결 과업.

---

## 2. 미종결 과업 총괄 현황 (Executive Summary)

현재 Dental 시리즈 18개 저장소에 남아 있는 미종결(Unclosed) 태스크는 크게 3개 출처에 걸쳐 총 66개 단위 과업(총괄 트래킹 이슈 `Dental_000#12` 별도)으로 집계된다:

| 구분 | 세부 출처 | 잔여 건수 | 핵심 성격 |
| :--- | :--- | :---: | :--- |
| 1. GitHub 원격 오픈 이슈 | 18개 저장소 Issues (`Grok` 정적 감사 등록분 56건 중 7건 종결 후 잔여) | 49건 (+ 총괄 `Dental_000#12` 1건) | `[P0]` 3건, `[P1]` 18건, `[P2]` 28건 (데이터 누수 재측정, 가중치 매니페스트, 중앙 테스트 예외 삼킴 제거, macOS MPS 이전, 위생/문서 정합성) |
| 2. 로컬 미종결 기획·감사 문서 | `Dental_000/plans_replies_walkthrough/` 및 `reports/` | 3개 문서 스레드 | `260917_1635` (체어사이드 UAT 대기), `260928_0036` (원본 파노라마 GT 대조 및 불확실 치아 수동 보정 UI), `260928_0312` (무누수 재학습 및 미달 모듈 후속 결정) |
| 3. 서브모듈 내부 미체크(`- [ ]`) 백로그 | `Dental_004`, `Dental_006`, `Dental_014` 내 로그/README | 14개 체크박스 항목 | `Dental_004` 체크박스 미갱신 2건, `Dental_006` 고도화 백로그 8건, `Dental_014` 특이도/형태학 퓨전/XAI 연구 과제 4건 |

---

## 3. 우선순위 `[P0]` 미종결 태스크 상세 (총 4건 — GitHub P0 3건 + 오너 임상 UAT 1건)

### 3.1. `[P0-1]` 가중치 자동 셋업(`setup_env.py`) 복구 및 단일 매니페스트화
- 관련 GitHub 이슈: [Dental_Panoramic_Reader#5](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/5) (`[P0] 가중치 셋업 경로 붕괴: setup_env.py가 존재하지 않는 HF 저장소 11개를 참조, app.py HF 파일명 3건 불일치 — 새 MacBook에서 E2E 재현 불가`)
- 관련 로컬 감사 문서:
  - [261019_1725_Grok_Dental시리즈_기능완성도_점검.md](file:///D:/Github/Dental_000/reports/261019_1725_Grok_Dental시리즈_기능완성도_점검.md#L154-L158)
  - [261019_1725_Grok_Dental시리즈_등록이슈_목록.md](file:///D:/Github/Dental_000/reports/261019_1725_Grok_Dental시리즈_등록이슈_목록.md#L100-L101)
- 대상 소스 코드: [setup_env.py](file:///D:/Github/Dental_Panoramic_Reader/setup_env.py), [app.py](file:///D:/Github/Dental_Panoramic_Reader/app.py), [pipeline.py](file:///D:/Github/Dental_Panoramic_Reader/core/pipeline.py)
- 수행 주체: 랩탑 개발팀 (즉시 수행 가능)
- 현황 및 종결 조건:
  - `app.py`의 HF 경로 3건 불일치 및 `token=True` 강제 문제는 금일 커밋 `adcfddc`에서 선행 해결 완료.
  - `setup_env.py`가 이미 삭제된 구형 HuggingFace 저장소 11개(`chemahc94/dental-cvm`, `dental-yolo` 등, 모두 HTTP 401)를 참조하는 문제를 현행 공개 저장소(`chemahc94/Dental-AI-Models`, `Dental_012`, `Dental_013`, `Dental_014`) 기준으로 개편하고 SHA-256 검증 추가.

### 3.2. `[P0-2]` 중앙 테스트 스위트(`Dental_000/tests`) 예외 삼킴 제거 및 CI 서브모듈 체크아웃
- 관련 GitHub 이슈: [Dental_000#2](https://github.com/HyunchanAn/Dental_000/issues/2) (`[P0] 중앙 테스트 130건 중 85건이 모든 예외(AssertionError 포함)를 삼켜 항상 통과 — 17개 레포 CI 'passing'이 품질을 보증하지 못함`)
- 관련 로컬 기획·감사 문서:
  - [261019_1725_Grok_Dental시리즈_기능완성도_점검.md](file:///D:/Github/Dental_000/reports/261019_1725_Grok_Dental시리즈_기능완성도_점검.md#L96-L100)
  - [261019_1038_Dental_Series_Unclosed_Tasks_and_Discrepancy_Audit_Report.md](file:///D:/Github/Dental_000/reports/261019_1038_Dental_Series_Unclosed_Tasks_and_Discrepancy_Audit_Report.md#L160-L162)
  - [260917_1335_System_Integrity_and_Discrepancy_Remediation_Plan.md](file:///D:/Github/Dental_000/plans_replies_walkthrough/260917_1335_System_Integrity_and_Discrepancy_Remediation_Plan.md)
- 대상 소스 코드: [.github/workflows/reusable-ci.yml](file:///D:/Github/Dental_000/.github/workflows/reusable-ci.yml), `D:\Github\Dental_000\tests\tests_001`~`tests_010`, `tests_panoramic_reader`
- 수행 주체: 랩탑 개발팀 (즉시 수행 가능)
- 현황 및 종결 조건:
  - 금일 `tests_011`~`014`의 더미 스텁 4건은 실체 단위 테스트(10개 케이스)로 개편 완료했으나, `tests_001`~`010` 및 `tests_panoramic_reader` 내 85개 테스트 함수가 여전히 `try: ... except Exception: pass`로 `AssertionError`까지 삼키고 있음.
  - `.github/workflows/reusable-ci.yml`에 `submodules: recursive` 추가 및 `try/except Exception: pass`·`|| echo` 제거.

### 3.3. `[P0-3]` `Dental_008` 검증셋 누수(`data/yolo_fdi` 38장 중복) 지표 정정 및 무누수 분할(507/127) 재학습
- 관련 GitHub 이슈:
  - [Dental_000#1](https://github.com/HyunchanAn/Dental_000/issues/1) (`[P0] data/yolo_fdi 검증셋 38장 전부가 학습셋과 동일(데이터 누수) — Dental_008 대표 지표 99.2%/98.4% 무효`)
  - 연관 `[P1]`: [Dental_008#1](https://github.com/HyunchanAn/Dental_008/issues/1) (`[P1] '무치악 Hard Negative로 FP 100% 억제' 주장 — 학습에 쓴 동일 75장 중 10장으로만 확인, 독립 검증 없음`), [Dental_000#3](https://github.com/HyunchanAn/Dental_000/issues/3) (`[P1] README 성능표가 모듈 README·감사 문서와 불일치`)
- 관련 로컬 기획·감사 문서:
  - [260928_0312_Codex_Dental_Module_Weights_Full_Audit.md](file:///D:/Github/Dental_000/plans_replies_walkthrough/260928_0312_Codex_Dental_Module_Weights_Full_Audit.md#L586-L660)
  - [261019_1038_Dental_Series_Unclosed_Tasks_and_Discrepancy_Audit_Report.md](file:///D:/Github/Dental_000/reports/261019_1038_Dental_Series_Unclosed_Tasks_and_Discrepancy_Audit_Report.md#L114-L115)
  - [261019_1725_Grok_Dental시리즈_기능완성도_점검.md](file:///D:/Github/Dental_000/reports/261019_1725_Grok_Dental시리즈_기능완성도_점검.md#L91-L95)
- 대상 파일: [Dental_000/README.md](file:///D:/Github/Dental_000/README.md), [Dental_008/README.md](file:///D:/Github/Dental_008/README.md), [dental_008_dentex_manifest.csv](file:///D:/Github/Dental_000/reports/dental_008_dentex_manifest.csv)
- 수행 주체: 랩탑 개발팀 (README 누수 수치 즉시 정정) + 메인 워크스테이션 (`RTX 5080`, Train 507 / Val 127 무누수 분할 재학습·재측정)

### 3.4. `[P0-4]` 오너 체어사이드 임상 UAT 및 원본 문제 파노라마 GT 대조 판정
- 관련 로컬 기획·감사 문서:
  - [260917_1635_Canvas_Letterbox_and_Coordinate_Pipeline_Remediation_Plan.md](file:///D:/Github/Dental_000/plans_replies_walkthrough/260917_1635_Canvas_Letterbox_and_Coordinate_Pipeline_Remediation_Plan.md#L359-L374) (`[CONDITIONAL HOLD]`)
  - [260928_0036_Codex_Dental_Repositories_Status_Security_Report.md](file:///D:/Github/Dental_000/reports/260928_0036_Codex_Dental_Repositories_Status_Security_Report.md#L462-L472) (`[기술적 안전 가드 구축 완료 및 임상 UAT 대기]`)
- 수행 주체: 안현찬 총괄 (체어사이드 시각 UAT 승인 및 원본 영상 지정)

---

## 4. 우선순위 `[P1]` 미종결 태스크 상세 (총 19건 — GitHub P1 잔여 18건 + 로컬 UI 과제 1건)

### 4.1. 통합 리더(`Dental_Panoramic_Reader`) 및 `Dental_000` 아키텍처·보안·이식성 (8건)
1. [Dental_Panoramic_Reader#6](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/6) (`[P1] core/interfaces가 저장소 밖 형제 폴더(../../../Dental_00X)를 import하고 ImportError를 무시 — 실패 시 FDI 번호가 전부 0으로 조용히 폴백`):
   - 근거 문서: [261019_1725_Grok_Dental시리즈_기능완성도_점검.md](file:///D:/Github/Dental_000/reports/261019_1725_Grok_Dental시리즈_기능완성도_점검.md#L159-L163), [261019_1038_Dental_Series_Unclosed_Tasks_and_Discrepancy_Audit_Report.md](file:///D:/Github/Dental_000/reports/261019_1038_Dental_Series_Unclosed_Tasks_and_Discrepancy_Audit_Report.md#L59)
   - 대상 파일: `Dental_Panoramic_Reader/core/interfaces/dental_002.py`, `dental_003.py`, `dental_004.py`, `dental_008.py`, `core/pipeline.py`
   - 조치: 저장소 밖 `../../../Dental_00X` 대신 레포 내부 서브모듈 `modules/Dental_00X`를 우선 참조하도록 일원화하고 `ImportError` 시 FDI=0 조용한 폴백 제거.
2. [Dental_Panoramic_Reader#8](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/8) (`[P1] macOS 미지원: BoneLoss 래퍼 'cuda' 하드코딩, ModelManager MPS 미지원, ONNX CoreML 미사용, 로그·설정에 Windows 경로`):
   - 근거 문서: [261019_1725_Grok_Dental시리즈_기능완성도_점검.md](file:///D:/Github/Dental_000/reports/261019_1725_Grok_Dental시리즈_기능완성도_점검.md#L168-L172)
   - 대상 파일: [app.py](file:///D:/Github/Dental_Panoramic_Reader/app.py), [model_manager.py](file:///D:/Github/Dental_Panoramic_Reader/core/model_manager.py), [pipeline.py](file:///D:/Github/Dental_Panoramic_Reader/core/pipeline.py)
3. [Dental_Panoramic_Reader#9](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/9) (`[P1] API 하드닝: 0.0.0.0 바인딩 + CORS '*' + allow_credentials, 인증·업로드 크기 제한 없음, 내부 예외 메시지 반환`):
   - 근거 문서: [261019_1725_Grok_Dental시리즈_기능완성도_점검.md](file:///D:/Github/Dental_000/reports/261019_1725_Grok_Dental시리즈_기능완성도_점검.md#L173-L177)
   - 대상 파일: [api_server.py](file:///D:/Github/Dental_Panoramic_Reader/api_server.py)
   - 조치: 기본 바인딩 `127.0.0.1` (`ALLOW_EXTERNAL_ACCESS=true` 시에만 `0.0.0.0`), `CORS_ORIGINS` 환경변수화, 업로드 파일 크기 제한(20MB) 및 매직바이트 검증, 내부 스택트레이스 노출 차단.
4. [Dental_000#3](https://github.com/HyunchanAn/Dental_000/issues/3) (`[P1] README 성능표가 모듈 README·감사 문서와 불일치(010 '검증 불가'인데 92.4%, 013 아키텍처 상이 등) — 지표 근거 재정리 필요`)
5. [Dental_000#4](https://github.com/HyunchanAn/Dental_000/issues/4) (`[P1] Windows 전용 경로(Y:, D:, C:\Users, UNC 네트워크 공유) 하드코딩 다수 + CUDA 전용 학습 스크립트 — macOS에서 스크립트·테스트·HiTL 도구 실행 불가`)
6. [Dental_000#5](https://github.com/HyunchanAn/Dental_000/issues/5) (`[P1] 전 레포 대상 git add . → commit → push 자동화 스크립트 — 대용량·민감 파일 오커밋 위험`)
7. [Dental_000#6](https://github.com/HyunchanAn/Dental_000/issues/6) (`[P1] DENTEX(CC BY-NC-SA 4.0) 파노라마 409장+라벨을 라이선스 표기 없이 공개 재배포`)
8. [Dental_000#7](https://github.com/HyunchanAn/Dental_000/issues/7) (`[P1] 시리즈 공통: 13개 레포 LICENSE 파일 부재·README 'MIT' 표기 불일치, Hugging Face 가중치(chemahc94/*) 라이선스 미기재`)

### 4.2. 개별 모듈(`[P1]`) 핵심 결함·데이터·법적 리스크 (11건)
9. [Dental_Core#2](https://github.com/HyunchanAn/Dental_Core/issues/2) (`[P1] 설명(DICOM I/O·logging·viz) 대비 실제 구현 부재 — io/ 빈 패키지, logging 없음, 테스트·CI 없음, 실사용은 onnx_exporter뿐`)
10. [Dental_003#5](https://github.com/HyunchanAn/Dental_003/issues/5) (`[P1] api/main.py가 dummy_yolo.pt를 로드하고 랜드마크 생성자 시그니처도 불일치 — FastAPI 서버는 기동 불가 스텁`)
11. [Dental_006#51](https://github.com/HyunchanAn/Dental_006/issues/51) (`[P1] Sci-Hub 폴백·스텔스 브라우저·사용자 Chrome 프로필 공유·EZproxy 경유 다운로드 — 저작권·기관 약관 위반 위험(공개 레포)`)
12. [Dental_006#52](https://github.com/HyunchanAn/Dental_006/issues/52) (`[P1] 저작권 있는 학술 논문 PDF 4편(reference_materials) 공개 레포에 커밋`)
13. [Dental_007#1](https://github.com/HyunchanAn/Dental_007/issues/1) (`[P1] Miniforge3-Linux-x86_64.sh 설치 파일 2개(각 85.8MB) 커밋 — 시크릿 스캐너 오탐 유발, Mac(arm64)에는 무용`)
14. [Dental_008#1](https://github.com/HyunchanAn/Dental_008/issues/1) (`[P1] '무치악 Hard Negative로 FP 100% 억제' 주장 — 학습에 쓴 동일 75장 중 10장으로만 확인, 독립 검증 없음`)
15. [Dental_011#1](https://github.com/HyunchanAn/Dental_011/issues/1) (`[P1] 연령 추정 MAE 0.76년 해석 주의: 정수 연령 라벨(9–19세, 295장), test셋 없이 val로 조기종료·보고, 동일 인물 중복 여부 미확인`)
16. [Dental_013#1](https://github.com/HyunchanAn/Dental_013/issues/1) (`[P1] Dental_000 README의 '31종 YOLOv8-seg 88.5%/84.2%'와 실제 레포(Kaggle 기반 분류기, 감사상 '데이터/라벨 준비 전 보류') 불일치, 테스트 없음`)
17. [Dental_014#2](https://github.com/HyunchanAn/Dental_014/issues/2) (`[P1] 'BRAR-anchored 1,104명' 데이터셋 출처·이용조건·윤리 승인 정보 미기재`)
18. [Dental_015#1](https://github.com/HyunchanAn/Dental_015/issues/1) (`[P1] 앱 초기 화면이 고정 목업 리포트(mockFinalReport)로 시작 — 실추론과 구분되는 상시 DEMO 배너 부재`)
19. [260928_0036 불확실 치아 수동 보정 UI](file:///D:/Github/Dental_000/reports/260928_0036_Codex_Dental_Repositories_Status_Security_Report.md#L470-L472): `uncertain: True`로 플래깅된 치아를 `Dental_015` 화면에서 임상가가 원클릭으로 치식 번호를 수정할 수 있는 인터랙션 구현.

---

## 5. 우선순위 `[P2]` 미종결 태스크 상세 (총 28건 — GitHub P2 잔여 전수)

1. [Dental_000#11](https://github.com/HyunchanAn/Dental_000/issues/11): 미결 상태 정리: 전역 판정 `CONDITIONAL HOLD`·감사 최종 `PASS` 승인 대기 상태와 `v1.0 Release` 배지 불일치
2. [Dental_Panoramic_Reader#10](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/10): 진입점 3중화(`app.py` / `api_server.py` / `core/pipeline.py`)와 `Dental_Core` 미활용 — 모듈 로딩·전처리 로직 중복
3. [Dental_Core#3](https://github.com/HyunchanAn/Dental_Core/issues/3): 위생: `gitleaks.exe`(7.7MB Windows 바이너리)·`egg-info`·`__pycache__` 커밋, `README` UTF-16 인코딩 깨짐, 스크립트 `d:\Github` 하드코딩
4. [Dental_Core#4](https://github.com/HyunchanAn/Dental_Core/issues/4): `ONNXManager`가 CUDA/CPU provider만 선택 — macOS `CoreMLExecutionProvider` 미지원
5. [Dental_001#8](https://github.com/HyunchanAn/Dental_001/issues/8): 라이선스·출처: 원저자 MIT 고지만 존재, GitHub fork 관계 해제, Aariz 파생 이미지 637장(CC BY 4.0) 귀속·변경 고지 필요
6. [Dental_001#9](https://github.com/HyunchanAn/Dental_001/issues/9): macOS 이전: `.env.example` `DEVICE=cuda`, 평가/아카이브 스크립트 CUDA 전용, `tools/inference.py`는 `mps/cpu`만 — 디바이스 처리 불일치
7. [Dental_001#10](https://github.com/HyunchanAn/Dental_001/issues/10): 지표 해석: MRE 3.86px의 `<4.6px (2.0mm)` 환산 근거 불명, CVM 정확도 45.05%인데 `v1.0 Release` 표기
8. [Dental_002#6](https://github.com/HyunchanAn/Dental_002/issues/6): macOS 이전: `data.yaml`(`D:/Github`)·`data_refined.yaml`(`C:/Users`) 절대경로, `malgun.ttf` 폰트, CUDA 전용 학습/추론
9. [Dental_002#7](https://github.com/HyunchanAn/Dental_002/issues/7): 위생: `.coverage`·`logs/test_results.txt`(비 UTF-8, `pytest` 수집 오류 유발)·`archive/scripts` 15개 커밋 (`#4`/`#5` 중복 이슈 종결은 금일 완료)
10. [Dental_003#6](https://github.com/HyunchanAn/Dental_003/issues/6): 데이터 출처 불일치: README는 UFBA-UESC(요청 기반 이용) 표기, `download_dataset.py`는 Zenodo 4457648(별도 데이터셋, CC BY 4.0)
11. [Dental_003#7](https://github.com/HyunchanAn/Dental_003/issues/7): macOS 이전·위생: 학습 스크립트 CUDA 고정, Windows PowerShell 안내, `egg-info` 커밋
12. [Dental_004#10](https://github.com/HyunchanAn/Dental_004/issues/10): `samples/` 웹 수집 파노라마(스톡 워터마크 포함) 출처·라이선스 미기재, Tufts DB 이용약관 확인 필요
13. [Dental_004#11](https://github.com/HyunchanAn/Dental_004/issues/11): SSIM 0.8413을 `높은 구조적 유사도`로 표기(문헌 기준 0.85~0.95 미만), `development_log.txt` 미체크 항목 2건 정리
14. [Dental_005#3](https://github.com/HyunchanAn/Dental_005/issues/3): macOS 이전: `train.py` `device=[0]`, `valid`/`inference` CUDA 전제
15. [Dental_005#4](https://github.com/HyunchanAn/Dental_005/issues/4): AlphaDent(Kaggle 대회) 파생 라벨 211개·`predictions.json`(4.5MB) 커밋 — 대회 데이터 재배포 조건 확인, `egg-info` 추적
16. [Dental_006#53](https://github.com/HyunchanAn/Dental_006/issues/53): macOS 이전: `start_services.bat` 2개(Windows 전용) — GROBID/Ollama 기동 스크립트 `.sh`/`Makefile` 필요
17. [Dental_006#54](https://github.com/HyunchanAn/Dental_006/issues/54): 위생: SQLite DB 4개·로그·`asreview tmp`·`pyc` 커밋, 무관한 `export_onnx.py`, README 배지 `Backend-YOLOv8` 오표기
18. [Dental_006#55](https://github.com/HyunchanAn/Dental_006/issues/55): `Development_log` 미체크 4건(스크리닝 자동화·RoB·Reporting·대규모 테스트)과 closed 이슈 상태 정합성 확인
19. [Dental_007#2](https://github.com/HyunchanAn/Dental_007/issues/2): macOS 이전: WSL2 전제 안내 → `conda-forge` `osx-arm64` `dolfinx` 네이티브 설치로 갱신
20. [Dental_007#3](https://github.com/HyunchanAn/Dental_007/issues/3): README 개요 비어 있음, 해석 검증(해석해/문헌값 비교) 부재, STL·재료 물성 출처 미기재, `gemini.md` 커밋
21. [Dental_008#2](https://github.com/HyunchanAn/Dental_008/issues/2): `edentulous_images` 75장 웹 수집 이미지 — 출처·라이선스 미기재(워터마크 포함), `Thumbs.db` 커밋
22. [Dental_008#3](https://github.com/HyunchanAn/Dental_008/issues/3): macOS 이전: `generate_vis.py`·학습/정리 스크립트에 `C:/Users`·UNC 경로, `device='0'`/`cuda` 고정
23. [Dental_009#1](https://github.com/HyunchanAn/Dental_009/issues/1): 규칙 기반 Winter/Pell-Gregory 분석에 검증 데이터·GT 없음, 테스트 스크립트가 `pytest`에 잘못 수집, `pyc` 커밋
24. [Dental_010#1](https://github.com/HyunchanAn/Dental_010/issues/1): README `검증 불가·릴리스 보류`인데 `v1.0 Release` 배지 — 레포는 38줄 차집합 스텁, 실사용 로직은 리더의 `dental_010_heuristic.py`
25. [Dental_011#2](https://github.com/HyunchanAn/Dental_011/issues/2): README는 `data/ gitignore`라 하지만 데이터 3중 커밋(`zip.zip` 14.8MB + 폴더 2개 591장), `pyc` 추적, CUDA/CPU만 지원
26. [Dental_012#1](https://github.com/HyunchanAn/Dental_012/issues/1): 레포에 추론 코드 없음(데이터 준비·학습만) — 추론은 리더에만 존재, `train.py` `device='cuda'` 고정, `data.yaml` `Y:/` 경로
27. [Dental_014#3](https://github.com/HyunchanAn/Dental_014/issues/3): macOS 이전: 학습·평가·추론 스크립트 6곳 CUDA/CPU만 지원(MPS 없음)
28. [Dental_015#2](https://github.com/HyunchanAn/Dental_015/issues/2): 레포 `description`·`LICENSE`·테스트 없음, `sample_panorama.png` 출처 미기재

---

## 6. 우선순위 `[P3]` 중장기 모델 재설계 및 서브모듈 고도화 백로그 (총 12건)

개별 저장소의 `development_log.txt` 및 `README.md`에 체크박스(`- [ ]`)로 기록되어 있는 중장기 연구·엔지니어링 백로그이다:

### 6.1. `Dental_014` ([Dental_014/README.md](file:///D:/Github/Dental_014/README.md) Future Roadmap 미체크 4건)
1. `- [ ] 특이도(Specificity) 개선`: 정상군(C1) 특이도 17.6% 한계 극복을 위한 클래스 불균형 해소 및 정상 데이터 증강.
2. `- [ ] 형태학적 특징 결합 (Morphological Fusion)`: `morphology_analyzer.py`의 하악 피질골 두께(MCW) 지표를 ViT 임베딩과 결합하여 Mode Collapse 해결.
3. `- [ ] 설명 가능한 AI (XAI) 파이프라인 연동`: Grad-CAM 또는 Attention Map 시각화를 추론 결과와 함께 출력.
4. `- [ ] 최종 목표 지표 달성`: Macro F1 Score 0.70 이상 달성 및 일반화 성능 벤치마크 확립.

### 6.2. `Dental_006` ([Dental_006/development_log.txt](file:///D:/Github/Dental_006/development_log.txt) 고도화 백로그 미체크 8건)
5. `- [ ] README.md 업그레이드` (Installation, Quick Start, Usage, Mermaid 아키텍처 다이어그램, 한계점 명시)
6. `- [ ] 주요 함수 및 클래스에 Google/NumPy 스타일 docstring 작성 및 Type Hints 90% 이상 적용`
7. `- [ ] pydantic-settings 및 .env.example 활용 환경변수/시크릿 관리 일원화`
8. `- [ ] loguru 기반 구조화 로깅(Structured Logging) 도입`
9. `- [ ] PRISMA flow diagram 자동 생성 기능 및 테스트 보강`
10. `- [ ] 합성 데이터(Synthetic Data)를 활용한 End-to-End 통합 파이프라인 테스트 작성`
11. `- [ ] Semantic Versioning (SemVer) 준수 및 CHANGELOG.md 관리 자동화`
12. `- [ ] 의료 도메인 Model Card 및 RoB 평가 정확도/신뢰성 검증 리포트 작성`

---

# [ 261019 2225 랩탑 개발팀 ] P0·P1 즉시 수행 가능 과업(5건 종결 + 1건 문서 정정) 이행 완료 Walkthrough

## 1. 이행 요약
본 마스터 보고서 수립 직후 `랩탑 개발팀`(`RTX4060Laptop-HC`)이 단독으로 즉시 완결 가능한 `[P0]` 및 `[P1]` 최우선 엔지니어링·문서 과업 6건을 선정하여 구현·검증·원격 푸시 및 GitHub 이슈 종결(Close)을 완료하였다.

## 2. 완결 및 종결된 과업 상세
1. `[P0] Dental_Panoramic_Reader#5` (`[CLOSED]`, 커밋 `a55b5d5`):
   - `weights_manifest.yaml` 단일 매니페스트 신설 및 `setup_env.py`(`ensure_weight_file`), `app.py`, `core/interfaces/dental_002.py`, `dental_008.py` 연동 완료.
2. `[P0] Dental_000#2` (`[CLOSED]`):
   - `.github/workflows/reusable-ci.yml`에 `submodules: recursive` 추가 완료.
   - `Dental_000/tests/` 내 37개 파일의 `try: ... except Exception: pass` 및 `def test_dummy_missing_deps(): pass` 예외 삼킴 래퍼를 전수 제거하고 전체 14개 테스트 디렉토리(92개 단위·통합 테스트) 100% 통과(`rc=0`) 검증 완료.
3. `[P0] Dental_000#1` (문서 정정 및 무누수 매니페스트 공시 완료, RTX 5080 재학습 대기, 커밋 `Dental_008@cbe529f`):
   - `Dental_000/README.md` 및 `Dental_008/README.md`에서 누수 검증셋(38장 중복) 기반 `99.2%/98.4%` (`mAP50 0.995`) 지표를 공식 폐기하고 무누수 매니페스트(`reports_archive/dental_008_dentex_manifest.csv`, Train 507 / Val 127, 교집합 0) 및 10례 임상 벤치마크(`10_cases_quantitative_benchmark.json`) 근거로 교체 완료.
4. `[P1] Dental_000#3` (`[CLOSED]`):
   - `Dental_000/README.md` 성능표의 `Dental_003`(`STANDBY`), `Dental_009`(규칙 기반 기하 분석), `Dental_010`(동적 정중선 갭 휴리스틱), `Dental_013`(4대 임상 범주 매핑), `Dental_014`(`OsteoMAENet` 실추론) 설명 및 지표를 실제 구현과 100% 정합화 완료.
5. `[P1] Dental_Panoramic_Reader#6` (`[CLOSED]`, 커밋 `a55b5d5`, `6990f66`):
   - `core/interfaces/` 및 `core/pipeline.py`의 외부 형제 폴더(`../../../Dental_00X`) 참조를 전수 제거하고, `Dental_008` 번호 매칭 실패 시 `FDI_UNAVAILABLE` 상태 전파 및 서브모듈 Git SHA(`imageMetadata.moduleVersions`) 기록 구현 완료.
6. `[P1] Dental_Panoramic_Reader#9` (`[CLOSED]`, 커밋 `a55b5d5`):
   - `api_server.py` 기본 `127.0.0.1` 바인딩(`ALLOW_EXTERNAL_ACCESS=true` 옵션화), `ALLOWED_ORIGINS` 화이트리스트(`allow_credentials=False`), 업로드 크기 30MB·50M 픽셀 제한, 선택적 API 토큰(`DPR_API_TOKEN`) 검증 및 `request_id` 기반 일반화 에러 응답 적용 완료.

## 3. 잔여 통계 갱신
- GitHub 원격 오픈 이슈: 기존 49건 → 39건 (우리 측 5건 `CLOSED` + Grok의 macOS 오등록 5건 `NOT_PLANNED` 종결 반영, 총괄 이슈 `Dental_000#12` 별도)
- `[P0]` 원격 오픈 이슈는 `Dental_000#1`(RTX 5080 무누수 분할 재학습 대기) 단 1건만 남았으며, 코딩·CI·셋업 영역의 `[P0]` 이슈는 전수 해소되었다.

---

# [ 261019 2250 랩탑 개발팀 ] 메인 워크스테이션(RTX 5080) 이관 작업 요청서 — `Dental_000#1` 및 `Dental_008#1` 재학습·검증 마감 요청

- 수신: `메인 워크스테이션` (`RTX5080Desktop-HC` — AMD Ryzen 9 9900X / RTX 5080 16GB / 64GB RAM)
- 발신: `랩탑 개발팀` (`RTX4060Laptop-HC`)
- 대상 이슈:
  - [필수] `Dental_000#1` (`[P0]` `Dental_008` 대표 성능 `99.2%/98.4%`, `mAP50 0.995`가 학습셋과 100% 중복된 검증셋 38장에서 산출된 문제 해결)
  - [권장 동시 처리] `Dental_008#1` (`[P1]` 무치악 Hard Negative 75장을 학습·평가가 공유하던 문제를 학습 60장 / 독립 검증 15장 홀드아웃으로 분리 평가)

## 1. `랩탑 개발팀`에서 사전 준비 완료해 둔 사항 (코드·문서 커밋 및 푸시 완료)
1. 무누수 분할 매니페스트 생성 및 커밋 완료:
   - 경로: `Dental_000/reports_archive/dental_008_dentex_manifest.csv`
   - 내역: DENTEX 전체 634장을 `seed=42` 기준 `train` 507장(80%) / `val` 127장(20%)으로 분할 완료(Train-Val 파일명 교집합 `0건` 검증 완료).
2. 데이터셋 분할 스크립트 패치 완료 (`Dental_008@cbe529f`):
   - 경로: `Dental_008/prepare_yolo_data.py`
   - 내역: 기존 `[:50]` 슬라이싱으로 인해 검증셋이 학습셋과 중복되던 로직을 제거하고, `Dental_000/reports_archive/dental_008_dentex_manifest.csv`를 우선 로드(파일 부재 시에도 `random.Random(42)` 80/20 무누수 분할 보장)하도록 수정 완료.
3. README 누수 수치 폐기 공시 완료 (`Dental_000@200ee1c`, `Dental_008@cbe529f`):
   - `Dental_000/README.md` 및 `Dental_008/README.md`에서 기존 `99.2% / 98.4%` (`mAP50 0.995`) 수치를 공식 폐기하고 `[RTX 5080 무누수 507/127 분할 재학습 대기]` 상태로 공시 완료.

## 2. `메인 워크스테이션`에서 수행해 주실 작업 (순서대로 실행 요청)

### Step 1. 최신 커밋 Pull
- `Dental_000`, `Dental_008`, `Dental_Panoramic_Reader` 저장소에서 각각 `git pull origin main`을 실행하여 위 패치와 매니페스트를 동기화해 주십시오.

### Step 2. 무누수 YOLO 데이터셋 재생성 (`prepare_yolo_data.py`)
- `Dental_008` 디렉터리에서 DENTEX 원본(`quadrant_enumeration/xrays/` 및 `train_quadrant_enumeration.json`)이 준비된 상태로 아래 명령을 실행해 주십시오:
  ```powershell
  python prepare_yolo_data.py
  ```
- 실행 후 `yolo_dataset/images/train`(507장)과 `yolo_dataset/images/val`(127장) 간 파일명 중복이 0건인지 확인해 주십시오.
- [추가 권장 — `Dental_008#1` 동시 해결]: `edentulous_images/`(75장)를 병합할 때 `scripts/prepare_v3_dataset.py`에서 75장 전부를 `train`에 넣지 말고 `60장(train) / 15장(독립 edentulous_val)`으로 분리한 뒤, 학습 완료 후 `scripts/test_on_edentulous.py`로 학습에 사용되지 않은 15장에 대한 False Positive 억제율을 측정해 주시면 `Dental_008#1`도 함께 종결할 수 있습니다.

### Step 3. `YOLOv8m-seg` 무누수 재학습 및 지표 산출 (`train.py`)
- `Dental_008`에서 RTX 5080(`device=0`)으로 100 에포크 재학습을 수행해 주십시오:
  ```powershell
  python train.py
  ```
- 학습 완료 후 무누수 검증셋(Val 127장) 기준 다음 지표를 기록해 주십시오:
  - `Box Precision`, `Box Recall`, `Box mAP@0.5`, `Box mAP@0.5:0.95`
  - `Mask Precision`, `Mask Recall`, `Mask mAP@0.5`, `Mask mAP@0.5:0.95`

### Step 4. 가중치 반영, README 수치 업데이트 및 GitHub 이슈 종결
1. 재학습된 `best.pt`를 `Dental_008/weights/best.pt`에 복사하고, Hugging Face Hub(`chemahc94/Dental-AI-Models` 내 `Dental_008_weights_best.pt`)에 업로드한 뒤 `Dental_Panoramic_Reader/weights_manifest.yaml`의 `dental_008_seg` `sha256` 해시를 갱신해 주십시오.
2. `Dental_000/README.md`(20행) 및 `Dental_008/README.md`(29~33행)의 재학습 대기 문구를 실측된 무누수 `mAP` 지표로 교체하고 커밋·푸시해 주십시오.
3. GitHub 이슈 `Dental_000#1`(및 무치악 홀드아웃 평가 시 `Dental_008#1`)을 `gh issue close`로 닫고, 본 문서 하단에 `# [ yymmdd hhmm 메인 워크스테이션 ]` 서명으로 완료 결과를 남겨 주십시오.
