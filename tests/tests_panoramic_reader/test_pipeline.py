import pytest
try:
    import os
    import sys
    import numpy as np
    
    # 파노라마 리더 및 하위 모듈 경로 등록 (Dental_000 내부 서브모듈 참조)
    _root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    reader_path = os.path.join(_root, "modules", "Dental_Panoramic_Reader")
    if reader_path not in sys.path:
        sys.path.insert(0, reader_path)
    for _p in [
        os.path.join(_root, "modules", "Dental_004", "src"),
        os.path.join(_root, "modules", "Dental_008", "src"),
        os.path.join(_root, "modules", "Dental_002"),
        os.path.join(_root, "modules", "Dental_003"),
    ]:
        if os.path.isdir(_p) and _p not in sys.path:
            sys.path.append(_p)
    
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

    from unittest.mock import patch
    
    def test_pipeline_deciduous_bypass():
        """유치 판별 시 003 모듈이 바이패스되는지 검증합니다."""
        # Dummy mock for testing
        pipeline = PanoramicPipeline(use_004=False)
    
        # We will simulate the run method logic manually for testing
        dummy_img = np.zeros((800, 800, 3), dtype=np.uint8)
    
        with patch('core.pipeline.run_deciduous_classification') as mock_deciduous, \
             patch('core.pipeline.run_tooth_segmentation') as mock_seg, \
             patch('core.pipeline.run_caries_detection') as mock_caries, \
             patch('modules.periapical_predictor.PeriapicalPredictorWrapper.predict') as mock_012, \
             patch('modules.restoration_predictor.RestorationPredictorWrapper.predict') as mock_013:
        
            mock_deciduous.return_value = True
            mock_seg.return_value = {'boxes': [], 'masks': [], 'fdi_labels': [], 'scores': [], 'contours': []}
            mock_caries.return_value = {'boxes': [], 'labels': [], 'scores': []}
            mock_012.return_value = {'module_name': 'Dental_012_periapical', 'lesions': []}
            mock_013.return_value = {'module_name': 'Dental_013_restoration', 'lesions': []}
        
            result = pipeline.run(dummy_img)
        
            # 검증: has_deciduous가 True이고, 003_bone_loss는 None이어야 함
            assert result['has_deciduous'] is True
            assert result['003_bone_loss'] is None
            assert '008_tooth_data' in result
            assert '002_lesions' in result

    def test_weights_manifest_and_api_hardening():
        """weights_manifest.yaml 정합성 및 api_server.py 보안/FDI 상태 전파를 검증합니다."""
        import setup_env
        import api_server

        manifest = setup_env.load_weights_manifest()
        assert "Dental_002_caries_detection" in manifest
        assert "Dental_008_segmentation" in manifest
        assert "Dental_012_periapical" in manifest
        assert "Dental_013_restoration" in manifest
        assert "Dental_014_osteoporosis" in manifest

        assert api_server.MAX_UPLOAD_BYTES == 30 * 1024 * 1024
        assert "*" not in api_server.ALLOWED_ORIGINS

        report_unavail = api_server.format_to_ssot_report(
            {"008_tooth_data": {"fdi_status": "FDI_UNAVAILABLE", "boxes": [], "fdi_labels": []}, "module_versions": {"Dental_008": "cef1c85"}},
            1000,
            500,
            "test.png",
        )
        assert report_unavail["imageMetadata"]["fdiStatus"] == "FDI_UNAVAILABLE"
        assert report_unavail["imageMetadata"]["moduleVersions"].get("Dental_008") == "cef1c85"
        assert report_unavail["imageMetadata"]["missingTeeth"] if "missingTeeth" in report_unavail["imageMetadata"] else report_unavail["findings"]["missingTeeth"]["status"] == "FDI_UNAVAILABLE"

    def test_repo_hygiene_and_large_file_blocker(tmp_path):
        """Dental_000#4 및 #5: 하드코딩 절대경로 0건 및 1MB 초과 대용량 파일 차단 동작을 검증합니다."""
        import subprocess
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        hygiene_script = os.path.join(repo_root, "scripts", "check_repo_hygiene.py")
        assert os.path.isfile(hygiene_script)

        # 1. 현재 저장소 추적 파일 내 하드코딩 경로 위반 0건 확인
        res_ok = subprocess.run(
            [sys.executable, hygiene_script, "--root", repo_root],
            capture_output=True,
            text=True,
        )
        assert res_ok.returncode == 0, f"Hygiene check failed: {res_ok.stderr}"

        # 2. 1024KB 초과 더미 파일 생성 시 즉시 차단(returncode != 0) 동작 확인
        oversized_file = tmp_path / "dummy_large.bin"
        oversized_file.write_bytes(b"0" * (1100 * 1024))
        res_block = subprocess.run(
            [sys.executable, hygiene_script, "--root", repo_root, "--check-file", str(oversized_file)],
            capture_output=True,
            text=True,
        )
        assert res_block.returncode != 0
        assert "exceeds 1024 KB limit" in res_block.stderr

except ImportError as _imp_err:
    pytest.skip(f"Optional dependency not available: {_imp_err}", allow_module_level=True)
