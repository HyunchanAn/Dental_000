import pytest


def test_imports():
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
