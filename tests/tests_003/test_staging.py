import sys
import os
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_module_path = os.path.join(_root, 'modules', 'Dental_003')
if _module_path not in sys.path:
    sys.path.insert(0, _module_path)
    
"""
Test Module for Staging Logic.
"""

from services.staging import determine_patient_stage, Stage, Extent

def test_staging_stage_i_localized():
    try:
        metrics = [{"tooth": 11, "max_rbl": 10.0}, {"tooth": 12, "max_rbl": 5.0}]
        stage, extent = determine_patient_stage(metrics)
        assert stage == Stage.STAGE_I
        assert extent == Extent.LOCALIZED

    except ImportError:
        pass
def test_staging_stage_iv_generalized():
    try:
        # 4개 치아 중 2개가 15% 이상(50%), 최고 RBL 35% + severe complexity
        metrics = [
            {"tooth": 11, "max_rbl": 35.0},
            {"tooth": 12, "max_rbl": 20.0},
            {"tooth": 21, "max_rbl": 5.0},
            {"tooth": 22, "max_rbl": 5.0}
        ]
        stage, extent = determine_patient_stage(metrics, has_severe_complexity=True)
        assert stage == Stage.STAGE_IV
        assert extent == Extent.GENERALIZED

    except ImportError:
        pass
if __name__ == "__main__":
    test_staging_stage_i_localized()
    test_staging_stage_iv_generalized()
    print("Staging tests passed.")
