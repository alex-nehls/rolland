.. _different_tracks:

Compare Different Tracks
=========================
This example demonstrates how to set up and run a basic simulation using the Rolland library to calculate the
frequency response of different railway tracks. The example includes continuous and discrete tracks with different
with a single or double layer. See :cite:`thompson2024j` for more information.


.. code-block:: python
  :caption: Python Code
  :linenos:

    # Import components
    from rolland import DiscrPad, Sleeper, Ballast, ContPad, Slab
    # Import rail
    from rolland.database.rail.db_rail import UIC60
    # Import different tracks
    from rolland import (
        ContSlabSingleRailTrack,
        ContBallastedSingleRailTrack,
        SimplePeriodicSlabSingleRailTrack,
        SimplePeriodicBallastedSingleRailTrack)
    # Import classes required for numerical simulation
    from rolland import GridFDMStampka, PMLStampka, GaussianImpulse, DiscretizationFDMStampkaConst, DeflectionFDMStampka
    # Import postprocessing functions
    from rolland.postprocessing import response_fdm, plot

    # Define tracks
    # Continuous slab track
    track1 = ContSlabSingleRailTrack(
        rail=UIC60,
        pad=ContPad(sp=[300*10**6, 0], dp=[30000, 0])),
        l_track = 145.2
    # Continuous ballasted track
    track2 = ContBallastedSingleRailTrack(
        rail=UIC60,
        pad=ContPad(sp=[300*10**6, 0], dp=[30000, 0]),
        slab=Slab(ms=250),
        ballast=Ballast(sb=[100*10**6, 0], db=[80000, 0])),
        l_track = 145.2
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

    # Define grids
    grid1 = GridFDMStampka(track = track1, dt=2e-5, req_simt=0.4, bx=1, n_bound=600)
    grid2 = GridFDMStampka(track = track2, dt=2e-5, req_simt=0.4, bx=1, n_bound=600)
    grid3 = GridFDMStampka(track = track3, dt=2e-5, req_simt=0.4, bx=1, n_bound=600)
    grid4 = GridFDMStampka(track = track4, dt=2e-5, req_simt=0.4, bx=1, n_bound=600)

    # Define boundary domains (Perfectly Matched Layer)
    bound1 = PMLStampka(grid=grid1)
    bound2 = PMLStampka(grid=grid2)
    bound3 = PMLStampka(grid=grid3)
    bound4 = PMLStampka(grid=grid4)

    # Define excitation (Gaussian Impulse)
    force1 = GaussianImpulse(grid=grid1)
    force2 = GaussianImpulse(grid=grid2)
    force3 = GaussianImpulse(grid=grid3)
    force4 = GaussianImpulse(grid=grid4)

    # Discretize
    discr1 = DiscretizationFDMStampkaConst(bound=bound1)
    discr2 = DiscretizationFDMStampkaConst(bound=bound2)
    discr3 = DiscretizationFDMStampkaConst(bound=bound3)
    discr4 = DiscretizationFDMStampkaConst(bound=bound4)

    # Run simulations and calculate deflection over time (excitation at 71.7m)
    defl1 = DeflectionFDMStampka(discr=discr1, excit=force1, x_excit=71.7)
    defl2 = DeflectionFDMStampka(discr=discr2, excit=force2, x_excit=71.7)
    defl3 = DeflectionFDMStampka(discr=discr3, excit=force3, x_excit=71.7)
    defl4 = DeflectionFDMStampka(discr=discr4, excit=force4, x_excit=71.7)

    # Postprocessing: Calculate frequency response at x = x_excit (receptance, mobility, accelerance)
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
          'Frequency Resonse', 'f [Hz]', 'Mobility [m/Ns]')



.. image:: ../images/example_different_tracks.png
   :width: 700px
   :align: center
