.. _start:

Start using Rolland
=======================


This section explains how to set up Rolland and get started with your first simulation.

Installation
------------

1. First step
2. Second step
3. Third step


Define Tracks
--------------


.. code-block:: python
  :linenos:

  from rolland.database.rail.db_rail import UIC60
  from rolland.arrangement import PeriodicArrangement, StochasticArrangement
  from rolland.track import *

  pad1 = DiscrPad(sp=[1, 1])
  slep1 = Sleeper(ms=200)
  pad2 = DiscrPad(sp=[2, 2])
  slep2 = Sleeper(ms=300)

  # Continuous slab track
  tr_slabtrackcont = ContSlabSingleRailTrack(
      rail=UIC60,
      pad = ContPad(sp=[1, 1], dp=[1, 1]),
  )

  # Discrete slab track (no variation)
  tr_slabtrack_simple = SimplePeriodicSlabSingleRailTrack(
      rail=UIC60,
      pad=pad1,
      distance=0.6,
      num_mount=20
  )

  # Discrete slab track (variation)
  tr_slabtrack_arranged = ArrangedSlabSingleRailTrack(
      rail=UIC60,
      pad=PeriodicArrangement(item=[pad1, pad2]),
      distance=StochasticArrangement(item=[0.1, 1.0]),
      num_mount=20
  )

  # Continuous ballasted track
  tr_ball_cont = ContBallastedSingleRailTrack(
      rail=UIC60,
      ballast=Ballast(),
      slab=Slab(),
      pad=ContPad(sp=[1, 1]),
  )

  # Discrete ballasted track (no variation)
  tr_ball_simp = SimplePeriodicBallastedSingleRailTrack(
      rail=UIC60,
      ballast=Ballast(),
      sleeper=slep1,
      pad=pad1,
      distance=0.49,
      num_mount=20
  )

  # Discrete ballasted track (variation)
  tr_ball_arr = ArrangedBallastedSingleRailTrack(
      rail=UIC60,
      ballast=Ballast(),
      pad=PeriodicArrangement(item=[pad1, pad2, pad2, pad1]),
      sleeper=PeriodicArrangement(item=[slep1, slep2, slep2]),
      distance=StochasticArrangement(item=[0.1, 1.0]),
      num_mount=20
  )


