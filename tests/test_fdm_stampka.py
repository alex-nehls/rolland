"""Tests for FDM Stampka methods."""

import csv

import numpy as np
import pytest

from rolland import (
    Ballast,
    ContBallastedSingleRailTrack,
    ContPad,
    ContSlabSingleRailTrack,
    DeflectionFDMStampka,
    DiscretizationFDMStampkaConst,
    DiscrPad,
    GaussianImpulse,
    GridFDMStampka,
    PMLStampka,
    SimplePeriodicBallastedSingleRailTrack,
    SimplePeriodicSlabSingleRailTrack,
    Slab,
    Sleeper,
)
from rolland.database.rail.db_rail import UIC60
from rolland.postprocessing import response_fdm

RELATIVE_TOLERANCE = 1e-5

# Mapping between CSV keys and test keys
CSV_KEY_MAPPING = {
    'ContSlabSingleRailTrack': 'mob_cont_slab',
    'ContBallastedSingleRailTrack': 'mob_cont_ball',
    'SimplePeriodicSlabSingleRailTrack': 'mob_discr_slab',
    'SimplePeriodicBallastedSingleRailTrack': 'mob_discr_ball',
}


@pytest.fixture(scope="module")
def tracks():
    """Create track instances for testing."""
    return {
        'track_cont_slab': ContSlabSingleRailTrack(
            rail=UIC60,
            pad=ContPad(sp=[300 * 10**6, 0], dp=[30000, 0]),
        ),
        'track_cont_ball': ContBallastedSingleRailTrack(
            rail=UIC60,
            pad=ContPad(sp=[300 * 10**6, 0], dp=[30000, 0]),
            slab=Slab(ms=250),
            ballast=Ballast(sb=[100 * 10**6, 0], db=[80000, 0]),
        ),
        'track_discr_slab': SimplePeriodicSlabSingleRailTrack(
            rail=UIC60,
            pad=DiscrPad(sp=[180 * 10**6, 0], dp=[30000, 0]),
            num_mount=243,
            distance=0.6,
        ),
        'track_discr_ball': SimplePeriodicBallastedSingleRailTrack(
            rail=UIC60,
            pad=DiscrPad(sp=[180 * 10**6, 0], dp=[18000, 0]),
            sleeper=Sleeper(ms=150),
            ballast=Ballast(sb=[105 * 10**6, 0], db=[48000, 0]),
            num_mount=243,
            distance=0.6,
        ),
    }


@pytest.fixture(scope="module")
def deflections(tracks):
    """Create deflection instances for testing."""
    grids = {
        'grid_cont_slab': GridFDMStampka(
            track=tracks['track_cont_slab'],
            dt=2e-5,
            req_l=80,
            req_simt=0.4,
            bx=1,
            n_bound=600,
        ),
        'grid_cont_ball': GridFDMStampka(
            track=tracks['track_cont_ball'],
            dt=2e-5,
            req_l=80,
            req_simt=0.4,
            bx=1,
            n_bound=600,
        ),
        'grid_discr_slab': GridFDMStampka(
            track=tracks['track_discr_slab'],
            dt=2e-5,
            req_l=80,
            req_simt=0.4,
            bx=1,
            n_bound=600,
        ),
        'grid_discr_ball': GridFDMStampka(
            track=tracks['track_discr_ball'],
            dt=2e-5,
            req_l=80,
            req_simt=0.4,
            bx=1,
            n_bound=600,
        ),
    }

    bounds = {key: PMLStampka(grid=grid) for key, grid in grids.items()}
    forces = {key: GaussianImpulse(grid=grid) for key, grid in grids.items()}
    discretizations = {
        key: DiscretizationFDMStampkaConst(bound=bounds[key])
        for key in bounds
    }

    return {
        'mob_cont_slab': DeflectionFDMStampka(
            discr=discretizations['grid_cont_slab'],
            excit=forces['grid_cont_slab'],
            x_excit=71.7,
        ),
        'mob_cont_ball': DeflectionFDMStampka(
            discr=discretizations['grid_cont_ball'],
            excit=forces['grid_cont_ball'],
            x_excit=71.7,
        ),
        'mob_discr_slab': DeflectionFDMStampka(
            discr=discretizations['grid_discr_slab'],
            excit=forces['grid_discr_slab'],
            x_excit=71.7,
        ),
        'mob_discr_ball': DeflectionFDMStampka(
            discr=discretizations['grid_discr_ball'],
            excit=forces['grid_discr_ball'],
            x_excit=71.7,
        ),
    }


@pytest.fixture(scope="module")
def mobility_results(deflections):
    """Compute mobility results for testing."""
    results = {}
    for key, deflection in deflections.items():
        # Compute mobility directly using response_fdm
        fftfre, _, mob, _ = response_fdm(deflection)
        results[key] = (fftfre, mob)
    return results


@pytest.fixture(scope="module")
def csv_data():
    """Load precomputed mobility data from CSV."""
    data = {}
    with open('tests/data/data_fdm_stampka.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            freq = float(row['Frequency'])
            # Map CSV keys to test keys
            mapped_row = {
                CSV_KEY_MAPPING[key]: float(value)
                for key, value in row.items()
                if key != 'Frequency'
            }
            data[freq] = mapped_row
    return data


@pytest.mark.parametrize("mobility_name", [
    'mob_cont_slab',
    'mob_cont_ball',
    'mob_discr_slab',
    'mob_discr_ball',
])
def test_fdm_stampka_methods(mobility_name, mobility_results, csv_data):
    """Test FDM Stampka methods against precomputed mobility data."""
    fftfre, mob = mobility_results[mobility_name]

    for i, freq in enumerate(fftfre):
        expected_value = csv_data[freq][mobility_name]
        actual_value = abs(mob[i])
        assert np.isclose(
            actual_value,
            expected_value,
            rtol=RELATIVE_TOLERANCE,
        ), (
            f"Mismatch in {mobility_name} at frequency {freq}: "
            f"expected {expected_value}, got {actual_value}"
        )
