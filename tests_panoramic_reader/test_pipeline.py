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
