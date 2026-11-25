# [ 261125 1530 랩탑 개발팀 ] (Dental 시리즈 전수조사 기반 잔여 이슈 통합 실행 계획서 - Umbrella Plan)

## 1. 기존 계획서 검토 및 리뉴얼 배경

- 기존 계획서: `plans_replies_walkthrough/261025_1810_Codex_Review_and_Series_Remediation_Plan.md`
  - 2026-10-25 Codex 검토 지적사항 및 11-09 ~ 11-24 단계별 로드맵 완결(CI 복구, 단위 테스트, 보안/인메모리 DICOM, 로드맵 11건 종결) 이력이 누적되어 있으며, 2026-11-24 16:24 시점 기준 잔여 이슈 3건(`Dental_000#17`, `Dental_000#13`, `Dental_Panoramic_Reader#15`)으로 마감 기록이 남아 있다.
  - 기존 문서는 과거 완결 이력 보존을 위해 원형을 유지하며, 본 문서가 2026-11-25 기준 최신 공식 실행 계획서(Umbrella Plan)로 대체한다.
- 리뉴얼 사유:
  - 2026-11-24 21:21~21:23 전수조사(GitHub 등록 2026-11-25)를 통해 18개 저장소(`Dental_000`~`Dental_015`, `Dental_Core`, `Dental_Panoramic_Reader`) 간 실제 런타임 통신 단절, 스키마/API 계약 불일치, 보안·임상 판정 결함 및 README 괴리가 확인되어 신규 Umbrella 이슈(`Dental_000#18`) 및 하위 이슈 10건이 추가 등록되었다. (`Dental_016`은 타측 오류로 삭제되어 조사 및 계획 대상에서 완전 제외)
  - 이에 따라 현재 Open 이슈 총 14건을 `[READY]`(즉시 코드·테스트 실행 가능), `[PARTIAL-FREEZE]`(기술 수정은 가능하나 임상/정책 판단 구간 동결), `[FREEZE]`(오너 승인·외부 설정 대기)로 재분류하고 실행 순서를 재정립한다.

---

## 2. 전체 Open 이슈 14건 통합 현황 및 상태 분류

| 우선순위 | 저장소 및 이슈 | 분류 | 상태 | 개별 계획서 위치 |
| :--- | :--- | :--- | :--- | :--- |
| P0 | [Dental_000#18](https://github.com/HyunchanAn/Dental_000/issues/18) | 총괄(Umbrella) | `[IN PROGRESS]` | 본 문서 |
| P0 | [Dental_006#59](https://github.com/HyunchanAn/Dental_006/issues/59) | 복구/통신 | `[READY]` | `Dental_006/plans_replies_walkthrough/261125_1530_Dental_006_Issue59_Remediation_Plan.md` |
| P0 | [Dental_Panoramic_Reader#21](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/21) | 통합/인터페이스 | `[READY]` | `Dental_Panoramic_Reader/plans_replies_walkthrough/261125_1530_Dental_Panoramic_Reader_Issues_21_22_15_Plan.md` |
| P0 | [Dental_015#4](https://github.com/HyunchanAn/Dental_015/issues/4) | 보안/임상 UI | `[PARTIAL-FREEZE]` | `Dental_015/plans_replies_walkthrough/261125_1530_Dental_015_Issue4_Remediation_Plan.md` |
| P1 | [Dental_Core#7](https://github.com/HyunchanAn/Dental_Core/issues/7) | 스키마/공통 | `[PARTIAL-FREEZE]` | `Dental_Core/plans_replies_walkthrough/261125_1530_Dental_Core_Issue7_Remediation_Plan.md` |
| P1 | [Dental_Panoramic_Reader#22](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/22) | API/문서 | `[READY]` | `Dental_Panoramic_Reader/plans_replies_walkthrough/261125_1530_Dental_Panoramic_Reader_Issues_21_22_15_Plan.md` |
| P1 | [Dental_009#4](https://github.com/HyunchanAn/Dental_009/issues/4) | 임상 로직 | `[PARTIAL-FREEZE]` | `Dental_009/plans_replies_walkthrough/261125_1530_Dental_009_Issue4_Remediation_Plan.md` |
| P1 | [Dental_010#4](https://github.com/HyunchanAn/Dental_010/issues/4) | 임상 정합성 | `[PARTIAL-FREEZE]` | `Dental_010/plans_replies_walkthrough/261125_1530_Dental_010_Issue4_Remediation_Plan.md` |
| P1 | [Dental_012#4](https://github.com/HyunchanAn/Dental_012/issues/4) | 브리지/정합 | `[READY]` | `Dental_012/plans_replies_walkthrough/261125_1530_Dental_012_Issue4_Remediation_Plan.md` |
| P1 | [Dental_013#4](https://github.com/HyunchanAn/Dental_013/issues/4) | 브리지/ONNX | `[READY]` | `Dental_013/plans_replies_walkthrough/261125_1530_Dental_013_Issue4_Remediation_Plan.md` |
| P2 | [Dental_000#19](https://github.com/HyunchanAn/Dental_000/issues/19) | CI/스크립트/문서 | `[PARTIAL-FREEZE]` | 본 문서 4장 (Track 4) |
| P2 | [Dental_000#13](https://github.com/HyunchanAn/Dental_000/issues/13) | 구형 총괄 | `[FREEZE]` | 본 문서 3장 (오너 승인 대기) |
| P0 | [Dental_000#17](https://github.com/HyunchanAn/Dental_000/issues/17) | 로드맵/동결 트래커 | `[FREEZE]` | 본 문서 3장 (오너 승인 대기) |
| P2 | [Dental_Panoramic_Reader#15](https://github.com/HyunchanAn/Dental_Panoramic_Reader/issues/15) | HF Space 배포 | `[FREEZE]` | `Dental_Panoramic_Reader/plans_replies_walkthrough/261124_1624_HF_Private_Space_Token_and_Deploy_Runbook.md` |

- 개별 Open 이슈 0건 저장소(9개): `Dental_001`, `Dental_002`, `Dental_003`, `Dental_004`, `Dental_005`, `Dental_007`, `Dental_008`, `Dental_011`, `Dental_014`
  - 이 중 `Dental_007`을 제외한 8개 저장소의 잔여 수정 항목(인터페이스, `export_onnx.py` 템플릿, `dataset.yaml`, README 현행화)은 `Dental_Panoramic_Reader#21` 및 `Dental_000#19`에서 통합 추적한다.

---

## 3. [FREEZE] 항목 총괄표 (치과의사 임상 판단 및 오너 승인 대기)

아래 항목은 임의로 확정하거나 실행하지 않고 `[FREEZE]` 상태로 보류한다.

### 3.1 [FREEZE / 임상 판단 필요] 치과의사(안현찬) 직접 판단 항목

| 대상 이슈 | 동결 항목 | 동결 사유 및 치과의사(안현찬) 역할 |
| :--- | :--- | :--- |
| `Dental_010#4` | `verify_missing_teeth` 기본 임계값(`r_gap_threshold`: `0.65` vs `1.55`) 확정 | 두 함수의 기본 임계값이 상이함. `0.65` 유지 시 교정 공간 폐쇄 구간 오탐 가능성, `1.55` 통일 시 협소 결손 공간 미탐지 가능성이 있어 치과의사가 임상 민감도/특이도 기준에 따라 표준 기본값을 최종 결정해야 함. |
| `Dental_009#4` | Winter's Classification 해상도 정규화 비율 임계치 및 임상 분류 결과 검수 | 하드코딩 픽셀값(`10` px, `adj_h > 20`)을 치아 높이 비율 기반으로 치환할 때의 경계 비율 및 Mesioangular/Distoangular/Vertical/Horizontal 판정 기준이 임상적으로 타당한지 치과의사가 최종 검증·승인해야 함. |
| `Dental_015#4` | 우식 확정/의심 신뢰도 컷오프(`0.45` / `0.25`) 및 치주 위험도 게이트(`hba1cPercent`, 차단 문구) 임상 검수 | 프론트엔드와 백엔드 간 기준 불일치를 `0.45`로 1차 정렬할 수 있으나, 최종 임상 판독 화면의 우식 확정/의심 임계치 및 당화혈색소(`HbA1c`) 기반 치주 위험도 안내 문구 적정성은 치과의사가 직접 검토·승인해야 함. |
| `Dental_012#4` | 유치(`51..85`)·과잉치(`19/29/39/49`) 치근단 병소 판정 임상 기준 확인 | 상·하악 판별 코드 확장(`quadrant in (1, 2, 5, 6)`)은 즉시 수정 가능하나, 유치 치근 흡수기와 치근단 병소 구분 및 `clinical_criteria_v1.json` 반영 여부는 치과의사의 임상 판단이 필요함. |

### 3.2 [FREEZE / 오너 승인 필요] 정책·아키텍처·보안·배포 승인 항목

| 대상 이슈 | 동결 항목 | 동결 사유 및 오너(안현찬) 역할 |
| :--- | :--- | :--- |
| `Dental_000#17` | 동결 스코프(`001/004/005/007/009/011/014`) 예외 수정 범위 승인 | `#17`에서 동결 지정된 저장소 중 `009`, `011`, `014`, `001`, `004`, `005`가 `#18`/`#19` 수정 대상에 포함됨. 동결 저장소에 대한 버그픽스 및 문서 현행화 예외 허용 여부를 오너가 승인해야 함. |
| `Dental_015#4` | `.dcm`/`.dicom` 브라우저 렌더링 아키텍처 선택 | (안 1) `Dental_Panoramic_Reader` 서버가 PHI 제거 후 프리뷰 이미지(PNG/base64)를 반환, (안 2) `Dental_015` 프론트엔드에 클라이언트 DICOM 디코더 라이브러리 추가. 보안(PHI 노출 최소화)과 프론트엔드 독립성 간 트레이드오프를 오너가 결정해야 함. |
| `Dental_000#19` | `.gitmodules`에 `Dental_015` 및 `Dental_Core` 포함 여부 정책 | 현재 `Dental_000`은 15개 서브모듈만 직접 바인딩 중. `Dental_015`와 `Dental_Core`를 직접 서브모듈로 편입할지 현행 구조를 유지할지 오너가 결정해야 함. |
| `Dental_Core#7` | 설치 태그 정책 (`@main` vs 신규 릴리스 `v0.2.0` 태그 발행) | `README.md` 설치 가이드 정정 시 브랜치 참조(`@main`)로 변경할지 공식 릴리스 태그(`v0.2.0`)를 발행할지 오너가 승인해야 함. |
| `Dental_Panoramic_Reader#15` | Hugging Face Private Space 생성, 토큰 발급 및 실배포 | 신규 Write `HF_TOKEN` 발급·로컬 주입, `DPR_API_TOKEN` / `DPR_CORS_ORIGINS` 시크릿 등록 및 외부 Space 배포는 오너의 자격 증명 관리 및 최종 배포 승인이 필요함 (`261124_1624` 런북 참조). |
| `Dental_000#13` | 구형 총괄 이슈 종결 및 `#18` 이관 여부 | `#13`의 코드 과업은 완료되었고 잔여 배포 항목만 `#15`에 남아 `#18`과 병존 중. `#13`을 종결 처리할지 유지할지 오너가 승인해야 함. |

---

## 4. 리뉴얼된 실행 순서 (Track 1 ~ Track 4)

`[FREEZE]` 항목을 제외한 `[READY]` 범위만 의존성 순서대로 실행하며, 각 단계 완료 시 원격/로컬 테스트 통과를 검증한다.

### [Track 1 — 최우선 선행] 공통 스키마 및 독립 P0 복구
1. `Dental_Core#7` (`[READY]` 범위): `PanoramaHiTLDocument` 라운드트립 필드 보존(`impacted_teeth`, `lesionSubtype`, `isolatedAnatomicalSuspicion`, `rawClass`, `rct_associated`), `clinical_status`/`label` 규약 통일, `geometry.py` `"confidence"` 키 및 빈 입력 방어, 테스트 보강. (태그 정책은 `[FREEZE]`)
2. `Dental_006#59` (`[READY]` 전체): `Dental_000/reports_archive/generator.py` -> `Dental_006/src/report/` 복구, GROBID(`8070`)/Ollama 환경변수 통일, 배치 스크립트 및 `README.md` 현행화.

### [Track 2 — 독립 단위 모듈 P1 정합화]
3. `Dental_012#4` (`[READY]` 범위): `src/inference.py` 상·하악 판별(`quadrant in (1, 2, 5, 6)`), BGR/RGB 통일, `clinician_corrected` 중복 적재 방지, `export_onnx.py` 및 `README.md` 수정.
4. `Dental_013#4` (`[READY]` 전체): `tooth_crop_bridge.py` 중복 `append` 및 다중 과잉치 키 덮어쓰기 방지, `sys.path` 충돌 개선, `export_onnx.py`(EfficientNet-B0) 및 `README.md` 수정.
5. `Dental_009#4` (`[READY]` 범위): `src/analyzer.py` 좌우 사분면 부호 오류 수정 및 단위 테스트 보강. (비율 기반 임계치 최종 확정은 `[FREEZE / 임상 판단 필요]`)
6. `Dental_010#4` (`[READY]` 범위): `src/detector.py` 중복 FDI 덮어쓰기 방어 및 `README.md` 테스트 건수 정정. (기본 임계값 `0.65` vs `1.55` 확정은 `[FREEZE / 임상 판단 필요]`)

### [Track 3 — 통합 파이프라인 및 프론트엔드 계약 정합화]
7. `Dental_Panoramic_Reader#21` (`[READY]` 전체): 9개 하위 모듈(`002/003/004/008/009/010/011/013/014`) 인터페이스 및 `weights_manifest.yaml` 단절 수정, 유틸리티 스크립트 3종 수정. (로컬 가중치 미보유 모듈은 모킹/인터페이스 테스트로 검증)
8. `Dental_Panoramic_Reader#22` (`[READY]` 전체): `findings.missingTeeth.details`, `caries[].clinicalStatus`, `restorations[].toothNumber` `int` 캐스팅, `moduleExecutionStatus` 정합화, 포트/CORS 정책 및 `README.md` 전면 현행화.
9. `Dental_015#4` (`[READY]` 범위): `hitlLogic.mjs` `overrideSha256` 무결성 우회 제거(보안 P0), `odontogram` `case 'Impacted'` 추가, `< 0.25` 저신뢰도 박스 노출 버그 수정, `GET /api/v1/hitl/{document_id}` 연동, 초기 `9/9 ONLINE` 하드코딩 제거, `README.md` 현행화. (DICOM 렌더링 방식 선택 및 임상 임계치 최종 승인은 `[FREEZE]`)

### [Track 4 — 시리즈 공통 CI·스크립트·템플릿·잔여 README 마감 (`Dental_000#19`)]
10. `Dental_000#19` (`[READY]` 범위):
    - `Dental_000`: `.github/workflows/reusable-ci.yml` 검사 루트(`.`) 수정, `scripts/run_e2e_tests.py` `tests/` 접두사 및 누락 폴더 추가, `scripts/run_e2e_inference.py` `None` 방어, `scripts/hitl_fdi_labeler.py` `modules/` 경로 수정, `Dental_006` 복구 완료 후 `reports_archive/generator.py` 잔존 파일 정리.
    - 시리즈 공통: `Dental_001/002/003/005/008/011/012` `export_onnx.py` 템플릿 정비, `Dental_005` `dataset.yaml` Windows 절대경로 제거 및 Python/requirements 통일, `Dental_008`/`002`/`003` 히트/브리지 방어 로직 추가.
    - 잔여 `README.md` 일괄 현행화: `Dental_001`, `011`, `000`, `004`, `005`, `008`, `014` 및 전 저장소 Python 배지 버전 통일. (단, 동결 스코프 저장소 수정 및 `.gitmodules` 정책은 3.2절 오너 승인 후 반영)

---

## 5. 완료 게이트 및 추적 원칙

- 각 모듈의 `[READY]` 작업 완료 시 해당 저장소의 로컬 테스트(`pytest` / `npm test`) 및 원격 GitHub Actions CI 통과를 확인한다.
- `[FREEZE]` 항목은 치과의사/오너의 회신이 기록되기 전까지 임의 값으로 종결하지 않는다.
- 세션별 실제 변경 내역과 핸드오프 상태는 프로젝트 최상위 `development_log.txt`에만 누적 기록한다.

---

# [ 261125 1618 랩탑 개발팀 ] (임상·오너 의사결정 최종 확정 및 전 트랙 착수 기준)

## 1. 최종 확정된 의사결정 (10건)

1. `Dental_010#4` [임상]: `r_gap_threshold = 1.0`으로 `verify_missing_teeth` 및 `evaluate_missing_teeth_from_boxes` 기본값 통일 (순수 공백이 평균 인접 치아 폭 이상일 때 결손 판정).
2. `Dental_009#4` [임상]: 좌우 사분면 부호 분리 + 맹출 깊이 교합면 허용 오차 `0.10 * adj_h` (`0.88` 비율 휴리스틱 유지, `adj_h > 20` px 하드코딩 비율/양수 가드로 치환).
3. `Dental_015#4` [임상]: 우식 확정 `0.45` / 의심 `0.25`로 백엔드·범례·캔버스 통일, `< 0.25` 저신뢰도 박스 숨김, `hba1cPercent` 입력 필드 및 `hallucinationGuardBlockedClaims` UI 반영.
4. `Dental_012#4` [임상]: 유치(`#51~#85`) 및 과잉치(`#19/#29/#39/#49`) 탐지 병소는 모두 `REVIEW_REQUIRED`로 분류.
5. `Dental_000#17` [정책]: 동결 스코프(`001/004/005/009/011/014`, `007` 제외)에 대해 신규 기능 추가 없이 `#18`/`#19` 범위의 버그픽스·절대경로 제거·템플릿/README 현행화 예외 허용.
6. `Dental_015#4` DICOM [아키텍처]: 안 1 채택 — `Dental_Panoramic_Reader` 서버가 PHI 제거 후 PNG/base64 프리뷰 이미지를 응답에 포함하고 `Dental_015`가 이를 렌더링.
7. `Dental_000#19` `.gitmodules` [구조]: 현행 유지 (15개 서브모듈 유지, README/문서 설명만 실제 구조에 일치화).
8. `Dental_Core#7` 태그 [버전]: 수정 및 테스트 통과 후 `v0.2.0` 릴리스 태그 신규 발행 및 `README.md` 반영.
9. `Dental_Panoramic_Reader#15` [배포]: 보류 유지 (`#21`, `#22`, `Dental_015#4` 완료 및 테스트 통과 후 추후 진행).
10. `Dental_000#13` [트래커]: `#18` 및 `Dental_Panoramic_Reader#15`로 이관 후 종결(`CLOSED`).

