import pytest
from src.components import Rail

def test_rail_initialization():
    """Test the initialization of the Rail class."""
    rail = Rail()
    assert rail.rl_prof == "UIC60"
    assert rail.rl_num == 1
    assert rail.bm_type == "TS"
    assert rail.E == 210e9
    assert rail.G == 81e9
    assert rail.nu == 0.3
    assert rail.kap == 0.0
    assert rail.mr == 60.2
    assert rail.dr == 0.0
    assert rail.gammar == 0.0
    assert rail.Iyr == 3038.30e-8
    assert rail.Izr == 512.30e-8
    assert rail.Itr == 209.20e-8
    assert rail.Ar == 76.70e-4
    assert rail.Asr == 0.688
    assert rail.Vr == 7670.00e-6

def test_rail_set_profile():
    """Test setting the rail profile."""
    rail = Rail(rl_prof="UIC54")
    assert rail.rl_prof == "UIC54"
    assert rail.E == 0.0
    assert rail.G == 0.0
    assert rail.nu == 0.0
    assert rail.kap == 0.0
    assert rail.mr == 54.0
    assert rail.dr == 0.0
    assert rail.gammar == 0.0
    assert rail.Iyr == 0.0
    assert rail.Izr == 0.0
    assert rail.Itr == 0.0
    assert rail.Ar == 0.0
    assert rail.Asr == 0.0
    assert rail.Vr == 0.0