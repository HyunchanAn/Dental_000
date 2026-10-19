import ast
import os
import sys
import onnxruntime as ort
import pytest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DENTAL_013_SRC = os.path.abspath(os.path.join(CURRENT_DIR, "../../../Dental_013/src"))
READER_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../../Dental_Panoramic_Reader"))

for p in (DENTAL_013_SRC, READER_ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

import predict
from modules.restoration_predictor import RestorationPredictorWrapper


def test_dental_013_onnx_metadata_31_class_parity():
    onnx_path = os.path.join(READER_ROOT, "modules", "Dental_013", "models", "best_restoration_model.onnx")
    assert os.path.exists(onnx_path), f"Missing ONNX model at {onnx_path}"

    wrapper = RestorationPredictorWrapper(model_path=onnx_path)
    sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
    meta = sess.get_modelmeta().custom_metadata_map
    assert "names" in meta, "ONNX model metadata missing 'names' dictionary"

    onnx_names = ast.literal_eval(meta["names"])
    assert len(onnx_names) == 31
    assert onnx_names == wrapper.raw_class_names


def test_dental_013_ssot_category_mapping_and_filtering():
    wrapper = RestorationPredictorWrapper(model_path="nonexistent.onnx")
    assert wrapper.category_mapping["Filling"] == "Inlay/Onlay"
    assert wrapper.category_mapping["Crown"] == "Crown/Bridge"
    assert wrapper.category_mapping["Implant"] == "Implant"
    assert wrapper.category_mapping["Root Canal Treatment"] == "Endodontic (RCT)"
    # Non-restorative classes in the 31-class ontology must not be mapped as restorations
    assert wrapper.category_mapping.get("Caries") is None
    assert wrapper.category_mapping.get("Missing teeth") is None
    assert callable(predict.load_model)

