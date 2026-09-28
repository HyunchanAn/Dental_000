import os
import shutil
import json
from PIL import Image

DEST_DIR = "D:/Github/Dental_015/example_panorama"
os.makedirs(DEST_DIR, exist_ok=True)

manifest = {}

# 0. TheGem (Base Case)
thegem_src = "D:/Github/Dental_015/example_panorama/panoramic-x-ray-thegem-blog-default.jpg"
if os.path.exists(thegem_src):
    manifest["panoramic-x-ray-thegem-blog-default.jpg"] = {
        "module": "Composite",
        "desc": "TheGem 파노라마 종합 경계 사례 (과잉치/매복치/수복물/치근단)",
        "width": 1170,
        "height": 540,
        "is_default": True
    }

# 1. Dental_008 (DENTEX 치아 세그멘테이션 / FDI)
dentex_json = "C:/Users/chema/.cache/dentex_dataset/training_data/quadrant_enumeration/train_quadrant_enumeration.json"
dentex_dir = "C:/Users/chema/.cache/dentex_dataset/training_data/quadrant_enumeration/xrays"
if os.path.exists(dentex_json):
    with open(dentex_json, "r", encoding="utf-8") as f:
        dj = json.load(f)
    img_map = {img["id"]: img for img in dj["images"]}
    selected_img_ids = [dj["images"][0]["id"], dj["images"][1]["id"], dj["images"][2]["id"]]
    
    for idx, iid in enumerate(selected_img_ids, 1):
        info = img_map[iid]
        src_path = os.path.join(dentex_dir, info["file_name"])
        dest_name = f"case_008_dentex_{idx}_{info['file_name']}"
        dest_path = os.path.join(DEST_DIR, dest_name)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            
        boxes = []
        for ann in dj["annotations"]:
            if ann["image_id"] == iid:
                x1, y1, w, h = ann["bbox"]
                fdi_val = str(ann.get("category_id_2", ""))
                quad_val = str(ann.get("category_id_1", ""))
                
                # quadrant mapping
                quad_label = f"Q{quad_val}"
                if quad_val == "1": quad_label = "Q1 (상악 우측)"
                elif quad_val == "2": quad_label = "Q2 (상악 좌측)"
                elif quad_val == "3": quad_label = "Q3 (하악 좌측)"
                elif quad_val == "4": quad_label = "Q4 (하악 우측)"

                boxes.append({
                    "id": f"box_008_{idx}_{ann['id']}",
                    "label": f"치아 FDI-{quad_val}{fdi_val}",
                    "fdi": f"{quad_val}{fdi_val}",
                    "quadrant": quad_label,
                    "category": "supernumerary" if fdi_val == "9" else ("impaction" if fdi_val == "8" else "normal_tooth"),
                    "x1": round(x1),
                    "y1": round(y1),
                    "x2": round(x1 + w),
                    "y2": round(y1 + h),
                    "confidence": 1.0,
                    "verified": True,
                    "notes": f"DENTEX 원본 정답 (Q{quad_val}, #{quad_val}{fdi_val})"
                })
                
        manifest[dest_name] = {
            "module": "Dental_008",
            "desc": f"Dental_008 DENTEX 치열/치식 표준 사례 {idx} ({info['file_name']})",
            "width": info["width"],
            "height": info["height"],
            "boxes": boxes
        }
        print(f"Imported Dental_008 Case {idx}: {dest_name}, Boxes: {len(boxes)}")

# 2. Dental_012 (치근단 병소)
p12_img_dir = "D:/Github/Dental_012/data/yolo_dataset_augmented/images/val"
p12_lbl_dir = "D:/Github/Dental_012/data/yolo_dataset_augmented/labels/val"
p12_files = ["00071.jpg", "00091.jpg", "00131.jpg"]

for idx, fn in enumerate(p12_files, 1):
    src_img = os.path.join(p12_img_dir, fn)
    src_lbl = os.path.join(p12_lbl_dir, fn.replace(".jpg", ".txt"))
    dest_name = f"case_012_periapical_{idx}_{fn}"
    dest_path = os.path.join(DEST_DIR, dest_name)
    if os.path.exists(src_img):
        shutil.copy2(src_img, dest_path)
        img = Image.open(src_img)
        iw, ih = img.size
    else:
        iw, ih = 1024, 512

    boxes = []
    if os.path.exists(src_lbl):
        with open(src_lbl, "r") as lf:
            for l_idx, line in enumerate(lf):
                parts = line.strip().split()
                if len(parts) >= 5:
                    cx, cy, nw, nh = map(float, parts[1:5])
                    x1 = round((cx - nw / 2) * iw)
                    y1 = round((cy - nh / 2) * ih)
                    x2 = round((cx + nw / 2) * iw)
                    y2 = round((cy + nh / 2) * ih)
                    boxes.append({
                        "id": f"box_p12_{idx}_{l_idx}",
                        "label": "치근단 병소 (Periapical GT)",
                        "fdi": "Apex",
                        "quadrant": "Q3/Q4 (하악)" if cy > 0.5 else "Q1/Q2 (상악)",
                        "category": "periapical",
                        "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                        "confidence": 1.0,
                        "verified": True,
                        "notes": "Dental_012 검증셋 정답 레이블"
                    })
    manifest[dest_name] = {
        "module": "Dental_012",
        "desc": f"Dental_012 치근단 병소 표준 사례 {idx} ({fn})",
        "width": iw,
        "height": ih,
        "boxes": boxes
    }
    print(f"Imported Dental_012 Case {idx}: {dest_name}, Boxes: {len(boxes)}")

# 3. Dental_013 (수복물/보철물)
p13_img_dir = "D:/Github/Dental_013/data/raw/YOLO/YOLO/valid/images"
p13_lbl_dir = "D:/Github/Dental_013/data/raw/YOLO/YOLO/valid/labels"

if os.path.exists(p13_img_dir):
    p13_files = [f for f in os.listdir(p13_img_dir) if f.lower().endswith((".jpg", ".png"))][:3]
    for idx, fn in enumerate(p13_files, 1):
        src_img = os.path.join(p13_img_dir, fn)
        base_lbl = os.path.splitext(fn)[0] + ".txt"
        src_lbl = os.path.join(p13_lbl_dir, base_lbl)
        dest_name = f"case_013_restoration_{idx}.jpg"
        dest_path = os.path.join(DEST_DIR, dest_name)
        shutil.copy2(src_img, dest_path)

        img = Image.open(src_img)
        iw, ih = img.size
        boxes = []
        if os.path.exists(src_lbl):
            with open(src_lbl, "r") as lf:
                for l_idx, line in enumerate(lf):
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        cls_id = int(parts[0])
                        if len(parts) > 5:  # polygon
                            coords = [float(x) for x in parts[1:]]
                            xs = coords[0::2]
                            ys = coords[1::2]
                            x1 = round(min(xs) * iw)
                            x2 = round(max(xs) * iw)
                            y1 = round(min(ys) * ih)
                            y2 = round(max(ys) * ih)
                        else:  # bbox
                            cx, cy, nw, nh = map(float, parts[1:5])
                            x1 = round((cx - nw / 2) * iw)
                            y1 = round((cy - nh / 2) * ih)
                            x2 = round((cx + nw / 2) * iw)
                            y2 = round((cy + nh / 2) * ih)

                        # classify into 4 clinical groups
                        cat_label = "Inlay/Onlay"
                        if cls_id in [1, 2, 3]: cat_label = "Crown/Bridge"
                        elif cls_id in [4, 5]: cat_label = "Implant"
                        elif cls_id in [6, 7]: cat_label = "Endodontic (RCT)"

                        boxes.append({
                            "id": f"box_p13_{idx}_{l_idx}",
                            "label": f"수복물 [{cat_label}]",
                            "fdi": "",
                            "quadrant": "General",
                            "category": "restoration",
                            "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                            "confidence": 1.0,
                            "verified": True,
                            "notes": f"Dental_013 GT Class {cls_id} -> {cat_label}"
                        })
        manifest[dest_name] = {
            "module": "Dental_013",
            "desc": f"Dental_013 수복물/보철물 표준 사례 {idx}",
            "width": iw,
            "height": ih,
            "boxes": boxes
        }
        print(f"Imported Dental_013 Case {idx}: {dest_name}, Boxes: {len(boxes)}")

manifest_path = "D:/Github/Dental_015/example_panorama/cases_manifest.json"
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print("Saved cases manifest successfully.")
