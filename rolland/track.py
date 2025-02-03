"""Defines track structures.

Contains classes for the following superstructure types:
    - Single rail track
        - Slab track
            - Continuous slab track
            - Discrete slab track
                - Simple periodic slab track (uniform properties)
                - Arranged slab track (nonuniform properties)

        - Ballasted single rail track
            - Continuous ballasted single rail track
            - Discrete ballasted single rail track
                - Simple periodic ballasted single rail track (uniform properties)
                - Arranged ballasted single rail track (nonuniform properties)
"""

from traitlets import Dict, Float, HasTraits, Instance, Integer, Tuple

from rolland.arrangement import Arrangement
from rolland.components import Ballast, ContPad, DiscrPad, Rail, Slab, Sleeper


class Track(HasTraits):
    """Base class for track structure."""


class SingleRailTrack(Track):
    """Single rail track class."""

    # Rail instance
    rail = Instance(Rail)


class SlabSingleRailTrack(SingleRailTrack):
    """Single rail slab track class.

    Slab is defined as rigid foundation.
    """

    # Slab instance
    slab = Slab()

    def __init__(self, *args, **kwargs):
        # Set the mass of the slab to a very large number to avoid discplacement
        super().__init__(*args, **kwargs)
        self.slab.ms = 1e20


class ContSlabSingleRailTrack(SlabSingleRailTrack):
    """Single rail continuous slab track class.

    All superstructure properties are uniform along the track.

    Example:
    --------
    >>> tr = ContSlabSingleRailTrack(rail = UIC60)
    >>> tr.pad = thepad
    >>> tr.slab = theslab
    ...
    """

    # Pad instance
    pad = Instance(ContPad)


class DiscrSlabSingleRailTrack(SlabSingleRailTrack):
    """Single rail discrete slab track class.

    Rail is mounted discretely. Mounting properties may vary.
    """

    # Pad instance
    pad = Instance(DiscrPad)

    # Dictionary for discrete mounting positions (x-> (Pad)).
    # May have nonuniform properties.
    mount_prop = Dict(value_trait=Float(), key_trait=Tuple(DiscrPad, None))

    def __repr__(self):
        """Represent mounting properties as string."""
        st = ""
        for x in sorted(self.mount_prop.keys()):
            p, s = self.mount_prop[x]
            st += f'{x}, {p.sp}, {s.ms} \n'
        return st


class SimplePeriodicSlabSingleRailTrack(DiscrSlabSingleRailTrack):
    """Single rail simple periodic slab track class.

    Rail is mounted discretely. Mounting properties are uniform.

    Example:
    --------
    >>> tr = SimplePeriodicSlabSingleRailTrack(rail = UIC60)
    >>> tr.mount_prop[0.0] = (thepad, None)
    >>> tr.mount_prop[0.6] = (thepad, None)
    >>> tr.mount_prop[1.2] = (thepad, None)
    ...
    """

    # Pad instance
    pad = Instance(DiscrPad)

    # Distance between mounting positions
    distance = Float()

    # Number of mounting positions
    num_mount = Integer()

    def __init__(self, *args, **kwargs):
        # Set the mounting properties
        super().__init__(*args, **kwargs)
        x = 0
        for _i in range(self.num_mount):
            self.mount_prop[x] = (self.pad, None)
            x += self.distance

class ArrangedSlabSingleRailTrack(DiscrSlabSingleRailTrack):
    """Single rail arranged slab track class.

    Rail is mounted discretely. Mounting properties may vary.

    Example:
    --------
    >>> tr = ArrangedSlabSingleRailTrack(rail = UIC60)
    >>> tr.mount_prop[0.0] = (thepadA, None)
    >>> tr.mount_prop[0.65] = (thepadA, None)
    >>> tr.mount_prop[1.15] = (thepadB, None)
    >>> tr.mount_prop[1.8] = (thepadB, None)
    ...
    """

    # Pad instance
    pad = Instance(Arrangement)

    # Distance between mounting positions
    distance = Instance(Arrangement)

    # Number of mounting positions
    num_mount = Integer()

    def __init__(self, *args, **kwargs):
        # Set the mounting properties
        super().__init__(*args, **kwargs)
        x = 0
        for p, d in zip(self.pad.generate(self.num_mount),
                        self.distance.generate(self.num_mount), strict=False):
            self.mount_prop[x] = (p, None)
            x += d


class BallastedSingleRailTrack(SingleRailTrack):
    """Ballasted single rail track class.

    This class represents a single rail track with ballast.
    """

    # Ballast instance
    ballast = Instance(Ballast)


class ContBallastedSingleRailTrack(BallastedSingleRailTrack):
    """Continuous ballasted single rail track class.

    This class represents a single rail track with ballast, pads and a slab.

    Example:
    --------
    >>> tr = BallastedSingleRailTrack(rail = UIC60, ballast = default_ballast)
    >>> tr.pad = thepad
    >>> tr.slab = theslab
    ...
    """

    # Pad instance
    pad = Instance(ContPad)

    # Sleeper instance
    slab = Instance(Slab)


class DiscrBallastedSingleRailTrack(BallastedSingleRailTrack):
    """Ballasted single rail track class.

    This class represents a single rail track with ballast, pads and sleepers and
    allows for nonuniform properties of pads and sleepers.
    """

    # Pads and sleepers may have nonuniform properties Dictionary (x-> (Pad, Sleeper))
    mount_prop = Dict(value_trait=Float(), key_trait=Tuple(DiscrPad, Sleeper))

    def __repr__(self):
        """Represent mounting properties as string."""
        st = ""
        for x in sorted(self.mount_prop.keys()):
            p, s = self.mount_prop[x]
            st += f'{x}, {p.sp}, {s.ms} \n'
        return st


class SimplePeriodicBallastedSingleRailTrack(DiscrBallastedSingleRailTrack):
    """Class to generate a simple periodic ballasted single rail track.

    All mounting properties are uniform.

    Example:
    --------
    >>> tr = SimplePeriodicBallastedSingleRailTrack(rail = UIC60, ballast = default_ballast)
    >>> tr.mount_prop[0.0] = (thepad, thesleeper)
    >>> tr.mount_prop[0.6] = (thepad, thesleeper)
    ...
    """

    # Sleeper instance
    sleeper = Instance(Sleeper)

    # Pad instance
    pad = Instance(DiscrPad)

    # Sleeper distance
    distance = Float()

    # Sleeper count
    num_mount = Integer()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        x = 0
        for _i in range(self.num_mount):
            self.mount_prop[x] = (self.pad, self.sleeper)
            x += self.distance


class ArrangedBallastedSingleRailTrack(DiscrBallastedSingleRailTrack):
    """Class to generate an arranged ballasted single rail track.

    Mounting properties may vary.

    Example:
    --------
    >>> tr = ArrangedBallastedSingleRailTrack(rail = UIC60, ballast = default_ballast)
    >>> tr.mount_prop[0.0] = (thepadA, thesleeperA)
    >>> tr.mount_prop[0.55] = (thepadA, thesleeperA)
    >>> tr.mount_prop[1.3] = (thepadB, thesleeperB)
    >>> tr.mount_prop[1.85] = (thepadB, thesleeperB)
    """

    # Sleeper instance
    sleeper = Instance(Arrangement)

    # Pad instance
    pad = Instance(Arrangement)

    # Sleeper distance instance
    distance = Instance(Arrangement)

    # Number of mounting positions
    num_mount = Integer()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # factory
        x = 0
        for s, p, d in zip(self.sleeper.generate(self.num_mount),
                           self.pad.generate(self.num_mount),
                           self.distance.generate(self.num_mount), strict=False):
            self.mount_prop[x] = (p, s)
            x += d
