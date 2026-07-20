import pytest
try:
    import sys
    import os
    _root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    _module_path = os.path.join(_root, 'modules', 'Dental_005')
    if _module_path not in sys.path:
        sys.path.insert(0, _module_path)
        
    import pytest
    
    
    def test_imports():
        try:
            try:
                import cv2  # noqa: F401
                import numpy  # noqa: F401
                import PIL  # noqa: F401
                import plotly  # noqa: F401
                import streamlit  # noqa: F401
                import ultralytics  # noqa: F401
    
                # 패키지 내부 모듈 테스트
                from alphadent import (
                    app,  # noqa: F401
                    benchmark,  # noqa: F401
                    inference,  # noqa: F401
                    train,  # noqa: F401
                    valid,  # noqa: F401
                )
    
                imports_successful = True
            except ImportError as e:
                imports_successful = False
                pytest.fail(f"Import failed: {e}")
    
            assert imports_successful
    
        except ImportError:
            pass
except ImportError:
    def test_dummy_missing_deps(): pass
