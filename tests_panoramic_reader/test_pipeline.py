import os
import sys
import numpy as np

# 파노라마 리더 경로 등록
reader_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Dental_Panoramic_Reader"))
if reader_path not in sys.path:
    sys.path.append(reader_path)

from core.pipeline import PanoramicPipeline

def test_pipeline_initialization():
    """오케스트레이터 파이프라인이 OOM 없이 정상적으로 초기화되는지 검증합니다."""
    try:
        pipeline = PanoramicPipeline(use_004=False)
        assert pipeline is not None
        assert "008" in pipeline.manager.models
        assert "008_classifier" in pipeline.manager.models
        assert "002" in pipeline.manager.models
    except Exception as e:
        assert False, f"파이프라인 초기화 중 에러 발생: {e}"

def test_fdi_mapping_logic():
    """008의 치아 BBox와 002의 병소 BBox 간의 기하학적 매핑 로직을 검증합니다."""
    pipeline = PanoramicPipeline(use_004=False)
    
    # Mock Data
    caries_data = {
        'boxes': [[100, 100, 200, 200], [300, 300, 400, 400]],
        'labels': ['Caries', 'Impacted'],
        'scores': [0.9, 0.8]
    }
    
    tooth_data = {
        'boxes': [[90, 90, 210, 210], [500, 500, 600, 600]],
        'masks': [None, None],
        'fdi_labels': ['46', '36'],
        'scores': [0.95, 0.99]
    }
    
    # 46번 치아(90~210)가 Caries(100~200)을 완벽히 포함하므로 매핑되어야 함
    mapped = pipeline._map_lesions_to_fdi(caries_data, tooth_data)
    
    assert len(mapped) == 2
    assert mapped[0]['lesion_type'] == 'Caries'
    assert mapped[0]['fdi'] == '46'
    
    # 두 번째 병소는 겹치는 치아가 없으므로 Unknown이어야 함
    assert mapped[1]['lesion_type'] == 'Impacted'
    assert mapped[1]['fdi'] == 'Unknown'

def test_pipeline_deciduous_bypass():
    """유치 판별 시 003 모듈이 바이패스되는지 검증합니다."""
    # Dummy mock for testing
    pipeline = PanoramicPipeline(use_004=False)
    
    # We will simulate the run method logic manually for testing
    dummy_img = np.zeros((800, 800, 3), dtype=np.uint8)
    
    # Override the deciduous classifier result for testing
    import core.interfaces.dental_008 as d008
    original_func = d008.run_deciduous_classification
    
    try:
        d008.run_deciduous_classification = lambda img, model, device: True
        
        # Override other models to return dummy data to avoid long inference
        original_seg = d008.run_tooth_segmentation
        d008.run_tooth_segmentation = lambda img, model, device: {'boxes': [], 'masks': [], 'fdi_labels': [], 'scores': []}
        
        import core.interfaces.dental_002 as d002
        original_caries = d002.run_caries_detection
        d002.run_caries_detection = lambda img, model: {'boxes': [], 'labels': [], 'scores': []}
        
        result = pipeline.run(dummy_img)
        
        # 검증: has_deciduous가 True이고, 003_bone_loss는 None이어야 함
        assert result['has_deciduous'] is True
        assert result['003_bone_loss'] is None
        assert '008_tooth_data' in result
        assert '002_lesions' in result
        
    finally:
        # Restore functions
        d008.run_deciduous_classification = original_func
        d008.run_tooth_segmentation = original_seg
        d002.run_caries_detection = original_caries
