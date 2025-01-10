from src.components import Sleeper


def test_sleeper_slab_initialization():
    """Test the initialization of the Sleeper class with slab foundation."""
    sleeper = Sleeper(fnd_type="slab")
    assert sleeper.sl_type == "discr"
    assert sleeper.fnd_type == "slab"
    assert sleeper.ms == 1e20
    assert sleeper.Bs == 1e20
