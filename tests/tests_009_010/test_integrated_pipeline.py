import os
import sys
import numpy as np
import pytest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

for cand in (
    os.path.join(ROOT_DIR, "modules", "Dental_009", "src"),
    os.path.join(ROOT_DIR, "modules", "Dental_010", "src"),
    os.path.abspath(os.path.join(ROOT_DIR, "..", "Dental_009", "src")),
    os.path.abspath(os.path.join(ROOT_DIR, "..", "Dental_010", "src")),
    os.path.abspath(os.path.join(ROOT_DIR, "..", "src")),
):
    if os.path.isdir(cand) and cand not in sys.path:
        sys.path.insert(0, cand)

from analyzer import ImpactedToothAnalyzer
from detector import MissingToothDetector


def test_impacted_tooth_analyzer_geometry():
    analyzer = ImpactedToothAnalyzer()
    # Vertical adjacent 2nd molar (#47) contour
    molar_47 = np.array(
        [[[400, 300]], [[440, 300]], [[440, 400]], [[400, 400]]],
        dtype=np.int32,
    )
    # Mesioangular impacted 3rd molar (#48) contour tilted toward #47
    molar_48 = np.array(
        [[[350, 330]], [[390, 310]], [[410, 390]], [[370, 410]]],
        dtype=np.int32,
    )
    res = analyzer.analyze_impacted_tooth(molar_48, 48, molar_47)
    assert "error" not in res
    assert "winters_class" in res
    assert "eruption_status" in res


def test_missing_tooth_detector_and_gap_verification():
    detector = MissingToothDetector()
    present_fdi = [
        17, 16, 15, 14, 13, 12, 11,
        21, 22, 23, 24, 25, 26, 27,
        37, 36, 35, 34, 33, 32, 31,
        41, 42, 43, 44, 47,
    ]
    res = detector.detect(present_fdi)
    assert 45 in res["missing_teeth"]
    assert 46 in res["missing_teeth"]
    assert res["supernumerary_or_error"] == []
