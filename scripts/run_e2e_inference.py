import cv2
import sys
import os
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
from config.paths import resolve_module_dir

reader_path = str(resolve_module_dir("Dental_Panoramic_Reader"))
if reader_path not in sys.path:
    sys.path.append(reader_path)

from core.pipeline import PanoramicPipeline

def run_test():
    img_path = os.path.join(reader_path, 'reports_archive', 'images', 'eval_permanent.jpg')
    img = cv2.imread(img_path)
    if img is None:
        print("Image not found")
        return
        
    pipeline = PanoramicPipeline(use_004=False)
    results = pipeline.run(img)
    
    print("Inference completed!")
    print(f"Deciduous detected: {results.get('has_deciduous')}")
    print(f"008 Tooth Data found: {len(results.get('008_tooth_data', {}).get('boxes', []))} teeth")
    print(f"002 Caries Data found: {len(results.get('002_lesions', []))} lesions")
    print(f"012 Periapical Data found: {len(results.get('012_periapical', {}).get('lesions', []))} lesions")
    print(f"013 Restoration Data found: {len(results.get('013_restoration', {}).get('lesions', []))} lesions")

if __name__ == '__main__':
    run_test()
