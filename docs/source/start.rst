.. _start:

Start using Rolland
=======================


This section explains how to set up Rolland and get started with your first simulation.

Installation
------------

To install Rolland, follow these steps:

1. **Clone the repository**: Clone the Rolland repository from GitHub to your local machine.
2. **Create a virtual environment**: Set up a virtual environment to manage dependencies.
3. **Install dependencies**: Install the required dependencies using `pip`.


Use Rolland
--------------

.. code-block:: python
  :caption: Define several tracks
  :linenos:

    # Import components
    from rolland import DiscrPad, Sleeper, Ballast, ContPad, Slab

    # Import rail
    from rolland.database.rail.db_rail import UIC60

    # Import tracks
    from rolland import (
        ContSlabSingleRailTrack,
        ContBallastedSingleRailTrack,
        SimplePeriodicSlabSingleRailTrack,
        SimplePeriodicBallastedSingleRailTrack
    )

    # Import necessary classes for calculation
    from rolland import (
        DeflectionFDMStampka,
        DiscretizationFDMStampkaConst,
        GaussianImpulse,
        GridFDMStampka,
        PMLStampka
    )

    # Import functions for postprocessing
    from demo.postporcessing_fdm import *

.. code-block:: python
  :caption: Define different tracks
  :linenos:

    # Continuous slab track
    track1 = ContSlabSingleRailTrack(
        rail=UIC60,
        pad=ContPad(sp=[300*10**6, 0], dp=[30000, 0]))

    # Continuous ballasted track
    track2 = ContBallastedSingleRailTrack(
        rail=UIC60,
        pad=ContPad(sp=[300*10**6, 0], dp=[30000, 0]),
        slab=Slab(ms=250),
        ballast=Ballast(sb=[100*10**6, 0], db=[80000, 0]))

    # Discrete slab track
    track3 = SimplePeriodicSlabSingleRailTrack(
        rail=UIC60,
        pad=DiscrPad(sp=[180*10**6, 0], dp=[30000, 0]),
        num_mount=243,
        distance=0.6)

    # Discrete ballasted track
    track4 = SimplePeriodicBallastedSingleRailTrack(
        rail=UIC60,
        pad=DiscrPad(sp=[180*10**6, 0], dp=[18000, 0]),
        sleeper=Sleeper(ms=150),
        ballast=Ballast(sb=[105*10**6, 0], db=[48000, 0]),
        num_mount=243,
        distance=0.6)

.. code-block:: python
  :caption: Define grid for each track
  :linenos:

    grid1 = GridFDMStampka(track = track1, dt=2e-5, req_l=80, req_simt=0.4, bx=1, n_bound=600)
    grid2 = GridFDMStampka(track = track2, dt=2e-5, req_l=80, req_simt=0.4, bx=1, n_bound=600)
    grid3 = GridFDMStampka(track = track3, dt=2e-5, req_l=80, req_simt=0.4, bx=1, n_bound=600)
    grid4 = GridFDMStampka(track = track4, dt=2e-5, req_l=80, req_simt=0.4, bx=1, n_bound=600)

.. code-block:: python
  :caption: Define boundary conditions
  :linenos:

    bound1 = PMLStampka(grid=grid1)
    bound2 = PMLStampka(grid=grid2)
    bound3 = PMLStampka(grid=grid3)
    bound4 = PMLStampka(grid=grid4)

.. code-block:: python
  :caption: Define excitation
  :linenos:

    force1 = GaussianImpulse(grid=grid1)
    force2 = GaussianImpulse(grid=grid2)
    force3 = GaussianImpulse(grid=grid3)
    force4 = GaussianImpulse(grid=grid4)

.. code-block:: python
  :caption: Descretization
  :linenos:

    discr1 = DiscretizationFDMStampkaConst(bound=bound1)
    discr2 = DiscretizationFDMStampkaConst(bound=bound2)
    discr3 = DiscretizationFDMStampkaConst(bound=bound3)
    discr4 = DiscretizationFDMStampkaConst(bound=bound4)

.. code-block:: python
  :caption: Calculate deflection
  :linenos:

    defl1 = DeflectionFDMStampka(discr=discr1, excit=force1, x_excit=71.7)
    defl2 = DeflectionFDMStampka(discr=discr2, excit=force2, x_excit=71.7)
    defl3 = DeflectionFDMStampka(discr=discr3, excit=force3, x_excit=71.7)
    defl4 = DeflectionFDMStampka(discr=discr4, excit=force4, x_excit=71.7)

.. code-block:: python
  :caption: Postprocessing
  :linenos:

    # Calculate the frequency response (receptance, mobility, accelerance)
    fftfre1, rez1, mob1, accel1 = response_fdm(defl1)
    fftfre2, rez2, mob2, accel2 = response_fdm(defl2)
    fftfre3, rez3, mob3, accel3 = response_fdm(defl3)
    fftfre4, rez4, mob4, accel4 = response_fdm(defl4)

    # Plot the results
    plot([(fftfre1, mob1), (fftfre2, mob2), (fftfre3, mob3), (fftfre4, mob4)],
         ['ContSlabSingleRailTrack',
          'ContBallastedSingleRailTrack',
          'SimplePeriodicSlabSingleRailTrack',
          'SimplePeriodicBallastedSingleRailTrack'],
          'Frequency Response', 'f [Hz]', 'Mobility [m/Ns]')


