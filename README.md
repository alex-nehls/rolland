<picture>
  <source srcset="docs/source/images/logo_rolland_light.svg" media="(prefers-color-scheme: dark)">
  <img src="docs/source/images/logo_rolland_dark.svg" alt="Logo" width="100">
</picture>


[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/mantelmax/rolland)
[![Documentation Status](https://readthedocs.org/projects/rolland-rolling-noise-and-dynamics/badge/?version=latest)](https://rolland-rolling-noise-and-dynamics.readthedocs.io/en/latest/?badge=latest)
[![Python Version](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)


# Rolland
Rolling Noise and Dynamics (Rolland) is an advanced simulation and calculation model designed to analyze, predict, 
and optimize the acoustic properties of railway tracks, with a focus on realistic, efficient, and fast computations. 

# Features
**Current Features:**
- Applies Finite Difference Method in time domain
- Allows the definition of arbitrary track structures
  - Enables periodic or stochastic variations of the track properties (e.g. stochastically varying sleeper distances)
  - Enables the representation of track property deviations that occur in practise
- Includes several analytical models for comparison and validation

**Planned Features:**
- Full rail dynamics
- Consideration of rail radiation
- Consideration of non-linear effects
- Excitation by multiple moving wheels

<picture>
  <source srcset="docs/source/images/mwi_github_dark.png" media="(prefers-color-scheme: dark)">
  <img src="docs/source/images/mwi_light.png">
</picture>

# Documentation
Documentation is available [here](https://rolland-rolling-noise-and-dynamics.readthedocs.io) with a 
how to section and examples.

# Example
This example calculates the track response of a double layer track with discrete mounting positions.
The track is excited between two sleepers with a Gaussian impulse.

```python
# Import components
from rolland import DiscrPad, Sleeper, Ballast
# Import rail
from rolland.database.rail.db_rail import UIC60
# Import double layer track with descrete mounting positions
from rolland import SimplePeriodicBallastedSingleRailTrack
# Import classes required for numerical simulation
from rolland import PMLRailDampVertic, GaussianImpulse, DiscretizationEBBVerticConst, DeflectionEBBVertic
# import postprocessing functions
from rolland.postprocessing import response_fdm, plot

# Define track
track = SimplePeriodicBallastedSingleRailTrack(
    rail=UIC60,
    pad=DiscrPad(sp=[180 * 10 ** 6, 0], dp=[18000, 0]),
    sleeper=Sleeper(ms=150),
    ballast=Ballast(sb=[105 * 10 ** 6, 0], db=[48000, 0]),
    num_mount=243,
    distance=0.6)

# Define boundary domain (Perfectly Matched Layer) --> 33.0m on each side
bound = PMLRailDampVertic(l_bound=33.0)

# Define excitation (Gaussian Impulse) --> Excitation between sleepers at 71.7m
excit = GaussianImpulse(x_excit=71.7)

# Discretize
discr = DiscretizationEBBVerticConst(track = track, bound=bound, dt=2e-5, req_simt=0.4)

# Run simulation and calculate deflection over time
defl = DeflectionEBBVertic(discr=discr, excit=excit)

# Postprocessing: Calculate frequency response at x = x_excit (receptance, mobility, accelerance)
fftfre, rez, mob, accel = response_fdm(defl)

# Plot the results
plot([(fftfre, mob)],
     ['SimplePeriodicBallastedSingleRailTrack'],
     'Frequency Response', 'f [Hz]', 'Mobility [m/Ns]')
```

![Example](docs/source/images/example_readme.png)