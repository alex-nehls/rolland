"""Tests for analytical methods in rolland package."""

import numpy as np
import pytest
from traitlets import TraitError

from rolland.methods.analytical import (
    ThompsonEBBCont1LSupp,
    ThompsonEBBCont2LSupp,
    ThompsonTSDiscr1LSupp,
    ThompsonTSDiscr2LSupp,
)
from rolland.track import (
    ContBallastedSingleRailTrack,
    ContSlabSingleRailTrack,
    DiscrBallastedSingleRailTrack,
    DiscrSlabSingleRailTrack,
)


@pytest.fixture
def track_instance_cont_slab():
    """Fixture to create an instance of ContSlabSingleRailTrack."""
    return ContSlabSingleRailTrack()

@pytest.fixture
def track_instance_cont_ballasted():
    """Fixture to create an instance of ContBallastedSingleRailTrack."""
    return ContBallastedSingleRailTrack()

@pytest.fixture
def track_instance_discr_slab():
    """Fixture to create an instance of DiscrSlabSingleRailTrack."""
    return DiscrSlabSingleRailTrack()

@pytest.fixture
def track_instance_discr_ballasted():
    """Fixture to create an instance of DiscrBallastedSingleRailTrack."""
    return DiscrBallastedSingleRailTrack()

@pytest.fixture
def analytical_method_instance_cont_slab(track_instance_cont_slab):
    """Fixture to create an instance of ThompsonEBBCont1LSupp with sample data."""
    return ThompsonEBBCont1LSupp(track=track_instance_cont_slab, f=np.array([10, 20]),
                                 F=np.array([100, 200]), x=np.array([1, 2]))

@pytest.fixture
def analytical_method_instance_cont_ballasted(track_instance_cont_ballasted):
    """Fixture to create an instance of ThompsonEBBCont2LSupp with sample data."""
    return ThompsonEBBCont2LSupp(track=track_instance_cont_ballasted, f=np.array([10, 20]),
                                 F=np.array([100, 200]), x=np.array([1, 2]))

@pytest.fixture
def analytical_method_instance_discr_slab(track_instance_discr_slab):
    """Fixture to create an instance of ThompsonTSDiscr1LSupp with sample data."""
    return ThompsonTSDiscr1LSupp(track=track_instance_discr_slab, f=np.array([10, 20]),
                                 F=np.array([100, 200]), x=np.array([1, 2]))

@pytest.fixture
def analytical_method_instance_discr_ballasted(track_instance_discr_ballasted):
    """Fixture to create an instance of ThompsonTSDiscr2LSupp with sample data."""
    return ThompsonTSDiscr2LSupp(track=track_instance_discr_ballasted, f=np.array([10, 20]),
                                 F=np.array([100, 200]), x=np.array([1, 2]))

@pytest.mark.parametrize(("f", "F", "x"), [
    (np.array([10, 20]), np.array([100, 200]), np.array([1, 2])),
    (np.array([0]), np.array([0]), np.array([0])),
    (np.array([1e-10]), np.array([1e-10]), np.array([1e-10])),
])
def class_initialization_cont_slab(f, force, x, track_instance_cont_slab):
    """Test initialization of ThompsonEBBCont1LSupp with different parameters."""
    instance = ThompsonEBBCont1LSupp(track=track_instance_cont_slab, f=f, force=force, x=x)
    assert isinstance(instance, ThompsonEBBCont1LSupp)

@pytest.mark.parametrize(("f", "F", "x"), [
    (np.array([10, 20]), np.array([100, 200]), np.array([1, 2])),
    (np.array([0]), np.array([0]), np.array([0])),
    (np.array([1e-10]), np.array([1e-10]), np.array([1e-10])),
])
def class_initialization_cont_ballasted(f, force, x, track_instance_cont_ballasted):
    """Test initialization of ThompsonEBBCont2LSupp with different parameters."""
    instance = ThompsonEBBCont2LSupp(track=track_instance_cont_ballasted, f=f, force=force, x=x)
    assert isinstance(instance, ThompsonEBBCont2LSupp)

def compute_mobility_cont_slab(analytical_method_instance_cont_slab):
    """Test the compute_mobility method of ThompsonEBBCont1LSupp."""
    mobility, omega_0 = analytical_method_instance_cont_slab.compute_mobility()
    assert mobility is not None
    assert omega_0 is not None

def compute_mobility_cont_ballasted(analytical_method_instance_cont_ballasted):
    """Test the compute_mobility method of ThompsonEBBCont2LSupp."""
    mobility, omega_0, omega_1, omega_2 = analytical_method_instance_cont_ballasted.compute_mobility()
    assert mobility is not None
    assert omega_0 is not None
    assert omega_1 is not None
    assert omega_2 is not None

def invalid_initialization_cont_slab(track_instance_cont_slab):
    """Test initialization of ThompsonEBBCont1LSupp with invalid parameters."""
    with pytest.raises(TraitError):
        ThompsonEBBCont1LSupp(track=track_instance_cont_slab, f="invalid", F="invalid", x="invalid")

def invalid_initialization_cont_ballasted(track_instance_cont_ballasted):
    """Test initialization of ThompsonEBBCont2LSupp with invalid parameters."""
    with pytest.raises(TraitError):
        ThompsonEBBCont2LSupp(track=track_instance_cont_ballasted, f="invalid", F="invalid", x="invalid")
