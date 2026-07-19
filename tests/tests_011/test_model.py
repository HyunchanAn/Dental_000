import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, "../../modules/Dental_011/src")))

def test_imports():
    import model
    import dataset
    assert model is not None
