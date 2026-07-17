import os
import json

def get_fdi_to_class_id():
    fdi_list = []
    for q in [1, 2, 3, 4]:
        for t in range(1, 9):
            fdi_list.append(q * 10 + t)
    for q in [5, 6, 7, 8]:
        for t in range(1, 6):
            fdi_list.append(q * 10 + t)
    fdi_to_id = {fdi: i+1 for i, fdi in enumerate(fdi_list)}
    id_to_fdi = {i+1: fdi for i, fdi in enumerate(fdi_list)}
    return fdi_to_id, id_to_fdi

def main():
    cache_dir = os.path.expanduser("~/.cache/dentex_dataset")
    json_path = os.path.join(cache_dir, "training_data/quadrant_enumeration/train_quadrant_enumeration.json")
    img_dir = os.path.join(cache_dir, "training_data/quadrant_enumeration/xrays")
    
    if not os.path.exists(json_path):
        print(f"DENTEX dataset JSON not found at {json_path}. Please ensure DENTEX is downloaded via Dental_008.")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        coco_data = json.load(f)
        
    images = {img['id']: img for img in coco_data['images']}
    img_to_anns = {}
    for ann in coco_data['annotations']:
        img_id = ann['image_id']
        if img_id not in img_to_anns:
            img_to_anns[img_id] = []
        img_to_anns[img_id].append(ann)
        
    fdi_to_id, id_to_fdi = get_fdi_to_class_id()
    
    wisdom_teeth = {18, 28, 38, 48}
    edge_cases = []
    
    for img_id, img_info in images.items():
        anns = img_to_anns.get(img_id, [])
        file_name = img_info['file_name']
        img_path = os.path.join(img_dir, file_name)
        
        valid_fdis = []
        parsed_anns = []
        
        for ann in anns:
            cat_1 = ann.get('category_id_1')
            cat_2 = ann.get('category_id_2')
            
            if cat_1 is not None and cat_2 is not None:
                fdi = (cat_1 + 1) * 10 + (cat_2 + 1)
                
                # Check for bbox or calculate from segmentation
                bbox = ann.get('bbox')
                if not bbox and 'segmentation' in ann and ann['segmentation']:
                    import numpy as np
                    poly = np.array(ann['segmentation'][0]).reshape(-1, 2)
                    xmin = np.min(poly[:, 0])
                    ymin = np.min(poly[:, 1])
                    xmax = np.max(poly[:, 0])
                    ymax = np.max(poly[:, 1])
                    bbox = [float(xmin), float(ymin), float(xmax - xmin), float(ymax - ymin)]
                
                if bbox:
                    parsed_anns.append({
                        "id": ann["id"],
                        "fdi": fdi,
                        "bbox": bbox,
                        "segmentation": ann.get('segmentation', [])
                    })
                    if fdi not in wisdom_teeth:
                        valid_fdis.append(fdi)
        
        unique_fdis = set(valid_fdis)
        if len(unique_fdis) != 28:
            edge_cases.append({
                "image_id": img_id,
                "file_name": file_name,
                "image_path": img_path,
                "tooth_count": len(unique_fdis),
                "annotations": parsed_anns
            })
            
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, "edge_cases_fdi.json")
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(edge_cases, f, indent=4)
        
    print(f"Total images processed: {len(images)}")
    print(f"Edge cases found (count != 28): {len(edge_cases)}")
    print(f"Saved edge cases to {out_path}")

if __name__ == "__main__":
    main()
