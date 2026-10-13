# [ 260928 치과 임상 라벨 및 판정 기준표 (v1.0 SSOT) ]

- 확정자: 안현찬 치과의사
- 확정 일시: 2026-09-28 KST
- 목적: Dental_008, 012, 013, 009 파이프라인 수정(3단계) 및 메인 워크스테이션 재학습(5단계) 공통 기준

---

## 1. Dental_008 과잉치(Supernumerary) 라벨링 정책
- 표기 원칙: [SEPARATE_ENTITY]
- 치식 명명 체계: FDI Quadrant Code + 9 (예: #19, #29) 또는 SN-1
- 임상 세부 지침:
  상악 제3대구치 후방/치관에 인접한 제4대구치 및 정중이개 과잉치는 독립된 바운딩 박스로 분리 라벨링하며, 정상 32개 영구치열 치식 정렬 시퀀스에서 제외함.

## 2. Dental_012 치근단 병소 임상 임계치 및 검토 필요 게이트
- 확정 병소 기준선 (Definite Lesion): Confidence >= 0.50
- 검토 필요 유보 구간 (Review Required): 0.25 <= Confidence < 0.50
- 음성 배제 구간 (Background / Skip): Confidence < 0.25
- 정상 해부학적 구조(상악동, 이공) 가드 적용 여부: True
- 임상 세부 지침:
  치근단 병소는 반드시 치아 Root Apex 반경 내에 인접할 때만 해당 FDI 번호로 귀속하며(TheGem 병소는 하악 좌측 #36/#37 apex), 단독 투과상은 턱뼈 내 낭종 또는 정상 음영으로 격리함.

## 3. Dental_013 수복물/보철물 4대 임상 분류 매핑 체계
- 확정 4대 핵심 범주: Inlay/Onlay, Crown/Bridge, Implant, Endodontic (RCT)
- 상세 매핑 정의:
- `Amalgam / Resin / Inlay` -> [Inlay/Onlay]
- `Gold / PFM / Zirconia Crown` -> [Crown/Bridge]
- `Implant Fixture / Abutment` -> [Implant]
- `Root Canal Filling / Post` -> [Endodontic (RCT)]

- 임상 세부 지침:
  치아 BBox 내 수복물 마스크가 감지되면 상기 4대 범주 중 가장 일치도가 높은 단일 클래스로 단순화하여 캔버스 및 SSOT에 표기함.

---
상기 기준표는 2단계 임상 라벨 확정 절차를 통해 생성되었으며, 향후 모든 데이터 어노테이션, 파이프라인 통합 및 독립 평가의 절대 기준으로 사용됩니다.
