"""Defines track structure."""

from scipy.stats import truncnorm
from traitlets import HasTraits, Instance, Integer, Float, Dict, Tuple, Any

from src.components import Ballast, ContPad, DiscrPad, Rail, Sleeper
from src.track_layout import LayoutConst, LayoutPeriod, LayoutStoch, TrackLayout


class Track(HasTraits):
    """Base class for track structure."""

class SingleRailTrack(Track):
    """Single rail track class."""

    # Rail instance
    rail = Instance(Rail)
class BallastedSingleRailTrack(SingleRailTrack):
    """
    Ballasted single rail track class.
    Example:
    
    >>> tr = BallastedSingleRailTrack(rail = UIC60, ballast = default_ballast)
    >>> tr.padsleepers[0.0] = (thepadA, thesleeperA)
    >>> tr.padsleepers[0.6] = (thepadA, thesleeperB)
    >>> tr.padsleepers[1.1] = (thepadB, thesleeperB)
    >>> tr.padsleepers[1.55] = (thepadC, thesleeperA)

    ...

    """

    # ballast has uniform properties
    ballast = Instance(Ballast)

    # pads and sleepers may have nonuniform properties Dictionary (x-> (Pad, Sleeper))
    padsleepers = Dict(value_trait=Float, key_trait=Tuple(DiscrPad, Sleeper))

class SimplePeriodicBallastedSingleRailTrackFactory(HasTraits):

    # Rail instance
    rail = Instance(Rail)

    # Ballast instance
    ballast = Instance(Ballast)

    # Ballast instance
    sleeper = Instance(Sleeper)

    # Ballast instance
    pad = Instance(DiscrPad)

    # sleeper distance
    distance = Float

    # sleeper count
    count = Integer

    def __call__(self):
        track =  BallastedSingleRailTrack(rail = self.rail, ballast = self.ballast)
        x = 0
        for i in range(self.count):
            track[x] = (self.pad, self.sleeper)
            x += self.distance()
        return track


