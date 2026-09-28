import os
import json
import hashlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

app = FastAPI(title="Dental Clinical Criteria & Annotation Review Tool")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../plans_replies_walkthrough"))

THEGEM_IMG_PATH = "D:/Github/Dental_015/example_panorama/panoramic-x-ray-thegem-blog-default.jpg"
THEGEM_SHA256 = "80585d1c86b95b39bb73ffb0d201057f72adb345b6bb15c885aa87f53c505e1b"
THEGEM_WIDTH = 1170
THEGEM_HEIGHT = 540

ANNOTATIONS_FILE = os.path.join(OUTPUT_DIR, "thegem_verified_annotations.json")

class AnnotationBox(BaseModel):
    id: str
    label: str
    fdi: Optional[str] = None
    quadrant: str # Q1, Q2, Q3, Q4, or General
    category: str # supernumerary, impaction, periapical, normal_anatomy, restoration
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: Optional[float] = None
    verified: bool = False
    notes: Optional[str] = ""

class AnnotationSavePayload(BaseModel):
    image_name: str
    image_sha256: str
    image_width: int
    image_height: int
    confirmed_by: str = "안현찬 치과의사"
    boxes: List[AnnotationBox]

class CriteriaModel(BaseModel):
    supernumerary_policy: str
    supernumerary_naming: str
    supernumerary_notes: str
    periapical_threshold_definite: float
    periapical_threshold_review: float
    periapical_anatomical_guard: bool
    periapical_notes: str
    restoration_classes: List[str]
    restoration_mapping: Dict[str, str]
    restoration_notes: str
    confirmed_by: str = "안현찬 치과의사"

# Default raw model prediction and candidate cases for TheGem
def get_initial_boxes() -> List[Dict[str, Any]]:
    return [
        # Upper Right / Q1 (Patient Right = Screen Left)
        {
            "id": "box_sn1",
            "label": "과잉치 후보 (#18 인접)",
            "fdi": "SN-1 (Q1)",
            "quadrant": "Q1 (상악 우측)",
            "category": "supernumerary",
            "x1": 80, "y1": 205, "x2": 130, "y2": 265,
            "confidence": 0.45,
            "verified": False,
            "notes": "상악 우측 제3대구치 후방/치관 인접 과잉치 의심"
        },
        {
            "id": "box_m18",
            "label": "#18 매복 대구치",
            "fdi": "18",
            "quadrant": "Q1 (상악 우측)",
            "category": "impaction",
            "x1": 120, "y1": 210, "x2": 190, "y2": 280,
            "confidence": 0.85,
            "verified": False,
            "notes": "상악 우측 제3대구치 매복 (안현찬 치과의사 정답)"
        },
        {
            "id": "box_r16",
            "label": "#16 수복물 (Crown)",
            "fdi": "16",
            "quadrant": "Q1 (상악 우측)",
            "category": "restoration",
            "x1": 260, "y1": 235, "x2": 325, "y2": 285,
            "confidence": 0.90,
            "verified": False,
            "notes": "상악 우측 제1대구치 보철물"
        },
        {
            "id": "box_sinus",
            "label": "상악동 저 음영 (정상 구조)",
            "fdi": None,
            "quadrant": "Q1 (상악 우측)",
            "category": "normal_anatomy",
            "x1": 350, "y1": 240, "x2": 430, "y2": 285,
            "confidence": 0.28,
            "verified": False,
            "notes": "상악동 방사선 투과상 (치근단 병소 오탐 주의)"
        },

        # Lower Right / Q4 (Patient Right = Screen Left)
        {
            "id": "box_m48",
            "label": "#48 수평 매복",
            "fdi": "48",
            "quadrant": "Q4 (하악 우측)",
            "category": "impaction",
            "x1": 130, "y1": 320, "x2": 215, "y2": 395,
            "confidence": 0.92,
            "verified": False,
            "notes": "하악 우측 제3대구치 수평/심부 매복 (안현찬 치과의사 정답)"
        },
        {
            "id": "box_r46",
            "label": "#46 결손 인접 수복 (#47)",
            "fdi": "46 or 47",
            "quadrant": "Q4 (하악 우측)",
            "category": "restoration",
            "x1": 270, "y1": 320, "x2": 335, "y2": 375,
            "confidence": 0.78,
            "verified": False,
            "notes": "#46 결손 및 #47 잔존 치아 보철 소견"
        },
        {
            "id": "box_mental",
            "label": "하악 이공 (Mental Foramen - 정상 구조)",
            "fdi": None,
            "quadrant": "Q4 (하악 우측)",
            "category": "normal_anatomy",
            "x1": 340, "y1": 380, "x2": 385, "y2": 425,
            "confidence": 0.32,
            "verified": False,
            "notes": "소구치 하방 정상 이공 투과상 (오탐 주의)"
        },

        # Upper Left / Q2 (Patient Left = Screen Right)
        {
            "id": "box_sn2",
            "label": "과잉치 후보 (#28 인접)",
            "fdi": "SN-2 (Q2)",
            "quadrant": "Q2 (상악 좌측)",
            "category": "supernumerary",
            "x1": 1025, "y1": 210, "x2": 1080, "y2": 270,
            "confidence": 0.42,
            "verified": False,
            "notes": "상악 좌측 제3대구치 후방 과잉치 의심"
        },
        {
            "id": "box_m28",
            "label": "#28 매복 대구치",
            "fdi": "28",
            "quadrant": "Q2 (상악 좌측)",
            "category": "impaction",
            "x1": 970, "y1": 215, "x2": 1040, "y2": 290,
            "confidence": 0.88,
            "verified": False,
            "notes": "상악 좌측 제3대구치 매복 소견"
        },
        {
            "id": "box_r26",
            "label": "#26 수복물 (Inlay/Crown)",
            "fdi": "26",
            "quadrant": "Q2 (상악 좌측)",
            "category": "restoration",
            "x1": 840, "y1": 235, "x2": 905, "y2": 285,
            "confidence": 0.85,
            "verified": False,
            "notes": "상악 좌측 제1대구치 수복 소견"
        },

        # Lower Left / Q3 (Patient Left = Screen Right)
        {
            "id": "box_pa1",
            "label": "치근단 병소 (Dental_012 실측 모델 원시 출력)",
            "fdi": "36 or 37 Apex",
            "quadrant": "Q3 (하악 좌측)",
            "category": "periapical",
            "x1": 912, "y1": 417, "x2": 942, "y2": 448, # Exact model detection raw coords
            "confidence": 0.541,
            "verified": False,
            "notes": "Dental_012 원시 YOLO11s 출력 좌표 [912, 417, 942, 448]. 화면 우측 하단이므로 환자 좌측 하악(Q3) #36 or #37 Apex임!"
        },
        {
            "id": "box_r36",
            "label": "#36 수복물 (Crown)",
            "fdi": "36",
            "quadrant": "Q3 (하악 좌측)",
            "category": "restoration",
            "x1": 830, "y1": 320, "x2": 895, "y2": 375,
            "confidence": 0.88,
            "verified": False,
            "notes": "하악 좌측 제1대구치 보철 소견"
        }
    ]

@app.get("/api/images/thegem")
def get_thegem_image():
    if os.path.exists(THEGEM_IMG_PATH):
        return FileResponse(THEGEM_IMG_PATH, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="TheGem Image not found")

@app.get("/api/metadata")
def get_metadata():
    boxes = get_initial_boxes()
    if os.path.exists(ANNOTATIONS_FILE):
        try:
            with open(ANNOTATIONS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                boxes = saved.get("boxes", boxes)
        except Exception:
            pass

    return {
        "image_id": "panoramic-x-ray-thegem-blog-default.jpg",
        "sha256": THEGEM_SHA256,
        "width": THEGEM_WIDTH,
        "height": THEGEM_HEIGHT,
        "coordinate_system": "pixel_xyxy",
        "patient_orientation": {
            "screen_left": "Patient Right (Q1 / Q4)",
            "screen_right": "Patient Left (Q2 / Q3)"
        },
        "boxes": boxes
    }

@app.post("/api/save_annotations")
def save_annotations(payload: AnnotationSavePayload):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(ANNOTATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(payload.dict(), f, indent=2, ensure_ascii=False)
        
    return {"status": "SUCCESS", "path": ANNOTATIONS_FILE, "count": len(payload.boxes)}

@app.post("/api/save_criteria")
def save_criteria(data: CriteriaModel):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, "clinical_criteria_v1.json")
    md_path = os.path.join(OUTPUT_DIR, "clinical_criteria_v1.md")
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data.dict(), f, indent=2, ensure_ascii=False)
        
    md_content = f"""# [ 260928 치과 임상 라벨 및 판정 기준표 (v1.0 SSOT) ]

- 확정자: {data.confirmed_by}
- 확정 일시: 2026-09-28 KST
- 목적: Dental_008, 012, 013, 009 파이프라인 수정(3단계) 및 메인 워크스테이션 재학습(5단계) 공통 기준

---

## 1. Dental_008 과잉치(Supernumerary) 라벨링 정책
- 표기 원칙: [{data.supernumerary_policy}]
- 치식 명명 체계: {data.supernumerary_naming}
- 임상 세부 지침:
  {data.supernumerary_notes}

## 2. Dental_012 치근단 병소 임상 임계치 및 검토 필요 게이트
- 확정 병소 기준선 (Definite Lesion): Confidence >= {data.periapical_threshold_definite:.2f}
- 검토 필요 유보 구간 (Review Required): {data.periapical_threshold_review:.2f} <= Confidence < {data.periapical_threshold_definite:.2f}
- 음성 배제 구간 (Background / Skip): Confidence < {data.periapical_threshold_review:.2f}
- 정상 해부학적 구조(상악동, 이공) 가드 적용 여부: {data.periapical_anatomical_guard}
- 임상 세부 지침:
  {data.periapical_notes}

## 3. Dental_013 수복물/보철물 4대 임상 분류 매핑 체계
- 확정 4대 핵심 범주: {', '.join(data.restoration_classes)}
- 상세 매핑 정의:
"""
    for src_cls, target_cls in data.restoration_mapping.items():
        md_content += f"- `{src_cls}` -> [{target_cls}]\n"
        
    md_content += f"""
- 임상 세부 지침:
  {data.restoration_notes}

---
상기 기준표는 2단계 임상 라벨 확정 절차를 통해 생성되었으며, 향후 모든 데이터 어노테이션, 파이프라인 통합 및 독립 평가의 절대 기준으로 사용됩니다.
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    return {"status": "SUCCESS", "json_path": json_path, "md_path": md_path}

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    html_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Clinical Criteria Review Tool</h1><p>Static index.html not found.</p>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8088, reload=False)
