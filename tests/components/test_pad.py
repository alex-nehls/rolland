import pytest
from traitlets import TraitError

from src.components import Pad


def test_pad_initialization():
    """Test the initialization of the Pad class."""
    pad = Pad()
    assert pad.sp == [0.0, 0.0]
    assert pad.dp == 0.0
    assert pad.wdthp == 0.0

def test_pad_invalid_stiffness():
    """Test the initialization of the Pad class with invalid stiffness."""
    with pytest.raises(TraitError):
        Pad(sp=[0.0, 0.0, 0.0])

def test_pad_set_values():
    """Test the setting of values in the Pad class."""
    pad = Pad(sp=[1000.0, 2000.0], dp=5.0, wdthp=0.5)
    assert pad.sp == [1000.0, 2000.0]
    assert pad.dp == 5.0
    assert pad.wdthp == 0.5
