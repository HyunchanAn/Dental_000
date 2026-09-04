# [메인 워크스테이션] Dental MSA Presentation Layer (Dental_015) 이행 및 API 계약 수립 계획서

## 1. 개요
Dental 마이크로서비스 아키텍처(001~014)의 현 모듈형 모놀리스(Modular Monolith) 구조를 서비스 지향 아키텍처(MSA)로 전환하기 위한 첫 단계로서, Presentation 레이어인 Dental_015 프론트엔드 플랫폼과 Dental_Panoramic_Reader 백엔드 API 게이트웨이 간의 연동 전략 및 설계 계약(Contract)을 정의합니다.

## 2. 현 아키텍처 진단 및 이행 방향
- 현 구조 진단: 도메인 모듈(001~014) 및 래퍼(Dental_Panoramic_Reader)가 Git 서브모듈 및 Python In-memory 함수 호출 방식으로 연결된 모듈형 모놀리스 구조입니다.
- 목표 아키텍처: UI Presentation 레이어(Dental_015)와 백엔드 오케스트레이션 레이어(Dental_Panoramic_Reader REST API)를 HTTP/JSON 프로토콜 기반으로 분리하는 MSA presentation 이행을 목표로 합니다.

## 3. 핵심 아키텍처 설계 원칙

1. 프론트엔드 단일 창구 직결 (Fat Frontend 방지)
   - Dental_015 프론트엔드는 개별 도메인 모듈(002, 012 등)을 직접 호출하지 않으며, 오케스트레이터인 Dental_Panoramic_Reader 게이트웨이만 단일 엔드포인트(Single Point of Entry)로 바라봅니다.

2. SSOT 데이터 스키마 재활용
   - Dental_Panoramic_Reader가 기존 파이프라인에서 생성하던 Final Report JSON 구조를 API Response Body의 표준 스키마로 준용하여 인터페이스 일관성을 유지합니다.

## 4. 단계별 실행 계획

### 1단계: 백엔드 얇은 API 게이트웨이 탑재 (Dental_Panoramic_Reader)
- FastAPI 기반 REST API 엔드포인트 수립
- 핵심 엔드포인트 규격:
  - POST /api/v1/infer : 파노라마 이미지(multipart/form-data) 수신 후 통합 분석 JSON 결과 반환
  - GET /api/v1/health : MSA 모듈 로딩 및 GPU 가용 상태 점검

### 2단계: 프론트엔드 Mocking 및 Canvas UI 개발 (Dental_015)
- 백엔드 엔드포인트 완성 전까지 기존 Final Report JSON 구조 기반의 Mock 응답으로 UI 인터렉션 구현
- 파노라마 이미지 visualizer 및 좌표(BBox/Polygon) 오버레이 Canvas 컴포넌트 구축

### 3단계: 통합 검증 및 E2E 테스트
- Dental_015 Axios 통신 클라이언트와 Reader FastAPI 엔드포인트 실서버 통신 전환 및 런타임 검증

## 5. 데이터 전달 규격 검토 사항
- 마스크 및 BBox 시각화 전달 시 Base64 대용량 인코딩 전송 대신, 좌표 데이터(Polygons/BBoxes) 중심의 JSON 전송 규격을 채택하여 프론트엔드 Canvas 상에서 동적 오버레이 렌더링을 수행함으로써 네트워크 대역폭을 최적화합니다.

# [랩탑 개발팀] 아키텍처 이행 계획서 검토 의견 및 핵심 질의사항

## 1. 아키텍처 방향성에 대한 종합 평가
- [Fat Frontend 방지 및 단일 창구화]: 프론트엔드가 개별 백엔드 모듈(001~014)을 직접 호출하지 않고 Dental_Panoramic_Reader 게이트웨이만 단일 접점으로 구성하는 아키텍처는 결합도를 최소화하고 배포 독립성을 확보하는 매우 타당한 설계입니다.
- [JSON 좌표 기반 동적 Canvas 렌더링]: Base64 인코딩 이미지 전송을 배제하고 좌표 데이터 중심 JSON 스키마를 채택한 점은 프론트엔드 렌더링 성능 최적화 및 네트워크 대역폭 절감 측면에서 최선의 선택입니다.

## 2. 세부 검토 및 비판적 의문점 (기술 질의)

### [질문 1] 동기 추론(Synchronous POST) vs 비동기 큐/Polling 방식의 처리 기준
- 현 계획서의 POST /api/v1/infer는 동기식 HTTP 요청 구조입니다.
- 001~014 다중 AI 모델이 연쇄적으로 추론을 수행할 경우, 전체 연산 시간에 따라 HTTP Timeout(예: 30초 초과) 또는 브라우저 대기 지연이 발생할 수 있습니다.
- [검토 제안]: 초기 MVP는 동기 방식을 적용하되, 대용량 파노라마나 고부하 연산 시 job_id를 반환하고 Status를 Polling(또는 SSE/WebSocket)하는 비동기 작업 큐 아키텍처로의 전환 가능성을 고려해야 합니다.

### [질문 2] 분석 진행률(Progress Status) 실시간 스트리밍 필요 여부
- 파이프라인 연산 중 (예: 우식증 탐지 중 -> 치조골 측정 중 -> 리포트 생성 중) 임상의 UI에 단계별 진행 상태를 시각화할 계획이 있으신지 문의드립니다.
- 필요하다면 FastAPI의 Server-Sent Events (SSE) 엔드포인트를 추가하여 진행 상태를 스트리밍하는 방식을 2단계/3단계 실행 계획에 포함시키는 것을 제안합니다.

### [질문 3] JSON 좌표 데이터의 정규화(Normalization) 여부
- Canvas 상에서 이미지를 리사이징하거나 Zoom/Pan을 수행할 때, BBox/Polygon 좌표 규격이 원본 이미지의 절대 피셀 좌표(Pixel Coordinates)인지, 0.0~1.0 사이의 정규화 좌표(Normalized Coordinates)인지 구분이 필요합니다.
- 해상도 가변 대응 및 Canvas 스케일링을 위해 API 스키마 상 정규화 좌표 사용을 기본으로 지정하는 것을 권장합니다.

### [질문 4] Mock 데이터 스키마의 SSOT 위치
- 2단계 프론트엔드 Mocking 작업 시 참조할 표준 Final Report JSON 스키마 샘플 파일의 위치가 Dental_000 내 테스트 자산인지, Dental_Panoramic_Reader 내부 스키마 정의 파일인지 명확한 위치 확인이 필요합니다.

## 3. 향후 실행 세부 협의 제안
- 상기 기술 질의에 대해 의견이 정립되시면, Dental_015 측에서는 선제적으로 정규화 좌표 기반 Canvas 오버레이 렌더러 및 Axios 인터셉터 구조 개발에 즉시 착수하겠습니다.


---

# [메인 워크스테이션] 랩탑 개발팀 기술 질의에 대한 회신 (2026-08-25)

랩탑 개발팀에서 제시해주신 비판적 아키텍처 검토 의견과 4가지 핵심 기술 질의사항을 확인했습니다. 질의해주신 각 항목에 대한 메인 워크스테이션의 표준 및 답변은 다음과 같습니다.

## 1. 기술 질의에 대한 공식 회신

### [답변 1] 동기 추론 vs 비동기 큐/Polling 수용 방안
- 1단계 MVP 구현: 통신 및 인터페이스 신속 검증을 위해 동기식 POST /api/v1/infer를 우선 적용합니다.
- 향후 비동기 확장성: 파이프라인 부하 심화 및 HTTP Timeout 이슈에 대비하여, 2단계 고도화 시 POST /api/v1/jobs (job_id 즉시 반환) 및 GET /api/v1/jobs/{job_id} Polling/SSE 구조로 원활히 마이그레이션할 수 있도록 백엔드 라우터 구조를 유연하게 캡슐화합니다.

### [답변 2] 분석 진행률(Progress Status) 실시간 스트리밍
- 임상 UX 차원에서 모듈별 진행 상황(예: 008 탐지 완료 -> 002 우식 분석 중) 시각화는 필요합니다.
- 1단계 기본 인터페이스 결합 완료 후, FastAPI의 Server-Sent Events (SSE) 기반 엔드포인트를 2단계 실행 계획에 공식 포함하여 연동 개발을 진행합니다.

### [답변 3] JSON 좌표 데이터 정규화(Normalization) 표준화
- 프론트엔드 Canvas의 가변 해상도, Zoom/Pan 및 반응형 스케일링 대응을 위해, API가 반환하는 모든 BBox 및 Polygon 좌표 규격은 0.0 ~ 1.0 사이의 정규화 좌표(Normalized Coordinates)를 기본 표준으로 확정합니다.
- 단, 필요 시 상호 변환을 위해 JSON metadata 객체 내에 파노라마 원본 이미지의 width, height (pixel) 정보를 반드시 함께 제공합니다.

### [답변 4] Mock 데이터 스키마의 SSOT 관리 위치
- 프론트엔드 및 백엔드 개발이 참조할 표준 Final Report JSON 스키마의 SSOT 위치는 중앙 QA 저장소인 Dental_000 내 schemas/final_report_schema.json (및 tests/assets/final_report_sample.json)으로 일원화하여 관리 및 배포합니다.

## 2. 향후 진행 절차
상기 답변에 따라 표준 스키마 및 좌표 규격이 확정되었으므로, Dental_015 및 Dental_Panoramic_Reader 팀에서는 2단계 실행 계획(Mock 기반 Canvas 렌더러 개발 및 FastAPI 래퍼 구축)에 즉시 착수해주시기 바랍니다.


# [맥북 개발팀] # [Walkthrough] Dental_015 아키텍처 회신 반영 및 Canvas 뷰포트 Engine 구축

메인 워크스테이션의 표준 명세 회신을 기반으로 `Dental_015` 모듈의 2단계 핵심 컴포넌트 개발 및 타입 선언을 완결했습니다.

## 핵심 변경 및 구축 내역

### 1. 정규화 좌표 타입 스키마 선언 (`src/types/finalReport.ts`)
- [NormalizedBBox & NormalizedPolygon](file:///d:/Github/Dental_015/src/types/finalReport.ts): API 반환 규격인 0.0 ~ 1.0 정규화 좌표(BBox/Polygon) 및 파노라마 원본 해상도(width, height) 메타데이터 타입 정의.

### 2. 표준 SSOT Mock 데이터 수립 (`src/mocks/mockFinalReport.ts`)
- [mockFinalReport](file:///d:/Github/Dental_015/src/mocks/mockFinalReport.ts): 치아 우식증(Caries), 치조골 소실(Bone Loss), 치근단 병변(Periapical Lesions) 정규화 좌표를 포함한 테스트 mock 데이터 구축.

### 3. 동적 Canvas 오버레이 렌더러 구현 (`src/components/PanoramaCanvasViewer.tsx`)
- [PanoramaCanvasViewer](file:///d:/Github/Dental_015/src/components/PanoramaCanvasViewer.tsx):
  - Canvas 뷰포트 크기에 맞춰 정규화 좌표(0.0~1.0)를 비율별 동적 변환하여 바운딩 박스 및 다각형 영역 렌더링.
  - 라벨, 확신도(Confidence Score), 치아 번호(FDI notation) 및 하이라이트 투명도 오버레이 구현.

### 4. 메인 UI 결합 및 GitHub 푸시 (`src/App.tsx`)
- [App.tsx](file:///d:/Github/Dental_015/src/App.tsx): 대시보드 내 PanoramaCanvasViewer 연동 완료.
- GitHub 원격 반영: `feat: Add Normalized Canvas Viewer and SSOT Final Report Types` 커밋 및 [HyunchanAn/Dental_015](https://github.com/HyunchanAn/Dental_015) 푸시 완료.

## 메인 워크스테이션 회신 주요 합의사항

1. **좌표 표준화**: BBox 및 Polygon은 0.0 ~ 1.0 정규화 좌표 사용 (원판 width/height 포함).
2. **비동기 확장 대비**: 1단계 동기 POST 후 2단계 SSE/Polling 지원 구조로 백엔드 라우터 캡슐화.
3. **SSOT 위치**: `Dental_000/schemas/final_report_schema.json`에서 통합 관리.
