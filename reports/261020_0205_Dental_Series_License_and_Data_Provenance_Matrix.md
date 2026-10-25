# [ 261020 0205 랩탑 개발팀 ] Dental 시리즈 18개 저장소 및 Hugging Face 가중치 라이선스·데이터 출처 SSOT 매트릭스

## 1. 개요 및 기본 원칙
- 본 문서는 `Dental_000`부터 `Dental_015`, `Dental_Core`, `Dental_Panoramic_Reader`에 이르는 18개 GitHub 저장소와 Hugging Face Hub(`chemahc94/*`)에 배포된 모델 가중치의 [소스 코드 라이선스], [학습·검증 데이터셋 출처 및 라이선스], [파생 가중치 배포·이용 조건]을 단일 진실 공급원(SSOT)으로 정의한다.
- 핵심 분리 원칙:
  1. [소스 코드 (Source Code)]: 모든 저장소의 자체 작성 파이프라인, 추론 래퍼, UI, 테스트 코드는 `MIT License`를 따른다(`Dental_001`은 원저자 Muhammad Anwaar Khalid 및 기여자 Hyunchan An 공동 MIT 고지).
  2. [데이터셋 및 파생 라벨 (Datasets & Derived Annotations)]: 각 공개 데이터셋의 원 라이선스(`CC BY 4.0`, `CC BY-NC-SA 4.0`, `CC0 1.0`, Kaggle 대회 규정 등)를 엄격히 승계한다.
  3. [학습된 모델 가중치 (Trained Model Weights)]: 비영리 조건(`CC BY-NC-SA 4.0`, 기관 제한 데이터 등)이 포함된 데이터셋으로 학습된 가중치는 학술 연구 및 비영리 교육 목적(`cc-by-nc-sa-4.0` 또는 `other` 비영리 연구용)으로만 사용 가능하며, 상업적 환경 배포 시에는 상업적 이용이 허용된 자체 데이터셋으로 재학습해야 한다.

---

## 2. 18개 GitHub 저장소별 코드·데이터·가중치 라이선스 매트릭스

| 저장소 | 소스 코드 라이선스 (`LICENSE` 파일) | 주요 사용 데이터셋 및 원 출처 | 데이터셋 라이선스 / 이용 조건 | 파생 가중치 라이선스 (HF Hub) |
| :--- | :---: | :--- | :--- | :--- |
| `Dental_000` | `MIT License` | `DENTEX` 파생 `data/yolo_fdi` (462 Train / 38 Val), `dental_008_dentex_manifest.csv` (507/127) | `CC BY-NC-SA 4.0` (`ibrahimhamamci/DENTEX`, 비영리·동일조건) | `CC BY-NC-SA 4.0` (비영리 연구 전용) |
| `Dental_Panoramic_Reader` | `MIT License` | 통합 파이프라인 (자체 학습 데이터 없음, 10례 임상 벤치마크) | 코드 `MIT`, 각 서브모듈 가중치 조건 준수 | `CC BY-NC-SA 4.0` (`chemahc94/Dental-AI-Models`) |
| `Dental_Core` | `MIT License` | 공통 유틸리티 라이브러리 (데이터셋 없음) | 해당 없음 (`N/A`) | 해당 없음 (`N/A`) |
| `Dental_001` | `MIT License` (원저자 + 기여자) | `Aariz Cephalometric Dataset` (Figshare, CVM ROI 637장 파생) | `CC BY 4.0` (원저자 표시 및 ROI 크롭/정제 변경 고지) | `MIT` / `CC BY 4.0` (`chemahc94/Cephalometric-Landmark-CVM`) |
| `Dental_002` | `MIT License` | `DENTEX` (우식·병소·매복치) + 2-Stage 치아 패치 파생 데이터셋 | `CC BY-NC-SA 4.0` (비영리·동일조건) | `CC BY-NC-SA 4.0` (`chemahc94/caries-detection-weights`) |
| `Dental_003` | `MIT License` | `Panoramic radiography database` (Zenodo `4457648`) 및 `UFBA-UESC` 참고 | `CC BY 4.0` (Zenodo `4457648`) / 요청 기반 학술 이용 (`UFBA-UESC`) | `CC BY-NC-SA 4.0` (`chemahc94/pano-boneloss-weights`) |
| `Dental_004` | `MIT License` | `Tufts Dental Database`, `DENTEX`, `Kaggle Panoramic X-rays` | `Tufts` (학술 이용 동의), `DENTEX` (`CC BY-NC-SA 4.0`) | `CC BY-NC-SA 4.0` (`chemahc94/Dental_004_Model`) |
| `Dental_005` | `MIT License` | `AlphaDent` (Kaggle 구내 사진 우식·보철 검출 대회 데이터셋) | Kaggle 대회 규정 (비영리 학술 연구·벤치마크 한정) | 비영리 연구 전용 (`chemahc94/Dental_005_Model`) |
| `Dental_006` | `MIT License` | Open Access 학술 메타데이터 (`PubMed Central OA`, `Europe PMC`, `Unpaywall`) | 각 OA 논문 라이선스 (`CC BY` 등, 출판사 비OA PDF 수록 배제) | 해당 없음 (Local Ollama `Gemma` 모델 활용) |
| `Dental_007` | `MIT License` | 자체 생성 치아 블록 STL 메쉬 (`molar_block_01/02.stl`) 및 문헌 참조 물성치 (`dentin_materials.xml`) | `MIT License` (문헌 참조 탄성계수·포아송비 출처 README 명시) | 해당 없음 (`FEniCSx / dolfinx` 수치 해석) |
| `Dental_008` | `MIT License` | `DENTEX` (`quadrant_enumeration` 634장: Train 507 / Val 127) + 무치악 배경 영상 (Train 60 / Holdout 15) | `CC BY-NC-SA 4.0` (비영리·동일조건) | `CC BY-NC-SA 4.0` (`chemahc94/dentex-tooth-segmentation`) |
| `Dental_009` | `MIT License` | 기하학적 규칙 기반 (Winter / Pell-Gregory 분류, 별도 학습 데이터 없음) | 해당 없음 (`N/A`, 10례 임상 벤치마크 검증) | 해당 없음 (Rule-based Geometric Analyzer) |
| `Dental_010` | `MIT License` | 동적 정중선 인접치 갭 휴리스틱 (별도 학습 데이터 없음) | 해당 없음 (`N/A`, 10례 임상 벤치마크 검증) | 해당 없음 (Rule-based Heuristic) |
| `Dental_011` | `MIT License` | `Pediatric Dental X-ray Dataset` (Zenodo `16745408`, 9~19세 파노라마 295장) | `CC BY 4.0` (저작자 표시) | `CC BY 4.0` (`chemahc94/Dental-AI-Models`) |
| `Dental_012` | `MIT License` | `Mendeley Panoramic Periapical Dataset` + `DENTEX` 정상 해부학 구조물 Negative 샘플 | `CC BY 4.0` (Mendeley) + `CC BY-NC-SA 4.0` (DENTEX Negative 병합분) | `CC BY-NC-SA 4.0` (`chemahc94/Dental_012`) |
| `Dental_013` | `MIT License` | `Kaggle Dental Disease Panoramic Detection Dataset` (`lokisilvres`) | Kaggle 공개 데이터셋 조건 (학술·연구 목적) | 비영리 연구 전용 (`chemahc94/Dental_013`) |
| `Dental_014` | `MIT License` | `BRAR-anchored` 다중 모달 임상 골흡수 코호트 (1,104명, 비공개/접근 제한) | 비공개 연구 데이터 (저장소 내 원본 이미지 미배포, 환자 그룹 분할 적용) | 비영리 연구 전용 (`chemahc94/Dental_014`) |
| `Dental_015` | `MIT License` | 데모 샘플 영상 `public/sample_panorama.png` (`DENTEX` 유래 공개 샘플 1장) | 코드 `MIT`, 데모 샘플 영상 `CC BY-NC-SA 4.0` | 해당 없음 (React/TypeScript 프런트엔드) |

---

## 3. Hugging Face Hub (`chemahc94/*`) 모델 카드 표준화 내역
- 대상 모델 저장소:
  1. `chemahc94/Dental-AI-Models` (통합 가중치 허브)
  2. `chemahc94/Dental_012`
  3. `chemahc94/Dental_013`
  4. `chemahc94/Dental_014`
  5. `chemahc94/dentex-tooth-segmentation`
  6. `chemahc94/caries-detection-weights`
  7. `chemahc94/pano-boneloss-weights`
  8. `chemahc94/Dental_001_Model`
  9. `chemahc94/Dental_003_Model`
  10. `chemahc94/Dental_004_Model`
  11. `chemahc94/Dental_005_Model`
- 조치 사항:
  - 기존 `'More Information Needed'` 빈 템플릿 상태였던 모델 카드(`README.md`)의 YAML Frontmatter에 `license: cc-by-nc-sa-4.0` (또는 해당 데이터셋 라이선스) 및 `tags`를 명시하고, 본문에 학습 아키텍처, 원본 데이터셋 출처·라이선스, 비영리 연구 전용 제한 고지를 일괄 반영한다.

---

# [ 261025 1455 랩탑 개발팀 ] 18개 전 저장소 LICENSE 및 데이터 출처·HF 모델 카드 정비 완결 및 공식 종결 (`[CLOSED]` / `[PASS]`)

- 상태: 공식 종결 (`[CLOSED]` / `[PASS]` 완결)
- 이행 결과: 본 매트릭스에 정의된 18개 전 GitHub 저장소의 `LICENSE` 파일, `README.md` 데이터셋 출처·라이선스 고지 및 Hugging Face Hub 11개 모델 저장소의 모델 카드 정비가 100% 완료되었으므로 본 SSOT 문서를 `[CLOSED]` / `[PASS]` 완결로 공식 종결한다.
