from src.track import *
from database.db_rail import UIC60

tr = SimplePeriodicBallastedSingleRailTrackFactory(
    rail = UIC60,
    ballast = Ballast(),
    pad = DiscrPad(),
    sleeper = Sleeper(),
    distance = 0.49,
    count = 20
    )

tr0 = tr.factory()
print(tr0)

tr1 = SimplePeriodicBallastedSingleRailTrack(
    rail = UIC60,
    ballast = Ballast(),
    pad = DiscrPad(),
    sleeper = Sleeper(),
    distance = 0.49,
    count = 20
    )

print(tr1)

pad1 = DiscrPad(sp=[1,1])
slep1 = Sleeper(ms=200)
pad2 = DiscrPad(sp=[2,2])
slep2 = Sleeper(ms=300)

tr2 = ArrangedBallastedSingleRailTrack(
    rail = UIC60,
    ballast = Ballast(),
    pad = PeriodicArrangment(item = [pad1,pad2]),
    sleeper = PeriodicArrangment(item = [slep1,slep2,slep2]),
    distance = PeriodicArrangment(item = 0.49),
    count = 20
    )

print(tr2)
