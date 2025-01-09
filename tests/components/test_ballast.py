from src.components import Ballast


def test_ballast_initialization():
    """Test the initialization of the Ballast class."""
    ballast = Ballast()
    assert ballast.sb == 0.0
    assert ballast.db == 0.0
