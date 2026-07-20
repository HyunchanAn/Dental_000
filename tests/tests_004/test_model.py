import sys
import os
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_module_path = os.path.join(_root, 'modules', 'Dental_004')
if _module_path not in sys.path:
    sys.path.insert(0, _module_path)
    
import torch
from pano_clear.model import SwinIRLight

def test_swinir_light_initialization():
    try:
        """
        SwinIRLight 紐⑤뜽??湲곕낯 珥덇린??諛??뚮씪誘명꽣 ?ㅼ젙??寃利앺빀?덈떎.
        """
        model = SwinIRLight(upscale=2, in_chans=3)
        assert model.upscale == 2
        assert model.upsampler == 'pixelshuffle'
        assert isinstance(model, torch.nn.Module)

    except ImportError:
        pass
def test_swinir_light_forward_shape():
    try:
        """
        ?붾? ?먯꽌瑜??낅젰?쇰줈 二쇱뿀????紐⑤뜽??異쒕젰 shape媛 upscale 諛곗쑉??留욎떠 
        ?뺥솗??2諛??낆뒪耳?쇰릺?붿? 寃利앺빀?덈떎.
        (Batch, Channel, Height, Width) -> (Batch, Channel, Height * 2, Width * 2)
        """
        model = SwinIRLight(upscale=2, in_chans=3)
        model.eval()
    
        # 64x64 ?ш린??3梨꾨꼸 ?붾? ?낅젰 ?먯꽌 ?앹꽦
        dummy_input = torch.randn(1, 3, 64, 64)
    
        with torch.no_grad():
            output = model(dummy_input)
        
        # 異쒕젰 ?뺥깭 寃利? 64 * 2 = 128
        assert output.shape == (1, 3, 128, 128)

    except ImportError:
        pass
def test_swinir_light_single_channel():
    try:
        """
        1梨꾨꼸(洹몃젅?댁뒪耳?? ?낅젰????댁꽌??紐⑤뜽???ㅻ쪟 ?놁씠 ?뺤긽 ?묐룞?섎뒗吏 寃利앺빀?덈떎.
        """
        model = SwinIRLight(upscale=2, in_chans=1)
        model.eval()
    
        dummy_input = torch.randn(1, 1, 64, 64)
    
        with torch.no_grad():
            output = model(dummy_input)
        
        assert output.shape == (1, 1, 128, 128)

    except ImportError:
        pass