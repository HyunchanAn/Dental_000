import pytest
try:
    import os
    import sys
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(current_dir, "../../modules/Dental_007/src")))
    
    def test_imports():
        import geometry
        assert geometry is not None

except ImportError as _imp_err:
    pytest.skip(f"Optional dependency not available: {_imp_err}", allow_module_level=True)
