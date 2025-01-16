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

    def __repr__(self):
        st = ""
        for x in sorted(self.padsleepers.keys()):
            p, s = self.padsleepers[x]
            st += f'{x}, {p.sp}, {s.ms} \n'
        return st
# option 1
class SimplePeriodicBallastedSingleRailTrackFactory(HasTraits):
    """each call to the factory produces a new track"""

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

    def factory(self):
        track =  BallastedSingleRailTrack(rail = self.rail, ballast = self.ballast)
        x = 0
        for i in range(self.count):
            track.padsleepers[x] = (self.pad, self.sleeper)
            x += self.distance
        return track

# option 2
class SimplePeriodicBallastedSingleRailTrack(BallastedSingleRailTrack):
    """this comes with a built-in factory"""

    # Sleeper instance
    sleeper = Instance(Sleeper)

    # Pad instance
    pad = Instance(DiscrPad)

    # sleeper distance
    distance = Float

    # sleeper count
    count = Integer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # factory
        x = 0
        for i in range(self.count):
            self.padsleepers[x] = (self.pad, self.sleeper)
            x += self.distance

# some classes to define the arrangement along the track
# this assumes that all attributes are floats (which is not the case)
class Arrangement(HasTraits):
    
    # characteristic object or objects to repeat
    item = Any

    def generate(self, count):
        """generate count repetitions of objects"""
        pass

class PeriodicArrangment(Arrangement):

    def generate(self, count):
        c = 0
        while c<count: 
            if isinstance(self.item, list):
                for item_ in self.item:
                    yield item_
                    c += 1
            else: 
                yield self.item
                c += 1

class ArrangedBallastedSingleRailTrack(BallastedSingleRailTrack):

    # Sleeper instance
    sleeper = Instance(Arrangement)

    # Pad instance
    pad = Instance(Arrangement)

    # sleeper distance
    distance = Instance(Arrangement)

    # sleeper count
    count = Integer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # factory
        x = 0
        for s, p, d in zip(self.sleeper.generate(self.count), 
                           self.pad.generate(self.count), 
                           self.distance.generate(self.count)):
            self.padsleepers[x] = (p, s)
            print(s,p,d)
            x += d

