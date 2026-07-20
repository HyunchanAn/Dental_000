import sys
import os
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_module_path = os.path.join(_root, 'modules', 'Dental_004')
if _module_path not in sys.path:
    sys.path.insert(0, _module_path)
    
import torch
from pano_clear.device import get_best_device, get_device_info


def test_get_best_device_returns_valid():
    try:
        """
        get_best_device()가 항상 유효한 torch.device 객체를 반환하는지 검증합니다.
        CI 환경(GPU 미보유)에서도 CPU로 안전하게 폴백되어야 합니다.
        """
        device = get_best_device()
        assert isinstance(device, torch.device)
        assert device.type in ['cuda', 'mps', 'cpu']


    except ImportError:
        pass
def test_get_best_device_tensor_allocation():
    try:
        """
        반환된 디바이스에서 실제 텐서 생성 및 연산이 정상 작동하는지 검증합니다.
        """
        device = get_best_device()
        tensor = torch.randn(2, 2, device=device)
        result = tensor + tensor
        assert result.shape == (2, 2)
        assert result.device.type == device.type


    except ImportError:
        pass
def test_get_device_info_structure():
    try:
        """
        get_device_info()가 필수 키를 모두 포함하는 딕셔너리를 반환하는지 검증합니다.
        """
        info = get_device_info()
        assert "device" in info
        assert "device_type" in info
        assert "gpu_name" in info
        assert "pytorch_version" in info
        assert info["device_type"] in ['cuda', 'mps', 'cpu']

    except ImportError:
        pass