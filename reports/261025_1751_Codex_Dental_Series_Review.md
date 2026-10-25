# [261025 1751 Codex] (Dental 시리즈 통합 검토 보고서)

## 1. 검토 개요

- 검토 일시: 2026-10-25 17:51 KST
- 대상: `D:\Github`의 Dental 시리즈 18개 저장소 (`Dental_000`~`Dental_015`, `Dental_Core`, `Dental_Panoramic_Reader`)
- 검토 범위: 각 저장소 README의 제목·기본 구조 및 로컬 Git 상태, `Dental_000`의 시리즈 감사/라이선스/미종결 과업 문서, 두 통합 저장소의 submodule 포인터, Reader의 API 상태/보고 생성 및 주요 모듈 호출 경로, 감사 JSON의 최신 변경 사항, 관련 원격 GitHub 이슈 검색 및 선택 이슈 상태/종결 코멘트
- 검토 방식: 로컬 파일 정적 대조 및 GitHub 관련 키워드 open 검색·선택 이슈 조회. 테스트·서버 실행·임상 검증·CI/Hugging Face 상태 확인은 수행하지 않음.

## 2. 요약

시리즈의 로컬 형상은 정돈되어 있습니다. 검토 보고서를 추가하기 전 18개 저장소 모두 `main` 브랜치였고 작업 트리는 clean이었으며, `Dental_000` 및 `Dental_Panoramic_Reader`에 기록된 직접 submodule 포인터는 로컬 체크아웃 커밋과 일치했습니다. 앞선 가중치 감사의 미달 IoU 연결 정보도 최신 JSON에 추가되어, 해당 지적은 해소된 것을 확인했습니다.

남은 주요 문제는 통합 API의 상태 표현과 중앙 문서의 추적성입니다. 특히 API 헬스체크가 가중치 파일 존재만으로 일부 모듈을 `ONLINE`으로 표시하고 전체 응답을 `HEALTHY`로 반환하며, 생성 리포트의 `patientId`가 모든 요청에서 고정 문자열입니다. 중앙 README의 벤치마크 JSON 경로는 실제 파일 위치와 다릅니다. 이는 코드의 현재 로컬 동작/내용에 대한 정적 확인이며, 서버가 현재 실제 구동 중이라거나 임상 사용 준비가 검증됐다는 뜻은 아닙니다.

## 3. 발견 사항

### P1 — 헬스체크가 실제 모듈 준비 상태를 보증하지 않음

`Dental_Panoramic_Reader/api_server.py`는 `has_003`, `has_012`, `has_013`, `has_014`를 주로 가중치 경로의 `os.path.exists()`로 정하고, 그 결과로 `ONLINE`/`STANDBY`/`MOCK`을 구성합니다. 같은 헬스체크의 전체 서비스 상태는 모듈 상태와 별개로 고정값 `HEALTHY`를 반환합니다. 따라서 가중치 파일은 존재하지만 로드·초기화·추론이 실패한 환경에서도 API가 준비 완료로 보일 수 있습니다. 현재 체크아웃에 주요 가중치 파일이 있다는 사실은 확인했지만 실제 로드/추론은 실행하지 않았습니다.

**권고:** 상태를 `configured`(파일/설정 존재), `loaded`(모델 초기화 성공), `ready`(간단한 입력 계약 또는 추론 확인)로 분리하고, 필수 모듈의 실패를 전체 readiness에 반영하십시오. README의 `8/8 ONLINE`은 런타임 health 결과 또는 검증 시점과 연결해 표현하십시오.

### P1 — API 리포트의 환자 식별자가 모든 요청에서 동일

`Dental_Panoramic_Reader/api_server.py`의 리포트 생성기는 요청 이미지와 관계없이 `patientId: "PATIENT-DEMO"`를 씁니다. 현재는 데모/placeholder 성격이 코드에서 분명하지만, 실제 업로드 경로에서 나온 리포트에도 그대로 붙으면 여러 이미지 리포트가 같은 환자 식별자처럼 보입니다. 기록 연결과 추적에서 오해가 생길 수 있습니다.

**권고:** 환자 식별자를 입력받지 않는 연구용 API라면 이 필드를 제거하거나 명시적인 익명 요청 ID로 대체하고, 스키마에서 데모 placeholder임을 구분하십시오. 임상 연동을 의도한다면 인증된 요청 메타데이터에서 전달·검증하도록 설계하고, 누락 시 추론 리포트를 생성하지 않도록 하십시오.

### P2 — 결과가 비어 있을 때 “특이 소견 없음”과 “평가 불가”가 구분되지 않음

같은 API는 `summary_parts`가 비어 있으면 `분석 결과 특이 소견이 없습니다.`를 반환합니다. 하지만 모듈 결과 일부는 `None`, `NOT_AVAILABLE`, 건너뜀 상태일 수 있으므로 결과가 비었다는 사실만으로 모든 대상 모듈이 정상 평가를 마쳤다고 해석할 수 없습니다.

**권고:** 모듈별 실행 상태/실패 사유를 결과에 포함하고, 전체 평가가 성공했을 때만 “특이 소견 없음”을 사용하십시오. 일부 미실행·오류가 있으면 “평가 불완전”을 별도로 표시하십시오.

### P2 — 중앙 README의 벤치마크 JSON 링크 경로가 실제 파일과 다름

`Dental_000/README.md`는 최신 성적표 근거를 `reports_archive/10_cases_quantitative_benchmark.json`으로 가리키지만 해당 경로에는 파일이 없습니다. 현재 JSON은 `plans_replies_walkthrough/10_cases_quantitative_benchmark.json`에 있습니다. README의 링크를 현재 위치로 고치거나, 의도한 아카이브 위치에 기준본을 두고 단일 기준 경로를 문서화해야 합니다.

### P2 — Dental_013 “검출률 100%” 지표의 의미를 중앙 표에서 한정할 필요

`Dental_013/README.md`는 이를 `Case-level Detection Rate`로 정의하고 수복물 전용 3건과 복합 사례 1건, 총 4건 모두에서 적어도 하나의 수복물을 찾았다고 설명합니다. 따라서 제시한 100%는 `4/4` 사례 단위(any-hit) 비율이지, 전체 10례 또는 수복물 객체 재현율이 아닙니다. 같은 README에 보고된 세 케이스의 인스턴스 Recall은 34.4%, 42.1%, 48.1%입니다. 반면 `Dental_000/README.md` 표는 이를 “10례 정량 벤치마크 검출률 100.0%”라고 표기하고, Dental_013 README도 섹션을 “10대 임상 케이스”로 부르면서 4건만 제시해 모집단과 분모가 맞지 않습니다.

**권고:** 모집단을 실제 계산에 사용한 4건으로 명시하고, 지표명을 `사례 단위(any-hit) 검출률 4/4`로 고치십시오. 중앙 요약에는 인스턴스 Precision/Recall(별도 분모)을 함께 제시하고, 전체 10례 평가라고 주장하려면 해당 10개 입력 각각의 수복물 정답 및 상세 판정을 추가하십시오.

### P2 — 중앙 README의 Dental_Core 직접 submodule 설명이 형상과 다름

`Dental_000/README.md`는 `modules/`가 `Dental_Core`를 포함한 Git submodule 바인딩이라고 설명합니다. 그러나 `.gitmodules`와 `HEAD:modules`에는 `Dental_001`~`Dental_014` 및 `Dental_Panoramic_Reader`만 직접 등록되어 있고 `Dental_Core`는 없습니다. `Dental_Core`는 Reader 저장소 안에 별도 submodule로 연결되어 있습니다.

**권고:** `Dental_Core`가 Reader를 통해 간접 포함된다는 구조를 README에 반영하거나, 중앙 저장소에서 직접 관리할 의도라면 실제 submodule을 추가하십시오.


### P2 — Dental_011의 파이프라인 연동 여부가 README와 구현에서 다름

`Dental_Panoramic_Reader/README.md`의 E2E 데이터 흐름 그림은 `Dental_008`에서 `Dental_011: Age Prediction`으로 연결해 최종 리포트로 보내는 것으로 표시합니다. 실제 `app.py`는 `AgePredictorWrapper`를 초기화하지만, FastAPI가 사용하는 `core/pipeline.py`에는 age predictor import/호출이 없고, `api_server.py` health 목록 및 JSON `findings`, `Dental_015` 리포트 타입에도 Dental_011 결과가 없습니다. 즉 Streamlit 진입점과 FastAPI→Dental_015 SSOT 경로의 모듈 범위가 다르며, README가 단일 E2E 파이프라인처럼 묘사한 흐름과 현재 구현은 일치하지 않습니다.

**권고:** Dental_011이 통합 범위라면 pipeline→API 스키마→프론트엔드 렌더링 및 health 상태까지 연결하고, 범위 밖/보류라면 Reader README의 E2E 그림과 기능 설명에서 현재 기능처럼 보이는 연결을 제거하거나 `미연동/선택 기능`으로 표시하십시오.
## 4. 확인된 정상/개선 사항

- 검토 보고서를 추가하기 전 로컬 18개 저장소의 Git 브랜치는 모두 `main`, 작업 트리는 모두 clean이었습니다. 이 보고서를 새 파일로 저장한 뒤 `Dental_000`에는 이 보고서만 미추적 상태로 추가되었습니다.
- 두 superproject의 등록된 submodule 커밋 SHA는 각 로컬 submodule 체크아웃과 일치했습니다. 다만 이는 원격 `origin/main`과의 최신성 확인을 뜻하지 않습니다.
- `Dental_000`의 직접 모듈 목록에는 `Dental_Core`가 없다는 점을 제외하면, 등록된 링크는 체크아웃과 정합했습니다.
- `260928_0312_Codex_Dental_Module_Weights_Full_Audit.md`의 261013 1455 후속 조치와 `10_cases_quantitative_benchmark.json` 최신 detail을 대조한 결과, #36/#29의 `best_candidate_iou`, 후보 좌표 및 대응 FP 레코드가 JSON에 반영되어 이전 P0 추적성 지적은 해결됐습니다. TP/FP/FN 집계도 맞습니다.
- Dental_013 README는 단독 EfficientNet 분류기와 통합 파이프라인 31-class ONNX 모델의 이중 구조를 설명하며, 케이스 단위 검출률과 객체 단위 지표도 구분하고 있습니다. 중앙 요약 표에 그 정의가 전달되지 않은 것이 남은 문서 문제입니다.

## 5. 기존 GitHub 이슈 인지 여부

2026-10-25 GitHub 커넥터에서 관련 저장소의 이슈 키워드를 조회하고 선택 이슈의 현재 상태 및 종결 코멘트를 확인했습니다. 관련 키워드로 검색된 열린 이슈는 없었고, Dental_000#12 총괄 이슈도 `closed` 상태이며 모든 P0/P1/P2가 종결되었다고 기록합니다. 다만 아래 항목들은 같은 문제를 완전히 추적·해결한 것으로 보기 어렵습니다.

| 현재 검토 항목 | 기존 이슈/상태 | 대조 결과 |
|---|---|---|
| API readiness 의미 | [Dental_Panoramic_Reader#4](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/4) `closed` (2026-10-19) | 기존 고정 `0.15/LOW`는 실제 OsteoMAENet 연결 및 가중치 부재 시 `NOT_AVAILABLE`로 고쳤다고 종결 코멘트에 기록되어 있고, 현재 코드도 그 조치를 반영합니다. 그러나 health 전체 `HEALTHY` 고정 및 파일 존재 기반 `ONLINE` 표시는 그 이슈의 완료 내용에 포함되지 않아 별도 잔여 문제입니다. |
| API `patientId` 고정 | 관련 열린 이슈 없음 | `PATIENT-DEMO`를 요청마다 고정하는 문제는 이번 관련 키워드 검색에서 열린 이슈를 찾지 못했습니다. |
| 빈 결과의 정상/미실행 구분 | 관련 열린 이슈 없음 | “특이 소견 없음” 대 `NOT_AVAILABLE`/모듈 오류 구분은 현재 별도 열린 이슈에서 확인되지 않았습니다. |
| Dental_011 API/UI 미연동 | [Dental_Panoramic_Reader#10](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/10) `closed` (2026-10-21) | 해당 이슈는 다중 진입점과 모듈 로직 분산을 직접 다뤘으므로 문제 계열은 인지했습니다. 그러나 종결 코멘트는 역할 분담·유틸 통합을 언급할 뿐, 본문 완료 조건인 Streamlit/API의 동일 파이프라인 사용은 입증하지 않습니다. 현재 Streamlit `app.py`는 age wrapper를 쓰고 FastAPI 경로는 쓰지 않아 이번 잔여 차이가 남습니다. |
| Dental_013 성능표/분모 및 벤치마크 경로 | [Dental_000#3](https://github.com/HyunchanAn/Dental_000/issues/3) `closed` (2026-10-19) 및 [Dental_013#1](https://github.com/HyunchanAn/Dental_013/issues/1) `closed` (2026-10-19) | 둘 다 README 성능표·모델 구조 정합 문제를 명시적으로 인지했습니다. Dental_000#3의 종결 코멘트는 성능표 수정과 JSON 인용을 주장하지만 현재 README가 가리키는 `reports_archive/10_cases_quantitative_benchmark.json`은 로컬에 없고, Dental_013의 100%는 설명상 4/4 any-hit인데 섹션/중앙 표는 10례처럼 씁니다. 과거 이슈가 같은 문제군을 다뤘으나 남은 세부 불일치를 추적하지 않고 닫힌 상태입니다. |
| Dental_Core 직접 submodule 설명 | [Dental_Panoramic_Reader#10](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/10) `closed` | Reader 안에서 Dental_Core 유틸리티를 사용하는 문제는 다뤘지만, Dental_000 `.gitmodules`에 직접 바인딩이 없는데 README가 있다고 한 구조 불일치는 그 이슈와 별개로 열린 채 추적되지 않습니다. |
| 전체 상태 종결 | [Dental_000#11](https://github.com/HyunchanAn/Dental_000/issues/11), [Dental_000#12](https://github.com/HyunchanAn/Dental_000/issues/12) 모두 `closed` (2026-10-21) | #11은 상태 배지 및 기존 감사 문서 마감, #12는 전체 이슈 종결을 기록합니다. 현재 새 정적 검토에서 찾은 잔여 사항을 재검토하는 열린 후속 이슈는 검색 결과에 없었습니다. |

**판정:** 일부 문제군은 기존 이슈가 인지했지만, 현재 남은 세부 사항까지 추적 중인 열린 이슈는 찾지 못했습니다. 특히 Reader#10은 본문 체크리스트가 미완료 표시인 상태에서 완료 코멘트로 닫혀 있고, Dental_000#3의 닫힘 뒤에도 성능표 경로/분모 문제가 남아 있습니다. 이 보고서에는 해당 사실을 추가했으며, 이 요청 범위에서 GitHub 이슈를 새로 만들거나 재개하지는 않았습니다.

## 6. 후속 우선순위

1. **랩탑 개발팀:** Reader health/readiness와 모듈별 실패 상태를 실제 초기화·로드 결과에 연동하고, 고정 `PATIENT-DEMO` 식별자 및 빈 결과 문구를 스키마와 함께 정리합니다.
2. **랩탑 개발팀 / 문서 담당:** `Dental_000/README.md`의 JSON 경로, Dental_013 지표명, `Dental_Core` submodule 설명을 실제 저장소와 일치시키고, Reader README의 Dental_011 연동 상태를 구현과 맞춥니다.
3. **메인 워크스테이션 / 총괄:** 시리즈 성능표는 출처·가중치 해시·데이터 분할·지표 단위를 함께 고정하고, 업데이트 시 중앙 README와 모듈 README/JSON을 동시 갱신합니다.
4. **Codex:** 수정 후 정적 재검토를 수행합니다. 이 보고서에서는 테스트 실행이나 임상 승인 판정을 하지 않았습니다.
5. **이슈 담당자:** Dental_000#3과 Dental_Panoramic_Reader#10의 잔여 범위를 재개방할지, 기존 이슈를 교차참조하는 새 후속 이슈로 관리할지 결정하고, 현재 발견 중 미추적 항목(patientId/readiness 등)을 추적 항목에 포함합니다.

## 7. 한계

이번 작업은 전 저장소 README·Git 형상 및 통합 경로의 표적 정적 검토입니다. 모든 소스 파일을 줄 단위로 읽거나 테스트를 실행하지 않았고, API 서버·모델을 띄우지 않았으며, 원격 GitHub는 관련 키워드 검색과 위 선택 이슈만 확인했으며, 18개 저장소 전체 이슈를 모두 페이지 조회한 것은 아닙니다. 원격 CI 및 Hugging Face 파일 상태도 확인하지 않았습니다. 따라서 이 문서는 발견된 로컬 문서/코드 불일치에 대한 검토 보고서이지 임상 유효성, 보안 인증, 배포 적합성 또는 원격 이슈 전체 종결에 대한 확인서가 아닙니다.





