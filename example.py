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

print(tr.factory())

tr1 = SimplePeriodicBallastedSingleRailTrack(
    rail = UIC60,
    ballast = Ballast(),
    pad = DiscrPad(),
    sleeper = Sleeper(),
    distance = 0.49,
    count = 20
    )

print(tr1)