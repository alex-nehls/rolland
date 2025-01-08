import pytest
from traitlets import TraitError
from src.components import Pad

def test_initializes_with_default_values():
    pad = Pad()
    assert pad.sp == 0.0
    assert pad.dp == 0.0
    assert pad.wdthp == 0.0

def test_sets_values_correctly():
    pad = Pad(sp=5.0, dp=3.0, wdthp=2.0)
    assert pad.sp == 5.0
    assert pad.dp == 3.0
    assert pad.wdthp == 2.0

def test_raises_error_for_invalid_type():
    with pytest.raises(TraitError):
        Pad(sp="invalid")

def test_updates_values_correctly():
    pad = Pad()
    pad.sp = 7.0
    pad.dp = 4.0
    pad.wdthp = 1.0
    assert pad.sp == 7.0
    assert pad.dp == 4.0
    assert pad.wdthp == 1.0