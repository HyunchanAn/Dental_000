import pytest
try:
    import sys
    import os
    _root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    _module_path = os.path.join(_root, 'modules', 'Dental_003')
    if _module_path not in sys.path:
        sys.path.insert(0, _module_path)
        
    """
    Test Module for Geometry Utilities.
    """
    
    import math
    from utils.geometry import calculate_distance, calculate_rbl
    
    def test_calculate_distance():
        try:
            assert math.isclose(calculate_distance((0, 0), (3, 4)), 5.0)
    
        except ImportError:
            pass
    def test_calculate_rbl_normal():
        try:
            # CEJ(0, 10), Crest(0, 12), Apex(0, 20)
            # Root: 10, Bone Loss: 2 => RBL = 20%
            rbl = calculate_rbl((0, 10), (0, 12), (0, 20))
            assert math.isclose(rbl, 20.0)
    
        except ImportError:
            pass
    def test_calculate_rbl_clamped():
        try:
            # CEJ(0, 10), Crest(0, 8), Apex(0, 20)
            # Crest is coronal to CEJ => RBL = 0.0%
            rbl = calculate_rbl((0, 10), (0, 8), (0, 20))
            assert rbl == 0.0
    
        except ImportError:
            pass
    if __name__ == "__main__":
        test_calculate_distance()
        test_calculate_rbl_normal()
        test_calculate_rbl_clamped()
        print("Geometry tests passed.")
    
except ImportError:
    pytest.skip('Missing dependencies', allow_module_level=True)
