import os
import sys
import numpy as np
import torch
import pytest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DENTAL_014_SRC = os.path.abspath(os.path.join(CURRENT_DIR, "../../../Dental_014/src"))
READER_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../../Dental_Panoramic_Reader"))

for p in (DENTAL_014_SRC, READER_ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

from dental_014.multitask_model import OsteoMAENet
from dental_014.inference import OsteoporosisInferencer
from modules.osteoporosis_predictor import OsteoporosisPredictorWrapper


def test_osteo_mae_net_architecture_forward():
    model = OsteoMAENet(in_channels=3, num_classes=3)
    model.eval()
    dummy_input = torch.randn(1, 3, 256, 512)
    with torch.no_grad():
        pred_pixel_no_mask, cls_logits, _ = model(dummy_input, mask=False)
        pred_pixel_masked, _, mask_tensor = model(dummy_input, mask=True)
    assert cls_logits.shape == (1, 3)
    assert pred_pixel_no_mask is None
    assert pred_pixel_masked is not None
    assert mask_tensor is not None


def test_osteoporosis_inferencer_validation(tmp_path):
    with pytest.raises(FileNotFoundError):
        OsteoporosisInferencer(weight_path=None, device="cpu")
    with pytest.raises(FileNotFoundError):
        OsteoporosisInferencer(weight_path=str(tmp_path / "nonexistent.pt"), device="cpu")
    dummy_onnx = tmp_path / "dummy.onnx"
    dummy_onnx.write_bytes(b"onnx")
    with pytest.raises(ValueError):
        OsteoporosisInferencer(weight_path=str(dummy_onnx), device="cpu")


def test_osteoporosis_predictor_wrapper_contract():
    model_path = os.path.join(READER_ROOT, "modules", "Dental_014", "models", "best.pt")
    wrapper = OsteoporosisPredictorWrapper(weight_path=model_path, device="cpu")
    dummy_pano = np.full((600, 1200, 3), 128, dtype=np.uint8)
    result = wrapper.predict(dummy_pano)
    assert result["module_name"] == "Dental_014_osteoporosis"
    assert result["status"] == "ONLINE_INFERENCE"
    assert result["predicted_class"] in ["Normal", "Osteopenia (경도)", "Osteoporosis (중증)"]
    assert result["category"] in ["LOW", "MODERATE", "HIGH"]
    probs = result["probabilities"]
    assert set(probs.keys()) == {"Normal", "Osteopenia", "Osteoporosis"}
    assert pytest.approx(sum(probs.values()), rel=1e-2) == 1.0


def test_osteoporosis_wrapper_not_available_when_missing():
    wrapper = OsteoporosisPredictorWrapper(weight_path="nonexistent_weight.pt", device="cpu")
    dummy_pano = np.full((600, 1200, 3), 128, dtype=np.uint8)
    result = wrapper.predict(dummy_pano)
    assert result["status"] == "NOT_AVAILABLE"
    assert result["score"] is None
    assert result["category"] is None


