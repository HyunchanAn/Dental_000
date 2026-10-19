import os
import sys
import torch
import pytest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DENTAL_011_SRC = os.path.abspath(os.path.join(CURRENT_DIR, "../../../Dental_011/src"))
if DENTAL_011_SRC not in sys.path:
    sys.path.insert(0, DENTAL_011_SRC)

from model import AgeRegressionModel


def test_age_regression_model_forward_shape():
    model = AgeRegressionModel(pretrained=False)
    model.eval()
    dummy_input = torch.randn(2, 3, 224, 224)
    with torch.no_grad():
        output = model(dummy_input)
    assert output.shape == (2,), f"Expected shape (2,), got {output.shape}"
    assert torch.isfinite(output).all(), "Model output contains non-finite values"


def test_age_regression_model_backward_pass():
    model = AgeRegressionModel(pretrained=False)
    model.train()
    dummy_input = torch.randn(2, 3, 224, 224)
    target_age = torch.tensor([12.5, 45.0], dtype=torch.float32)
    pred = model(dummy_input)
    loss = torch.nn.functional.mse_loss(pred, target_age)
    loss.backward()
    assert model.backbone.fc[1].weight.grad is not None

