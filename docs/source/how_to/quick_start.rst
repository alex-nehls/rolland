.. _quick_start:

First Simulation
================

This example demonstrates how to set up and run a basic simulation using the Rolland library to calculate the
frequency response of a simple railway track.


.. code-block:: python
  :caption: Python Code
  :linenos:

    # Import components
    from rolland import DiscrPad, Sleeper, Ballast
    # Import rail
    from rolland.database.rail.db_rail import UIC60
    # Import double layer track with descrete mounting positions
    from rolland import SimplePeriodicBallastedSingleRailTrack
    # Import classes required for numerical simulation
    from rolland import GridFDMStampka, PMLStampka, GaussianImpulse, DiscretizationFDMStampkaConst, DeflectionFDMStampka
    # Import postprocessing functions
    from rolland.postprocessing import response_fdm, plot

    # Define track
    track = SimplePeriodicBallastedSingleRailTrack(
          rail=UIC60,
          pad=DiscrPad(sp=[180*10**6, 0], dp=[18000, 0]),
          sleeper=Sleeper(ms=150),
          ballast=Ballast(sb=[105*10**6, 0], db=[48000, 0]),
          num_mount=243,
          distance=0.6)

    # Define grid
    grid = GridFDMStampka(track = track, dt=2e-5, req_simt=0.4, bx=1, n_bound=600)

    # Define boundary domain (Perfectly Matched Layer)
    bound = PMLStampka(grid=grid)

    # Define excitation (Gaussian Impulse)
    excit = GaussianImpulse(grid=grid)

    # Discretize
    discr = DiscretizationFDMStampkaConst(bound=bound)

    # Run simulation and calculate deflection over time (excitation at 71.7m between two sleepers)
    defl = DeflectionFDMStampka(discr=discr, excit=excit, x_excit=71.7)

    # Postprocessing: Calculate frequency response at x = x_excit (receptance, mobility, accelerance)
    fftfre, rez, mob, accel = response_fdm(defl)

    # Plot the results
    plot([(fftfre, mob)],
       ['SimplePeriodicBallastedSingleRailTrack'],
        'Frequency Response', 'f [Hz]', 'Mobility [m/Ns]')



.. image:: ../images/example_readme.png
   :width: 700px
   :align: center
