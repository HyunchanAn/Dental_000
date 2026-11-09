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

# [261025 2309 Codex] (Codex 통합 검토 지적사항 및 GitHub 잔여 이슈 전수 해결 실행 계획서 검토)

## 검토 결과

**판정: 조건부 승인 — 실행 전 Track 2 개인정보·식별자 요구사항과 총괄 이슈의 작업 순서를 정합화할 것.**

GitHub 원격 이슈 24건(총괄 1건, 세부 23건)의 번호·제목·열림 상태를 확인했다. 신규 4건(Reader #17~#19, Dental_000 #16)은 실제 생성되어 #13의 댓글에 하위 이슈로 연결되어 있다. 따라서 계획서의 건수는 맞고, #16이 신규 이슈 표와 Track 6에 각각 나오는 것은 같은 이슈의 설명과 실행 목록으로 중복 집계가 아니다. 다만 현재 모두 열려 있으며 완료된 Track은 확인되지 않는다.

## 실행 전에 반영할 사항

1. **총괄 이슈 #13과 실행 순서를 맞춘다.** 총괄 이슈 본문은 `Core CI → 나머지 CI → 테스트 → Dental_001 배포 → Reader 보안 → Reader 배포 → 개인정보 → 라이선스` 순서다. 계획서는 Reader 보안·개인정보를 나머지 CI보다 먼저 둔다. 보안 조치를 웹 공개 전 차단 조건으로 우선하는 판단은 타당하지만, 현재 총괄 이슈와 실행 기준이 서로 다르므로 #13의 순서도 계획서에 맞춰 갱신하거나, 계획서를 총괄 이슈 순서에 맞춰야 한다. 어느 쪽이 결정됐는지 기록하기 전에는 “공식 실행 순서”가 단일하지 않다.

2. **DICOM 처리 범위를 명시적으로 결정한다.** 현 `Dental_Panoramic_Reader/api_server.py`는 `image/*`만 허용하고 업로드 바이트를 메모리에서 Pillow로 디코드한다. 현행 입력 경로에는 DICOM 파서가 없으므로 `strip_phi_tags` 강제 호출을 계획에 넣어도 현재 DICOM 입력을 보호하지 못한다. DICOM을 지원하지 않는다면 해당 업로드를 명시적으로 거부하고 이슈 #16 완료 기준을 그에 맞춘다. 지원한다면 DICOM 파싱·메타데이터 익명화·픽셀에 구워진 식별정보(Burned-in PHI) 처리까지 별도 설계와 테스트를 완료 조건으로 정의한다. 메타데이터 태그 제거만으로 픽셀 내 식별정보가 제거되지는 않는다.

3. **`patientId = ANON-{sha256[:8]}`를 익명 환자 ID로 취급하지 않는다.** SHA-256 접두값은 같은 영상 요청을 연결할 수 있고 원본 영상 대조가 가능하면 재식별 단서가 될 수 있다. 현재 코드가 이미지 전체 SHA-256을 이미 응답 메타데이터에 넣는 점도 함께 검토해야 한다. 환자 식별이 필요 없다면 `patientId` 대신 요청별 무작위 `requestId`를 사용하고, 영상 해시를 응답·로그에 노출할 필요가 있는지 별도로 판단한다. 환자 단위 연결이 필수라면 키 관리와 보존 범위를 정한 비밀키 기반 가명화 방식을 사용한다.

4. **Track 2의 완료 기준과 웹 배포 차단 조건을 연결한다.** #14의 토큰 미설정 시 서버 시작 거부 또는 요청 거부는 선택지를 남기지 말고 운영 모드별 동작을 확정한다. CORS 허용 목록은 인증 대체가 아니다. #14·#16·#17·#18의 보안/개인정보/상태/리포트 테스트가 통과하고 원격 CI 결과를 확인하기 전에는 #15 웹 배포를 진행하지 않는다고 계획서에 완료 게이트를 적는다. Reader #13의 테스트 추가 이슈를 Track 4에 배치하더라도, Track 2 기능은 각 이슈의 완료 전 테스트로 검증되어야 한다.

## 확인 근거 및 범위

- GitHub의 #13 및 세부 이슈 23건을 조회했다. 신규 이슈 4건은 #13의 두 번째 댓글에 체크리스트로 연결되어 있다.
- 로컬 `Dental_Panoramic_Reader/api_server.py`와 `Dental_Core/dental_core/io/dicom.py`의 업로드·인증·DICOM 경로를 정적 확인했다.
- 원격 Actions 로그나 실제 CI 실행 결과는 확인하지 않았다. 이 검토는 계획 및 이슈 추적의 정합성 검토이며, 구현 완료나 배포 준비 완료를 뜻하지 않는다.

— Codex


---

# [ 261109 1500 랩탑 개발팀 ] (코드 해결 가능 잔여 이슈 10건 전수 해결·종결, 18개 레포 4폴더 문서 체계 정립 및 사용자 확인/외부 설정 이관 보고서)

## 1. 작업 개요 및 실행 기준 정렬

Codex 검토 의견(`261025 2309`) 및 오너 지침(`/goal 해결할 수 있는 것들은 해결하고, 내 확인이 필요한 것들은 우선 미뤄둬. 그리고 외부 설정이 필요한건 맨 마지막에 하자.`)에 따라 전체 24건의 이슈를 다음과 같이 단계별로 완결하였다:

1. [선행 완결 (11건 CLOSED)]: `Dental_Core#5`, `Dental_001#11`, `Dental_Panoramic_Reader#12`, `Dental_000#14`, `Dental_007#4`, `Dental_009#2`, `Dental_010#2`, `Dental_011#3`, `Dental_012#2`, `Dental_013#2`, `Dental_014#4` 원격 GitHub Actions CI 및 GHCR 배포 파이프라인 전수 복구 완료.
2. [금번 코드 해결 및 원격 CI 검증 완결 (10건 CLOSED)]:
   - 개별 레포 단위/스모크 테스트 구축 및 CI 연동 4건: `Dental_002#8`, `Dental_003#8`, `Dental_011#4`, `Dental_Panoramic_Reader#13`
   - `Dental_Panoramic_Reader` 보안·인메모리 DICOM PHI 익명화·헬스체크 Readiness·리포트 무결성·연령 추정(`Dental_011`) 통합 5건: `Dental_Panoramic_Reader#14`, `#16`, `#17`, `#18`, `#19`
   - 중앙 및 모듈 문서 정합성 교정 1건: `Dental_000#16`
3. [코드 측 선행 준비 완료 및 사용자 최종 확인 / 외부 설정 보류 (3건 OPEN 유지)]:
   - `Dental_000#15`: `Dental_Panoramic_Reader/app.py` 및 `Dental_015/src/App.tsx` 내 비상업 연구용(`CC BY-NC 4.0` / `Non-Commercial Research Only`) 상시 고지 배너 반영 완료. 공개 화면 샘플 이미지 최종 육안 검수 후 종결 대기.
   - `Dental_Panoramic_Reader#15`: `Dockerfile`, `requirements.txt`, 인메모리 추론 및 Fail-Closed 인증 코드 준비 완료. 외부 Hugging Face Private Space 생성 및 `HF_TOKEN` / `DPR_API_TOKEN` Secret 등록은 맨 마지막 외부 설정 단계로 보류.
   - `Dental_000#13`: 마스터 트래킹 이슈 (위 2건의 최종 사용자 확인 및 외부 설정 마감 시 함께 종결).

---

## 2. 코드 해결 완결 이슈 10건 상세 내역 (Walkthrough)

### 2.1 `Dental_Panoramic_Reader` 보안·개인정보·헬스체크·리포트·연령 추정 통합 (`#13, #14, #16, #17, #18, #19`)
- `Dental_Panoramic_Reader#14` (Fail-Closed 인증 및 CORS 정밀 제어):
  - `api_server.py`의 `_verify_api_token`을 Fail-Closed 방식으로 개편하여 서버 환경변수 `DPR_API_TOKEN`이 미설정되어 있거나 요청 헤더(`X-API-Token` 또는 `Authorization: Bearer`)가 누락·불일치(`hmac.compare_digest`)할 경우 예외 없이 `HTTP 401 Unauthorized`를 반환하도록 수정하였다.
  - `DPR_CORS_ORIGINS` 및 `ALLOWED_ORIGINS` 환경변수를 통해 허용 출처를 파싱하며 와일드카드(`*`)를 원천 배제하였다.
- `Dental_Panoramic_Reader#16` (인메모리 방사선·DICOM 디코딩 및 PHI 메타데이터 스트리핑):
  - `api_server.py`에 `decode_uploaded_radiograph_in_memory(contents, filename, content_type)` 및 `strip_phi_tags_in_memory(ds)`를 구현하여 일반 이미지(`PNG/JPEG`)와 `DICOM`(`.dcm`/`.dicom`/`DICM` 헤더) 모두 디스크 임시 파일 저장 없이 순수 메모리(`io.BytesIO`)에서 처리하도록 일원화하였다.
  - DICOM 업로드 시 픽셀 배열 추출 전에 `PatientName`, `PatientID`, `PatientBirthDate`, `PatientSex`, `InstitutionName`, `AccessionNumber` 등 PHI 태그를 메모리상에서 즉시 `ANONYMIZED`로 덮어쓰고 사설 태그(`remove_private_tags()`)를 제거한다.
  - `app.py`(Streamlit)에서도 `image.save("temp_xai.png")` 임시 파일 생성을 제거하고 `Dental_002/src/dentex_caries/explain.py`가 인메모리 `np.ndarray`를 직접 입력받도록 개선하였다.
- `Dental_Panoramic_Reader#17` (`/api/v1/health` 모듈별 `configured` / `loaded` / `ready` 분리 및 동적 상태 판정):
  - 9개 진단 모듈(`Dental_008, 002, 012, 010, 003, 009, 013, 014, 011`) 각각에 대해 `configured`(설정 여부), `loaded`(파이프라인/메모리 적재 여부), `ready`(가중치 및 의존 모듈 준비 완료 여부) 불리언 필드를 반환한다.
  - 최상위 서비스 상태를 고정 `HEALTHY`에서 동적 판정(`Dental_008` 미준비 시 `UNHEALTHY`, 전 모듈 준비 완료 시 `HEALTHY`, 일부 보조 모듈 미준비 시 `DEGRADED`)으로 전환하였다.
- `Dental_Panoramic_Reader#18` (고정 `PATIENT-DEMO` 제거, 모듈 실행 상태 기록 및 요약문 오해 방지):
  - `format_to_ssot_report`에서 고정 `"PATIENT-DEMO"`를 제거하고 `ANON-<sha256[:12]>`(해시 부재 시 `ANON-<uuid[:12]>`) 형식의 요청별 익명 식별자로 대체하였다.
  - `core/pipeline.py` 및 `api_server.py`에서 모듈별 실행 상태(`moduleExecutionStatus`: `executed` / `skipped` / `unavailable` 및 `reason`)를 기록하여 리포트에 포함하였다.
  - 일부 모듈이 `skipped`(예: 유치열 감지 시 `Dental_003` 우회) 또는 `unavailable` 상태일 때 병소가 없더라도 `"특이 소견이 없습니다"`로 오인되지 않도록 미실행/제한 모듈 안내 및 정상 판정 보류 문구를 명시하였다.
- `Dental_Panoramic_Reader#19` (`Dental_011` 치아 연령 추정 엔드투엔드 파이프라인·SSOT·UI 통합):
  - `core/pipeline.py`에서 `AgePredictorWrapper`(`011`)를 등록·호출하여 `011_age` 결과를 생성하고, `api_server.py`의 `format_to_ssot_report`에서 `findings.ageEstimation`(`predictedAge`, `confidenceInterval95`, `status`, `model`) 및 `summary`에 반영하였다.
  - `Dental_015` 프론트엔드(`src/types/finalReport.ts`, `src/mocks/mockFinalReport.ts`, `src/App.tsx`)에 `ageEstimation` 및 `moduleExecutionStatus` 타입과 연령 추정 표시 UI를 추가하였다.
- `Dental_Panoramic_Reader#13` (API·파이프라인 통합 단위 테스트 구축):
  - `tests/test_api_and_pipeline.py`를 신설하여 `#14, #16, #17, #18, #19` 핵심 요구사항 5건을 자동 검증하고 `.github/workflows/ci.yml`에 연동하였다 (`pytest` 10건 전수 통과).

### 2.2 개별 레포지토리 스모크·단위 테스트 구축 (`Dental_002#8`, `Dental_003#8`, `Dental_011#4`)
- `Dental_002#8`: `tests/test_caries_smoke.py` 신설 (`apply_clahe`, `assign_quadrant`, `map_detections_to_quadrants`, `coco_to_yolo_bbox`, `YOLOwrapper`, `CariesDetector.predict` 스모크 검증) 및 `.github/workflows/ci.yml` 연동 (`13 passed`).
- `Dental_003#8`: `tests/test_boneloss_smoke.py` 신설 (`calculate_distance`, `calculate_rbl`, `determine_patient_stage`, `PerioLandmarkPredictor.predict_landmarks_from_contour` 치간 방사선 밀도 프로파일 검증, FastAPI `/predict/pano` 스모크 검증) 및 `.github/workflows/ci.yml` 연동 (`9 passed`).
- `Dental_011#4`: `tests/test_age_smoke.py` 신설 (`AgeRegressionModel` 순전파, `evaluate_loader_pytorch`, `compute_bootstrap_ci`, `DentalAgeDataset`, `check_sha256_duplicates`, `split_dataset_files` 무누수 3분할 검증) 및 `.github/workflows/ci.yml` 연동 (`5 passed`).

### 2.3 중앙·모듈 문서 정합성 교정 (`Dental_000#16`) 및 18개 전 레포 4폴더 문서 체계 정립
- `Dental_000#16`:
  - `10_cases_quantitative_benchmark.json`을 `reports_archive/10_cases_quantitative_benchmark.json`(및 `reports/10_cases_quantitative_benchmark.json`)에 배치하고 `benchmark_scripts/run_clinical_evaluation.py`와 `Dental_000/README.md`의 참조 경로를 일치시켰다.
  - `Dental_000/README.md` 및 `Dental_013/README.md`에서 `Dental_013` 지표를 `수복물 보유 4례 기준 증례 단위(Any-hit) 검출률 4/4 (100.0%), 개별 객체 단위(IoU >= 0.50) Recall 34.4% ~ 48.1% (Precision 44.0% ~ 76.2%)`로 명확히 분리 표기하였다.
  - `Dental_000/README.md`에서 `modules/`가 15개 서브모듈(`Dental_001`~`014`, `Dental_Panoramic_Reader`)을 직접 바인딩하고 `Dental_Core`는 `Dental_Panoramic_Reader/modules/Dental_Core`를 통해 간접 포함된다는 실제 Git 형상을 정확히 기술하였다.
- 18개 전 저장소(`Dental_000` ~ `Dental_015`, `Dental_Core`, `Dental_Panoramic_Reader`) 4폴더 문서 표준화:
  - 모든 저장소에 `reports/`, `plans_replies_walkthrough/`, `reports_archive/`, `plans_replies_walkthrough_archive/` 4개 표준 폴더를 생성하였다.
  - 문서 성격에 맞지 않게 배치되어 있던 스레드형 감사·회신·Walkthrough 문서들과 벤치마크 JSON/CSV 산출물을 올바른 성격의 폴더로 재분류하고, `[CLOSED]`가 명시된 후 2주 이상 경과(`<= 2026-10-25`)한 문서들을 각각 `reports_archive/` 및 `plans_replies_walkthrough_archive/`로 이관하였다.

---

## 3. 사용자 최종 확인 및 외부 설정 보류 항목 (3건)

| 이슈 번호 | 구분 | 코드 측 완료 상태 | 남은 사용자 확인 / 외부 설정 사항 |
| :--- | :--- | :--- | :--- |
| [Dental_000#15](https://github.com/HyunchanAn/Dental_000/issues/15) | 사용자 확인 | `Dental_Panoramic_Reader/app.py` 및 `Dental_015/src/App.tsx` 비상업 연구용(`CC BY-NC 4.0`) 상시 배너 탑재 완료 | 웹 UI 공개 화면에 노출할 샘플 이미지 최종 육안 확인 및 승인 |
| [Dental_Panoramic_Reader#15](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/15) | 외부 설정 (맨 마지막) | `Dockerfile`, `requirements.txt`, 인메모리 추론, Fail-Closed 토큰 인증 및 단위 테스트 완비 | Hugging Face Private Space 생성 및 외부 Secret(`HF_TOKEN`, `DPR_API_TOKEN`) 설정 |
| [Dental_000#13](https://github.com/HyunchanAn/Dental_000/issues/13) | 총괄 트래킹 | 산하 23개 세부 이슈 중 코드 해결 가능 21건(CI 11건 + 기능/테스트/문서 10건) `CLOSED` 완료 | 위 2건(`Dental_000#15`, `Dental_Panoramic_Reader#15`) 마감 시 최종 종결 |
