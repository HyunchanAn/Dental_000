import pytest
try:
    import sys
    import os
    import cv2
    import time
    from tqdm import tqdm
    
    # Add module paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(os.path.join(BASE_DIR, 'Dental_008', 'src'))
    sys.path.append(os.path.join(BASE_DIR, 'Dental_Panoramic_Reader'))
    
    from dentex_seg.dataset import DENTEXDataset
    from modules.segmentation_predictor import SegmentationPredictorWrapper
    from modules.missing_tooth_predictor import MissingToothPredictorWrapper
    from modules.impacted_tooth_predictor import ImpactedToothPredictorWrapper
    
    def main():
        print("========================================")
        print("DENTEX 008->010->009 E2E Pipeline Benchmark")
        print("========================================")
        
        # Initialize Predictors
        yolo_weight_path = os.path.join(BASE_DIR, 'Dental_000', 'yolov8m_seg_scratch', 'weights', 'best.pt')
        seg_predictor = SegmentationPredictorWrapper(model_path=yolo_weight_path)
        missing_predictor = MissingToothPredictorWrapper()
        impacted_predictor = ImpactedToothPredictorWrapper()
        
        dataset_val = DENTEXDataset(split='val')
        num_eval = len(dataset_val)
        print(f"Total Validation Images: {num_eval}")
        
        total_time = 0
        total_images_processed = 0
        total_missing_teeth_detected = 0
        total_supernumerary_detected = 0
        total_impacted_analyzed = 0
        impacted_class_counts = {}
        
        for idx in tqdm(range(num_eval)):
            img_id = dataset_val.img_ids[idx]
            img_info = dataset_val.images[img_id]
            img_path = os.path.join(dataset_val.img_dir, img_info['file_name'])
            
            cv_img = cv2.imread(img_path)
            if cv_img is None: continue
                
            start_time = time.time()
            
            # 1. Segmentation & FDI (008)
            seg_res = seg_predictor.predict(cv_img, conf=0.5, iou=0.4)
            teeth_data = seg_res.get('teeth', [])
            fdi_list = [t['fdi'] for t in teeth_data]
            
            # 2. Missing Teeth (010)
            missing_res = missing_predictor.predict(cv_img, fdi_list=fdi_list)
            
            # 3. Impacted Teeth (009)
            impacted_res = impacted_predictor.predict(cv_img, teeth_data=teeth_data)
            
            end_time = time.time()
            
            total_time += (end_time - start_time)
            total_images_processed += 1
            
            total_missing_teeth_detected += len(missing_res['missing_teeth'])
            total_supernumerary_detected += len(missing_res['supernumerary_or_error'])
            
            for imp in impacted_res['impacted_analysis']:
                total_impacted_analyzed += 1
                w_class = imp.get('winters_class', 'Unknown')
                impacted_class_counts[w_class] = impacted_class_counts.get(w_class, 0) + 1
                
        avg_time = total_time / total_images_processed if total_images_processed > 0 else 0
        
        print("\n========================================")
        print("Benchmark Results Summary:")
        print(f"Processed Images: {total_images_processed}")
        print(f"Avg Inference Time (Full Pipeline): {avg_time:.4f} s/image")
        print(f"Avg Missing Teeth per Image: {total_missing_teeth_detected/total_images_processed:.2f}")
        print(f"Avg Supernumerary/FP per Image: {total_supernumerary_detected/total_images_processed:.2f}")
        print(f"Total Impacted 3rd Molars Analyzed: {total_impacted_analyzed}")
        for k, v in impacted_class_counts.items():
            print(f"  - {k}: {v}")
        print("========================================")
    
    if __name__ == '__main__':
        main()
    
except ImportError:
    pytest.skip('Missing dependencies', allow_module_level=True)
