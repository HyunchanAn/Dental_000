import os
import sys
import pytest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

for cand in (
    os.path.join(ROOT_DIR, "modules", "Dental_012", "src"),
    os.path.abspath(os.path.join(ROOT_DIR, "..", "Dental_012", "src")),
    os.path.abspath(os.path.join(ROOT_DIR, "..", "src")),
    os.path.join(ROOT_DIR, "modules", "Dental_Panoramic_Reader"),
    os.path.abspath(os.path.join(ROOT_DIR, "..", "Dental_Panoramic_Reader")),
):
    if os.path.isdir(cand) and cand not in sys.path:
        sys.path.insert(0, cand)

from prepare_data import convert_to_yolo
from modules.periapical_predictor import PeriapicalPredictorWrapper


def test_convert_to_yolo_normalization():
    size = (1000, 500)
    # box format in prepare_data.py: (xmin, xmax, ymin, ymax)
    box = (100.0, 300.0, 50.0, 250.0)
    x, y, w, h = convert_to_yolo(size, box)
    assert pytest.approx(x, rel=1e-5) == 0.20
    assert pytest.approx(y, rel=1e-5) == 0.30
    assert pytest.approx(w, rel=1e-5) == 0.20
    assert pytest.approx(h, rel=1e-5) == 0.40


def test_periapical_apex_anchoring_and_anatomical_guard():
    wrapper = PeriapicalPredictorWrapper(model_path="nonexistent.pt")
    teeth_data = [
        {"fdi": 16, "bbox": [200, 150, 260, 280], "contour": None},  # Maxillary molar (apex near y=150)
        {"fdi": 36, "bbox": [700, 400, 760, 530], "contour": None},  # Mandibular molar (apex near y=530)
    ]
    lesions = [
        {
            "bbox": [710, 515, 750, 555],
            "confidence": 0.62,
            "clinical_status": "DEFINITE",
            "fdi": None,
            "isolated_anatomical_suspicion": False,
        },
        {
            "bbox": [50, 700, 90, 740],  # Isolated radiolucency far from any tooth apex
            "confidence": 0.35,
            "clinical_status": "REVIEW_REQUIRED",
            "fdi": None,
            "isolated_anatomical_suspicion": False,
        },
    ]
    wrapper._match_fdi(lesions, teeth_data, anatomical_guard=True)
    assert lesions[0]["fdi"] == 36
    assert lesions[0]["isolated_anatomical_suspicion"] is False
    assert lesions[1]["fdi"] is None
    assert lesions[1]["isolated_anatomical_suspicion"] is True
