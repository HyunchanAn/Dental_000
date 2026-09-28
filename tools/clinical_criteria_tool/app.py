import os
import json
import hashlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

app = FastAPI(title="Dental Clinical Criteria & Multi-Case Review Tool")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../plans_replies_walkthrough"))
PANORAMA_DIR = "D:/Github/Dental_015/example_panorama"
MANIFEST_FILE = os.path.join(PANORAMA_DIR, "cases_manifest.json")

class AnnotationBox(BaseModel):
    id: str
    label: str
    fdi: Optional[str] = None
    quadrant: str
    category: str
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: Optional[float] = 1.0
    verified: bool = True
    notes: Optional[str] = ""

class AnnotationSavePayload(BaseModel):
    image_name: str
    image_sha256: Optional[str] = ""
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

def load_manifest():
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@app.get("/api/cases")
def get_cases():
    manifest = load_manifest()
    case_list = []
    
    # Put TheGem first
    if "panoramic-x-ray-thegem-blog-default.jpg" in manifest:
        case_list.append({
            "filename": "panoramic-x-ray-thegem-blog-default.jpg",
            "desc": manifest["panoramic-x-ray-thegem-blog-default.jpg"]["desc"],
            "module": manifest["panoramic-x-ray-thegem-blog-default.jpg"]["module"]
        })
        
    for fn, info in manifest.items():
        if fn != "panoramic-x-ray-thegem-blog-default.jpg":
            case_list.append({
                "filename": fn,
                "desc": info["desc"],
                "module": info["module"]
            })
    return case_list

@app.get("/api/case/{filename}")
def get_case_detail(filename: str):
    manifest = load_manifest()
    if filename not in manifest:
        raise HTTPException(status_code=404, detail="Case not found in manifest")
        
    img_path = os.path.join(PANORAMA_DIR, filename)
    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail="Image file missing")
        
    with open(img_path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
        
    info = manifest[filename]
    
    # Check if there is a saved verified annotation
    verified_file = os.path.join(OUTPUT_DIR, f"verified_{filename}.json")
    boxes = info.get("boxes", [])
    
    # Handle TheGem initial boxes if not in manifest boxes
    if filename == "panoramic-x-ray-thegem-blog-default.jpg" and not boxes:
        from app_legacy import get_thegem_boxes # fallback
        boxes = get_thegem_boxes()
        
    if os.path.exists(verified_file):
        try:
            with open(verified_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
                boxes = saved.get("boxes", boxes)
        except Exception:
            pass

    return {
        "filename": filename,
        "image_url": f"/api/images/{filename}",
        "sha256": sha,
        "width": info["width"],
        "height": info["height"],
        "desc": info["desc"],
        "module": info["module"],
        "boxes": boxes
    }

@app.get("/api/images/{filename}")
def get_image_file(filename: str):
    img_path = os.path.join(PANORAMA_DIR, filename)
    if os.path.exists(img_path):
        media = "image/png" if filename.lower().endswith(".png") else "image/jpeg"
        return FileResponse(img_path, media_type=media)
    raise HTTPException(status_code=404, detail="Image not found")

@app.post("/api/save_annotations")
def save_annotations(payload: AnnotationSavePayload):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_file = os.path.join(OUTPUT_DIR, f"verified_{payload.image_name}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload.dict(), f, indent=2, ensure_ascii=False)
        
    # Also update cases_manifest.json with modified boxes
    manifest = load_manifest()
    if payload.image_name in manifest:
        manifest[payload.image_name]["boxes"] = [b.dict() for b in payload.boxes]
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            
    return {"status": "SUCCESS", "path": out_file, "count": len(payload.boxes)}

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

# TheGem fallback boxes
def get_thegem_boxes():
    return [
        {"id": "box_sn1", "label": "과잉치 후보 (#18 인접)", "fdi": "SN-1", "quadrant": "Q1 (상악 우측)", "category": "supernumerary", "x1": 80, "y1": 205, "x2": 130, "y2": 265, "confidence": 0.45, "verified": False},
        {"id": "box_m18", "label": "#18 매복 대구치", "fdi": "18", "quadrant": "Q1 (상악 우측)", "category": "impaction", "x1": 120, "y1": 210, "x2": 190, "y2": 280, "confidence": 0.85, "verified": False},
        {"id": "box_m48", "label": "#48 수평 매복", "fdi": "48", "quadrant": "Q4 (하악 우측)", "category": "impaction", "x1": 130, "y1": 320, "x2": 215, "y2": 395, "confidence": 0.92, "verified": False},
        {"id": "box_r16", "label": "#16 수복물 (Crown)", "fdi": "16", "quadrant": "Q1 (상악 우측)", "category": "restoration", "x1": 260, "y1": 235, "x2": 325, "y2": 285, "confidence": 0.90, "verified": False},
        {"id": "box_sinus", "label": "상악동 저 음영 (정상)", "fdi": None, "quadrant": "Q1 (상악 우측)", "category": "normal_anatomy", "x1": 350, "y1": 240, "x2": 430, "y2": 285, "confidence": 0.28, "verified": False},
        {"id": "box_mental", "label": "하악 이공 (Mental Foramen)", "fdi": None, "quadrant": "Q4 (하악 우측)", "category": "normal_anatomy", "x1": 340, "y1": 380, "x2": 385, "y2": 425, "confidence": 0.32, "verified": False},
        {"id": "box_sn2", "label": "과잉치 후보 (#28 인접)", "fdi": "SN-2", "quadrant": "Q2 (상악 좌측)", "category": "supernumerary", "x1": 1025, "y1": 210, "x2": 1080, "y2": 270, "confidence": 0.42, "verified": False},
        {"id": "box_m28", "label": "#28 매복 대구치", "fdi": "28", "quadrant": "Q2 (상악 좌측)", "category": "impaction", "x1": 970, "y1": 215, "x2": 1040, "y2": 290, "confidence": 0.88, "verified": False},
        {"id": "box_r26", "label": "#26 수복물 (Inlay)", "fdi": "26", "quadrant": "Q2 (상악 좌측)", "category": "restoration", "x1": 840, "y1": 235, "x2": 905, "y2": 285, "confidence": 0.85, "verified": False},
        {"id": "box_pa1", "label": "치근단 병소 (012 원시 출력)", "fdi": "36 or 37 Apex", "quadrant": "Q3 (하악 좌측)", "category": "periapical", "x1": 912, "y1": 417, "x2": 942, "y2": 448, "confidence": 0.541, "verified": False},
        {"id": "box_r36", "label": "#36 수복물 (Crown)", "fdi": "36", "quadrant": "Q3 (하악 좌측)", "category": "restoration", "x1": 830, "y1": 320, "x2": 895, "y2": 375, "confidence": 0.88, "verified": False}
    ]

# Populate TheGem boxes in manifest if missing
manifest_init = load_manifest()
if "panoramic-x-ray-thegem-blog-default.jpg" in manifest_init:
    if "boxes" not in manifest_init["panoramic-x-ray-thegem-blog-default.jpg"] or not manifest_init["panoramic-x-ray-thegem-blog-default.jpg"]["boxes"]:
        manifest_init["panoramic-x-ray-thegem-blog-default.jpg"]["boxes"] = get_thegem_boxes()
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(manifest_init, f, indent=2, ensure_ascii=False)

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    html_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Clinical Criteria Review Tool</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8088, reload=False)
