# [ 261025 1810 랩탑 개발팀 ] (Codex 통합 검토 지적사항 및 GitHub 잔여 이슈 전수 해결 실행 계획서)

## 1. 배경 및 목적

- 원천 보고서: `reports/261025_1751_Codex_Dental_Series_Review.md` (현 상태 정적 검토 보고서로서 `reports/` 폴더에 원형 보존)
- 본 문서는 Codex 통합 검토 보고서에서 도출된 미추적 지적 사항 7건(신규 GitHub 이슈 4건으로 정식 등록 완료)과 원격 GitHub에 이미 열려 있던 기존 이슈 20건(`Dental_000#13` 총괄 이슈 산하 19건)을 합쳐 총 `24건`(총괄 1건 + 세부 23건)의 전체 과업을 통합 관리하고 실행하기 위한 공식 계획서이다.

---

## 2. Codex 검토 지적사항 신규 GitHub 이슈 등록 내역 (4건)

Codex 보고서(`261025_1751`) 3장 및 5장에서 지적된 미추적 잔여 결함 7개 항목을 빠짐없이 추적하기 위해 아래 4건의 신규 GitHub 이슈를 생성하고 총괄 이슈(`Dental_000#13`)에 정식 연결하였다.

| 신규 이슈 번호 | 우선순위 | 제목 및 핵심 해결 범위 | 대응하는 Codex 지적 항목 |
| :--- | :--- | :--- | :--- |
| [Dental_Panoramic_Reader#17](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/17) | P1 | `[P1] 헬스체크(/api/v1/health) 실제 모듈 로드 상태(readiness) 검증 및 전체 상태 연동` | 3장 P1-1 (`os.path.exists` 기반 `ONLINE` 및 고정 `HEALTHY` 탈피, `configured`/`loaded`/`ready` 분리) |
| [Dental_Panoramic_Reader#18](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/18) | P1 | `[P1] 리포트 patientId 고정값(PATIENT-DEMO) 제거 및 미실행 모듈과 특이소견 없음 구분` | 3장 P1-2 (`PATIENT-DEMO` 고정 식별자를 `ANON-<sha256[:8]>`로 전환) 및 P2-1 (`summary_parts` 빈 결과 시 미실행/오류 모듈 분리 표기) |
| [Dental_Panoramic_Reader#19](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/19) | P2 | `[P2] Dental_011(연령 추정) 모듈의 FastAPI 파이프라인·SSOT 리포트·문서 연동 정합성 확보` | 3장 P2-5 (`Dental_Panoramic_Reader/README.md` 및 `app.py`와 `core/pipeline.py` -> `api_server.py` -> `Dental_015` 간 `Dental_011` 범위 일치화) |
| [Dental_000#16](https://github.com/HyunchanAn/Dental_000/issues/16) | P2 | `[P2] 중앙 README 벤치마크 JSON 경로, Dental_013 검출률 분모(4/4 Any-hit vs 객체 Recall), Dental_Core 서브모듈 설명 정정` | 3장 P2-2 (`plans_replies_walkthrough/10_cases_quantitative_benchmark.json` 경로 정정), P2-3 (`Dental_013` 4/4 사례 검출률 vs 인스턴스 Recall 병기), P2-4 (`Dental_Core` 간접 서브모듈 구조 명시) |

---

## 3. 전체 열린 GitHub 이슈 통합 목록 및 실행 우선순위 (총 24건: 총괄 1건 + 세부 23건)

총괄 트래킹 이슈: [Dental_000#13](https://github.com/HyunchanAn/Dental_000/issues/13) (`[총괄] Dental 시리즈 CI 복구·테스트·Reader 웹 공개 준비`)

### [Track 1 — 1순위 (최우선 선행)] `Dental_Core` 의존성 및 원격 CI 복구
하위 저장소들의 CI 실패 원인이 공통 패키지인 `Dental_Core`와 직결되어 있으므로 가장 먼저 복구한다.
1. [Dental_Core#5](https://github.com/HyunchanAn/Dental_Core/issues/5): `[CI] 실패 중인 CI 복구`
   - 실행 내용: 원격 GitHub Actions 실패 로그 조회(`gh run view`), 의존성/테스트 설정 수정 후 `main` 브랜치 원격 CI 녹색(`success`) 통과 확인.

### [Track 2 — 2순위 (P1 차단급)] `Dental_Panoramic_Reader` 보안·개인정보·헬스체크·리포트 무결성 통합 개편
`api_server.py` 및 `core/pipeline.py`를 수정할 때 기존 보안/개인정보 이슈 2건과 Codex 신규 P1/P2 이슈 3건을 한 번에 묶어 리팩토링한다.
2. [Dental_Panoramic_Reader#14](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/14): `[보안·차단] DPR_API_TOKEN 미설정 시 인증 없이 열리는 문제(fail-open) 수정 + CORS 설정`
   - 실행 내용: 인증 토큰 미설정 시 fail-closed(HTTP 401/503 차단 또는 로컬 전용 명시 모드 분리) 적용 및 명시적 허용 출처(`CORS_ORIGINS`) 설정.
3. [Dental_Panoramic_Reader#16](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/16): `[개인정보] 웹 공개 전 업로드 영상 처리 기준`
   - 실행 내용: `api_server.py`에서 `temp_{filename}` 디스크 파일 생성을 전면 제거하고 순수 메모리(`BytesIO` / `cv2.imdecode`) 스트림으로 처리하며, DICOM 입력 시 `dental_core.io.dicom.strip_phi_tags`를 강제 호출하도록 구현.
4. [Dental_Panoramic_Reader#17](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/17): `[P1] 헬스체크(/api/v1/health) 실제 모듈 로드 상태(readiness) 검증 및 전체 상태 연동`
   - 실행 내용: 모듈별 상태를 `configured`, `loaded`, `ready`로 세분화하고, 파이프라인 초기화/모델 로드 상태를 반영하여 필수 모듈 장애 시 최상위 상태를 `DEGRADED`/`UNHEALTHY`로 반환.
5. [Dental_Panoramic_Reader#18](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/18): `[P1] 리포트 patientId 고정값(PATIENT-DEMO) 제거 및 미실행 모듈과 특이소견 없음 구분`
   - 실행 내용: 업로드 추론 시 `patientId`를 `ANON-{sha256[:8]}`로 생성하고, 모듈별 실행 상태(`moduleStatus`)를 리포트에 기록하여 미실행/보류 모듈 존재 시 `"특이 소견 없음"` 대신 `"평가 불완전(일부 모듈 미실행 포함)"`을 구분 표기.
6. [Dental_Panoramic_Reader#19](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/19): `[P2] Dental_011(연령 추정) 모듈의 FastAPI 파이프라인·SSOT 리포트·문서 연동 정합성 확보`
   - 실행 내용: `core/pipeline.py`, `api_server.py`, `Dental_015` 리포트 및 `Dental_Panoramic_Reader/README.md` 간 `Dental_011` 연동 범위 일치화.

### [Track 3 — 3순위 (P1)] 나머지 9개 저장소 원격 GitHub Actions CI 복구
`Dental_Core#5` 해결 직후 각 저장소의 원격 Actions 실패 로그를 분석해 전수 `success`로 복구한다.
7. [Dental_000#14](https://github.com/HyunchanAn/Dental_000/issues/14): `[CI] 실패 중인 CI 복구`
8. [Dental_007#4](https://github.com/HyunchanAn/Dental_007/issues/4): `[CI] 실패 중인 CI 복구`
9. [Dental_009#2](https://github.com/HyunchanAn/Dental_009/issues/2): `[CI] 실패 중인 CI 복구`
10. [Dental_010#2](https://github.com/HyunchanAn/Dental_010/issues/2): `[CI] 실패 중인 CI 복구`
11. [Dental_011#3](https://github.com/HyunchanAn/Dental_011/issues/3): `[CI] 실패 중인 CI 복구`
12. [Dental_012#2](https://github.com/HyunchanAn/Dental_012/issues/2): `[CI] 실패 중인 CI 복구`
13. [Dental_013#2](https://github.com/HyunchanAn/Dental_013/issues/2): `[CI] 실패 중인 CI 복구`
14. [Dental_014#4](https://github.com/HyunchanAn/Dental_014/issues/4): `[CI] 실패 중인 CI 복구`
15. [Dental_Panoramic_Reader#12](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/12): `[CI] 실패 중인 CI 복구`

### [Track 4 — 4순위 (P2)] 개별 레포지토리 기본·스모크 테스트 추가 및 CI 연동
16. [Dental_002#8](https://github.com/HyunchanAn/Dental_002/issues/8): `[테스트] 기본 테스트 추가`
17. [Dental_003#8](https://github.com/HyunchanAn/Dental_003/issues/8): `[테스트] 기본 테스트 추가`
18. [Dental_011#4](https://github.com/HyunchanAn/Dental_011/issues/4): `[테스트] 기본 테스트 추가`
19. [Dental_Panoramic_Reader#13](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/13): `[테스트] 기본 테스트 추가` (Track 2의 보안·인메모리·readiness·patientId 검증 테스트 포함)

### [Track 5 — 5순위 (P2)] 컨테이너 빌드 및 웹 조회용 배포 파이프라인 정비
20. [Dental_001#11](https://github.com/HyunchanAn/Dental_001/issues/11): `[배포] GHCR 이미지 빌드·배포 워크플로 실패 수정`
21. [Dental_Panoramic_Reader#15](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/15): `[배포] 웹 조회용 배포 준비 (의존성·Dockerfile·비공개 Space)`

### [Track 6 — 6순위 (P2)] 중앙·모듈 문서 정합성 및 라이선스·샘플 마감 점검
22. [Dental_000#16](https://github.com/HyunchanAn/Dental_000/issues/16): `[P2] 중앙 README 벤치마크 JSON 경로, Dental_013 검출률 분모(4/4 Any-hit vs 객체 Recall), Dental_Core 서브모듈 설명 정정`
23. [Dental_000#15](https://github.com/HyunchanAn/Dental_000/issues/15): `[라이선스] 비상업 연구용 고지와 데이터 출처 표기, 공개 화면 샘플 정리`

---

## 4. 진행 상태

- 상태: `[IN PROGRESS]` — 신규 이슈 4건 등록 및 마스터 이슈(`Dental_000#13`) 연결 완료, Track 1~6 순차 실행 대기.
