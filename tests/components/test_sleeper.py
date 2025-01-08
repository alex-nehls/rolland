from src.components import Sleeper


def test_sleeper_initialization():
    """Test the initialization of the Sleeper class."""
    sleeper = Sleeper()
    assert sleeper.sl_typ == "B70"
    assert sleeper.ms == 300.0
    assert sleeper.ls == 2.5
    assert sleeper.Bs == 10000.0

def test_sleeper_set_values():
    """Test the setting of values in the Sleeper class."""
    sleeper = Sleeper(sl_typ="B80")
    assert sleeper.sl_typ == "B80"
    assert sleeper.ms == 320.0
    assert sleeper.ls == 2.6
    assert sleeper.Bs == 11000.0

def test_sleeper_invalid_type():
    """Test the initialization of the Sleeper class with an invalid type."""
    sleeper = Sleeper(sl_typ="InvalidType")
    assert sleeper.sl_typ == "InvalidType"
    assert sleeper.ms == 0.0
    assert sleeper.ls == 0.0
    assert sleeper.Bs == 0.0
