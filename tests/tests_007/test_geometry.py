import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, "../../modules/Dental_007/src")))

def test_imports():
    import geometry
    import materials
    assert geometry is not None
