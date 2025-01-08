import pytest
from traitlets import TraitError

from src.components import Rail


def test_rail_initialization():
    """Test the initialization of the Rail class."""
    rail = Rail()
    assert rail.rl_prof == "UIC60"
    assert rail.rl_geo == [(0.0, 0.0)]
    assert rail.rl_num == 1
    assert rail.Br == 5000.0
    assert rail.dr == 0.5
    assert rail.mr == 60.0

def test_rail_invalid_number():
    """Test the initialization of the Rail class with invalid rail number."""
    with pytest.raises(TraitError):
        Rail(rl_num=3)

def test_rail_set_values():
    """Test the setting of values in the Rail class."""
rail = Rail(rl_prof="UIC54", rl_geo=[(0.0, 0.0)], rl_num=2, Br=4500.0, dr=0.45, mr=54.0)
assert rail.rl_prof == "UIC54"
assert rail.rl_geo == [(0.0, 0.0)]
assert rail.rl_num == 2
assert rail.Br == 4500.0
assert rail.dr == 0.45
assert rail.mr == 54.0
