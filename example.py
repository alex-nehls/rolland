from database.db_rail import UIC60
from src.arrangement import PeriodicArrangment, StochasticArrangement
from src.track import *

pad1 = DiscrPad(sp=[1, 1])
slep1 = Sleeper(ms=200)
pad2 = DiscrPad(sp=[2, 2])
slep2 = Sleeper(ms=300)


tr_slabtrackcont = SlabSingleRailTrack(
    rail=UIC60,
    pad = ContPad(sp=[1, 1])
)


tr_slabtrack_simple = SimplePeriodicSlabSingleRailTrack(
    rail=UIC60,
    pad=pad1,
    distance=0.6,
    num_mount=20
)


tr_slabtrack_arranged = ArrangedSlabSingleRailTrack(
    rail=UIC60,
    pad=PeriodicArrangment(item=[pad1, pad2]),
    distance=StochasticArrangement(item=[0.1, 1.0]),
    num_mount=20
)



tr_ball_cont = ContBallastedSingleRailTrack(
    rail=UIC60,
    ballast=Ballast(),
    slab=Slab(),
    pad=ContPad(sp=[1, 1]),
)

tr_ball_simp = SimplePeriodicBallastedSingleRailTrack(
    rail=UIC60,
    ballast=Ballast(),
    sleeper=slep1,
    pad=pad1,
    distance=0.49,
    num_mount=20
)

tr_ball_arr = ArrangedBallastedSingleRailTrack(
    rail=UIC60,
    ballast=Ballast(),
    pad=PeriodicArrangment(item=[pad1, pad2, pad2, pad1]),
    sleeper=PeriodicArrangment(item=[slep1, slep2, slep2]),
    distance=StochasticArrangement(item=[0.1, 1.0]),
    num_mount=20
)



a=10
