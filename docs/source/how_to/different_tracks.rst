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
    from rolland import GaussianImpulse, DiscretizationEBBVerticConst, DeflectionEBBVertic, PMLRailDampVertic
    # Import postprocessing functions
    from rolland.postprocessing import response_fdm, plot

    # Define tracks
    # Continuous slab track
    track1 = ContSlabSingleRailTrack(
        rail=UIC60,
        pad=ContPad(sp=[300*10**6, 0], dp=[30000, 0]),
        l_track = 145.2)
    # Continuous ballasted track
    track2 = ContBallastedSingleRailTrack(
        rail=UIC60,
        pad=ContPad(sp=[300*10**6, 0], dp=[30000, 0]),
        slab=Slab(ms=250),
        ballast=Ballast(sb=[100*10**6, 0], db=[80000, 0]),
        l_track = 145.2)
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

    # Define boundary domains (Perfectly Matched Layer) --> 33.0m on each side
    bound1 = PMLRailDampVertic(l_bound=33.00)
    bound2 = PMLRailDampVertic(l_bound=33.00)
    bound3 = PMLRailDampVertic(l_bound=33.00)
    bound4 = PMLRailDampVertic(l_bound=33.00)

    # Define excitation (Gaussian Impulse) --> Excitation between sleepers at 71.7m
    force1 = GaussianImpulse(x_excit=71.7)
    force2 = GaussianImpulse(x_excit=71.7)
    force3 = GaussianImpulse(x_excit=71.7)
    force4 = GaussianImpulse(x_excit=71.7)

    # Discretize
    discr1 = DiscretizationEBBVerticConst(track = track1, bound=bound1, dt=2e-5, req_simt=0.4)
    discr2 = DiscretizationEBBVerticConst(track = track2, bound=bound2, dt=2e-5, req_simt=0.4)
    discr3 = DiscretizationEBBVerticConst(track = track3, bound=bound3, dt=2e-5, req_simt=0.4)
    discr4 = DiscretizationEBBVerticConst(track = track4, bound=bound4, dt=2e-5, req_simt=0.4)

    # Run simulations and calculate deflection over time
    defl1 = DeflectionEBBVertic(discr=discr1, excit=force1)
    defl2 = DeflectionEBBVertic(discr=discr2, excit=force2)
    defl3 = DeflectionEBBVertic(discr=discr3, excit=force3)
    defl4 = DeflectionEBBVertic(discr=discr4, excit=force4)

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
