import streamlit as st
import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

st.set_page_config(page_title="FDI HiTL Labeler", layout="wide")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
if not os.path.exists(DATA_DIR):
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
EDGE_CASES_PATH = os.path.join(DATA_DIR, "edge_cases_fdi.json")
CORRECTED_LABELS_PATH = os.path.join(DATA_DIR, "corrected_fdi_labels.json")

@st.cache_data
def load_edge_cases():
    if not os.path.exists(EDGE_CASES_PATH):
        return []
    with open(EDGE_CASES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_corrected_labels():
    if not os.path.exists(CORRECTED_LABELS_PATH):
        return {}
    with open(CORRECTED_LABELS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_corrected_labels(labels):
    with open(CORRECTED_LABELS_PATH, 'w', encoding='utf-8') as f:
        json.dump(labels, f, indent=4)

edge_cases = load_edge_cases()

if not edge_cases:
    st.error("Edge cases JSON not found. Please run scripts/batch_fdi_filter.py first.")
    st.stop()

if 'corrected_labels' not in st.session_state:
    st.session_state.corrected_labels = load_corrected_labels()

if 'current_idx' not in st.session_state:
    start_idx = 0
    for i, case in enumerate(edge_cases):
        if str(case['image_id']) not in st.session_state.corrected_labels:
            start_idx = i
            break
    st.session_state.current_idx = start_idx

def next_image():
    st.session_state.current_idx = min(st.session_state.current_idx + 1, len(edge_cases) - 1)
def prev_image():
    st.session_state.current_idx = max(st.session_state.current_idx - 1, 0)

st.title("🦷 치식 번호 교정기 (HiTL FDI Labeler) - DENTEX Dataset")
st.markdown("정상 치열 28개가 아닌 엣지 케이스들을 검수하고 올바른 FDI 번호로 매핑을 교정해 주세요.")

idx = st.session_state.current_idx
if idx >= len(edge_cases):
    st.success("🎉 모든 이미지 검수가 완료되었습니다!")
    st.stop()

case = edge_cases[idx]
img_id_str = str(case['image_id'])

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.button("⬅️ 이전", on_click=prev_image, use_container_width=True)
with col2:
    st.write(f"[진행 상황]: {idx + 1} / {len(edge_cases)} (치아 개수: {case['tooth_count']}개, 파일: {case['file_name']})")
with col3:
    st.button("다음 ➡️", on_click=next_image, use_container_width=True)

# Image and Box rendering
img_path = case['image_path']
if not os.path.exists(img_path):
    alt_img_path = os.path.join(BASE_DIR, "..", "Dental_015", "example_panorama", f"case_008_dentex_1_{case['file_name']}")
    if os.path.exists(alt_img_path):
        img_path = alt_img_path
try:
    img = Image.open(img_path).convert("RGB")
except Exception:
    st.error(f"이미지를 불러올 수 없습니다: {img_path}")
    st.stop()

fig, ax = plt.subplots(figsize=(12, 8))
ax.imshow(img)

# Pre-fill with corrected labels if they exist, else use original
current_annotations = st.session_state.corrected_labels.get(img_id_str, case['annotations'])

import numpy as np
# Dental_008 모델을 통한 정밀 마스킹을 위해 YOLO 로드
try:
    from ultralytics import YOLO
except ImportError:
    st.error("ultralytics 패키지가 필요합니다.")
    st.stop()

@st.cache_resource
def load_yolo_model():
    # 008 모듈의 정규 치아 분할 YOLOv8-seg 가중치 경로 탐색
    candidate_paths = [
        os.path.abspath(os.path.join(BASE_DIR, "..", "Dental_008", "weights", "yolov8m_best.pt")),
        os.path.abspath(os.path.join(BASE_DIR, "..", "Dental_Panoramic_Reader", "modules", "Dental_008", "models", "yolov8m_best.pt")),
        os.path.abspath(os.path.join(BASE_DIR, "submodules", "Dental_008", "weights", "yolov8m_best.pt")),
    ]
    for model_path in candidate_paths:
        if os.path.exists(model_path):
            return YOLO(model_path)
    st.warning(f"YOLO 치아 분할 모델을 찾을 수 없습니다: {candidate_paths[0]}")
    return None

yolo_model = load_yolo_model()

def calculate_iou(box1, box2):
    # box: [x, y, w, h]
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    xA, yA = max(x1, x2), max(y1, y2)
    xB, yB = min(x1+w1, x2+w2), min(y1+h1, y2+h2)
    interArea = max(0, xB - xA) * max(0, yB - yA)
    if interArea == 0:
        return 0
    box1Area = w1 * h1
    box2Area = w2 * h2
    return interArea / float(box1Area + box2Area - interArea)

def extract_annotation_polygon(ann):
    seg = ann.get("segmentation")
    if isinstance(seg, list) and len(seg) > 0 and len(seg[0]) >= 6:
        pts = np.array(seg[0], dtype=np.float32).reshape(-1, 2)
        return pts
    return None

masks = []
if yolo_model:
    results = yolo_model(img, verbose=False, conf=0.20, iou=0.50)
    masks = results[0].masks.xy if (results and results[0].masks is not None) else []

for i, ann in enumerate(current_annotations):
    ann_box = ann['bbox'] # [x, y, w, h]
    fdi = ann['fdi']
    
    # 1순위: 가장 많이 겹치는 YOLOv8-seg 실시간 추론 마스크 찾기
    best_iou = 0.0
    best_poly = None
    for poly in masks:
        if len(poly) >= 3:
            px, py = poly[:, 0], poly[:, 1]
            p_box = [float(np.min(px)), float(np.min(py)), float(np.max(px) - np.min(px)), float(np.max(py) - np.min(py))]
            iou = calculate_iou(ann_box, p_box)
            if iou > best_iou:
                best_iou = iou
                best_poly = poly

    # 2순위: 어노테이션 내 원본 segmentation 폴리곤 활용
    if best_poly is None or best_iou <= 0.1:
        best_poly = extract_annotation_polygon(ann)

    if best_poly is not None and len(best_poly) >= 3:
        poly_patch = patches.Polygon(best_poly, closed=True, facecolor='cyan', edgecolor='cyan', linewidth=1.5, alpha=0.25)
        ax.add_patch(poly_patch)
        cx, cy = float(np.mean(best_poly[:, 0])), float(np.mean(best_poly[:, 1]))
        ax.text(cx, cy, f"ID:{i}\nFDI:{fdi}", color='black', fontsize=8, weight='bold', ha='center', va='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2, boxstyle='round,pad=0.2'))
    else:
        x, y, w, h = ann_box
        rect = patches.Rectangle((x, y), w, h, linewidth=1.5, edgecolor='cyan', facecolor='cyan', alpha=0.2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, f"ID:{i}\nFDI:{fdi}", color='black', fontsize=8, weight='bold', ha='center', va='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2, boxstyle='round,pad=0.2'))


ax.axis('off')

# Display
col_img, col_form = st.columns([2, 1])
with col_img:
    st.pyplot(fig)

with col_form:
    st.subheader("FDI 번호 교정 폼")
    with st.form(key=f"form_{idx}"):
        new_annotations = []
        for i, ann in enumerate(current_annotations):
            # Selectbox might be better than number input for categorical FDI
            new_fdi = st.number_input(f"ID {i}의 올바른 FDI 번호", value=int(ann['fdi']), min_value=11, max_value=85, step=1, key=f"fdi_{i}")
            entry = {
                "id": ann["id"],
                "fdi": new_fdi,
                "bbox": ann['bbox']
            }
            if "segmentation" in ann:
                entry["segmentation"] = ann["segmentation"]
            new_annotations.append(entry)
            
        submitted = st.form_submit_button("💾 현재 라벨 저장 및 다음", use_container_width=True)
        if submitted:
            st.session_state.corrected_labels[img_id_str] = new_annotations
            save_corrected_labels(st.session_state.corrected_labels)
            st.success("성공적으로 저장되었습니다!")
            next_image()
            st.rerun()
