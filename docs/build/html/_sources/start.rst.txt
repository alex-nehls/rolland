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

    from rolland.database.rail.db_rail import UIC60
    from rolland.deflection import DeflectionFDMStampka
    from rolland.discretization import DiscretizationFDMStampkaConst
    from rolland.excitation import GaussianImpulse
    from rolland.grid import GridFDMStampka
    from rolland.track import (
        ContBallastedSingleRailTrack,
        ContSlabSingleRailTrack,
        SimplePeriodicBallastedSingleRailTrack,
        SimplePeriodicSlabSingleRailTrack,
        SlabSingleRailTrack)

    from demo.postporcessing_fdm import *

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

    bound1 = PMLStampka(track=track1, grid=grid1)
    bound2 = PMLStampka(track=track2, grid=grid2)
    bound3 = PMLStampka(track=track3, grid=grid3)
    bound4 = PMLStampka(track=track4, grid=grid4)

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

    discr1 = DiscretizationFDMStampkaConst(track=track1, grid=grid1, bound=bound1)
    discr2 = DiscretizationFDMStampkaConst(track=track2, grid=grid2, bound=bound2)
    discr3 = DiscretizationFDMStampkaConst(track=track3, grid=grid3, bound=bound3)
    discr4 = DiscretizationFDMStampkaConst(track=track4, grid=grid4, bound=bound4)

.. code-block:: python
  :caption: Calculate deflection
  :linenos:

    defl1 = DeflectionFDMStampka(track=track1, grid=grid1, excit=force1, discr=discr1, x_excit=grid1.dx * 1337)
    defl2 = DeflectionFDMStampka(track=track2, grid=grid2, excit=force2, discr=discr2, x_excit=grid2.dx * 1337)
    defl3 = DeflectionFDMStampka(track=track3, grid=grid3, excit=force3, discr=discr3, x_excit=grid3.dx * 1337)
    defl4 = DeflectionFDMStampka(track=track4, grid=grid4, excit=force4, discr=discr4, x_excit=grid4.dx * 1337)

.. code-block:: python
  :caption: Postprocessing
  :linenos:

    #   Postprocessing parameters
    f_min = 100                             # Minimum frequency [Hz].
    f_max = 3000                            # Maximum frequency [Hz].

    #   Postprocessing for deflection
    fftfre1, M1 = mobility(defl1, force1.force, grid1, dist=0, f_min=f_min, f_max=f_max)
    fftfre2, M2 = mobility(defl2, force2.force, grid2, dist=0, f_min=f_min, f_max=f_max)
    fftfre3, M3 = mobility(defl3, force3.force, grid3, dist=0, f_min=f_min, f_max=f_max)
    fftfre4, M4 = mobility(defl4, force4.force, grid4, dist=0, f_min=f_min, f_max=f_max)

    # Plot Mobility over Frequency
    plt.figure(figsize=(10, 6))
    plt.loglog(fftfre1, abs(M1), label='Mobility 1')
    plt.loglog(fftfre2, abs(M2), label='Mobility 2')
    plt.loglog(fftfre3, abs(M3), label='Mobility 3')
    plt.loglog(fftfre4, abs(M4), label='Mobility 4')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Mobility')
    plt.title('Mobility vs Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()



