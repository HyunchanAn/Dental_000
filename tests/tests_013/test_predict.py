import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, "../../modules/Dental_013/src")))

def test_imports():
    import predict
    assert predict is not None
