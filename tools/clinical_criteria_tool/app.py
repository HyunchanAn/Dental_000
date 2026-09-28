import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List

app = FastAPI(title="Dental Clinical Criteria Review Tool")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../plans_replies_walkthrough"))

THEGEM_IMG_PATH = "D:/Github/Dental_015/example_panorama/panoramic-x-ray-thegem-blog-default.jpg"
SAMPLE_IMG_PATH = "D:/Github/Dental_015/public/sample_panorama.png"

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

@app.get("/api/images/{name}")
def get_image(name: str):
    if name == "thegem":
        if os.path.exists(THEGEM_IMG_PATH):
            return FileResponse(THEGEM_IMG_PATH, media_type="image/jpeg")
    elif name == "sample":
        if os.path.exists(SAMPLE_IMG_PATH):
            return FileResponse(SAMPLE_IMG_PATH, media_type="image/png")
    raise HTTPException(status_code=404, detail="Image not found")

@app.get("/api/sample_data")
def get_sample_data():
    return {
        "thegem": {
            "image_url": "/api/images/thegem",
            "name": "TheGem Panoramic Case (대표 경계 사례)",
            "width": 1170,
            "height": 540,
            "annotations": {
                "supernumerary_cases": [
                    {"id": "sn1", "label": "과잉치 후보 (#18 인접)", "x": 0.08, "y": 0.42, "w": 0.045, "h": 0.09, "type": "supernumerary"},
                    {"id": "sn2", "label": "과잉치 후보 (#28 인접)", "x": 0.88, "y": 0.43, "w": 0.045, "h": 0.09, "type": "supernumerary"},
                ],
                "impaction_cases": [
                    {"id": "m18", "label": "#18 매복 대구치", "x": 0.12, "y": 0.44, "w": 0.05, "h": 0.085, "type": "impaction", "status": "Impacted (User Ground Truth)"},
                    {"id": "m28", "label": "#28 매복 대구치", "x": 0.84, "y": 0.45, "w": 0.05, "h": 0.085, "type": "impaction", "status": "Vertical/Partially Erupted"},
                    {"id": "m48", "label": "#48 수평 매복", "x": 0.14, "y": 0.62, "w": 0.055, "h": 0.09, "type": "impaction", "status": "Horizontal / Deep Impacted"},
                ],
                "periapical_cases": [
                    {"id": "pa1", "label": "치근단 병소 검출부 (conf 0.54)", "x": 0.779, "y": 0.772, "w": 0.025, "h": 0.058, "type": "periapical", "conf": 0.541, "fdi": "46 or 47 apex"},
                    {"id": "norm_mental", "label": "정상 하악 이공 (Mental Foramen - 오탐 위험)", "x": 0.28, "y": 0.73, "w": 0.03, "h": 0.04, "type": "normal_anatomy", "conf": 0.32},
                    {"id": "norm_sinus", "label": "상악동 저 (Maxillary Sinus Floor - 음영)", "x": 0.32, "y": 0.48, "w": 0.06, "h": 0.05, "type": "normal_anatomy", "conf": 0.28},
                ],
                "restoration_cases": [
                    {"id": "r1", "label": "#16 수복물 (Crown)", "x": 0.23, "y": 0.46, "w": 0.045, "h": 0.06, "type": "crown"},
                    {"id": "r2", "label": "#26 수복물 (Inlay)", "x": 0.73, "y": 0.46, "w": 0.042, "h": 0.055, "type": "inlay"},
                    {"id": "r3", "label": "#36 수복물 (Crown)", "x": 0.72, "y": 0.60, "w": 0.045, "h": 0.065, "type": "crown"},
                    {"id": "r4", "label": "#46 잔존 수복 / 결손 인접", "x": 0.24, "y": 0.61, "w": 0.045, "h": 0.065, "type": "missing_or_crown"},
                ]
            }
        }
    }

@app.post("/api/save_criteria")
def save_criteria(data: CriteriaModel):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, "clinical_criteria_v1.json")
    md_path = os.path.join(OUTPUT_DIR, "clinical_criteria_v1.md")
    
    # Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data.dict(), f, indent=2, ensure_ascii=False)
        
    # Save Markdown
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

# Mount static files if present
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
