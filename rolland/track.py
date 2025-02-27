"""Defines track structure and arrangement.

.. autosummary::
    :toctree: track

    Track
    SingleRailTrack
    SlabSingleRailTrack
    ContSlabSingleRailTrack
    DiscrSlabSingleRailTrack
    SimplePeriodicSlabSingleRailTrack
    ArrangedSlabSingleRailTrack
    BallastedSingleRailTrack
    ContBallastedSingleRailTrack
    DiscrBallastedSingleRailTrack
    SimplePeriodicBallastedSingleRailTrack
    ArrangedBallastedSingleRailTrack
"""
import abc
from decimal import Decimal

from traitlets import Dict, Float, Instance, Integer, Tuple

from rolland.abstract_traits import ABCHasTraits
from rolland.arrangement import Arrangement
from rolland.components import Ballast, ContPad, DiscrPad, Rail, Slab, Sleeper


class Track(ABCHasTraits):
    r"""Abstract base class for track classes."""

    @abc.abstractmethod
    def validate_track(self):
        """Validate the track configuration."""

class SingleRailTrack(Track):
    r"""Abstract base class for single rail track classes.

    Attributes
    ----------
    rail : Rail
        Rail instance.
    """

    rail = Instance(Rail)

    @abc.abstractmethod
    def validate_single_rail_track(self):
        """Validate the single rail configuration."""

class SlabSingleRailTrack(SingleRailTrack):
    r"""Abstract base class for slab single rail track classes.

    Slab mass is set to a very large number to avoid displacement in order to avoid
    displacement and simulate a rigid slab.

    Attributes
    ----------
    rail : Rail
        Rail instance.
    slab : Slab
        Slab instance.
    """

    slab = Slab()

    def __init__(self, *args, **kwargs):
        # Set the mass of the slab to a very large number to avoid displacement
        super().__init__(*args, **kwargs)
        self.slab.ms = 1e20

    @abc.abstractmethod
    def validate_slab_single_rail_track(self):
        """Validate the slab single rail configuration."""


class ContSlabSingleRailTrack(SlabSingleRailTrack):
    r"""Single rail slab track with continuous support.

    All superstructure properties are continuous along the track. The slab is assumed to be rigid.

    +------------------+-----------+--------------------+-------------+
    | Layer of Support | Component | Condition          | Variability |
    +==================+===========+====================+=============+
    | /                | rail      | continuous         | no          |
    +------------------+-----------+--------------------+-------------+
    | 1st              | pads      | continuous         | no          |
    +------------------+-----------+--------------------+-------------+
    | 1st/2nd          | slab      | continuous (rigid) | no          |
    +------------------+-----------+--------------------+-------------+
    | 2nd              | ballast   | /                  | /           |
    +------------------+-----------+--------------------+-------------+


    Attributes
    ----------
    rail : Rail
        Rail instance.
    slab : Slab
        Slab instance.
    pad : ContPad
        Continuous pad instance.


    Example
    --------
    >>> from rolland.database.rail.db_rail import UIC60
    >>> from rolland.components import ContPad, Slab
    >>> from rolland.track import ContSlabSingleRailTrack

    >>> thepad = ContPad(sp = [300*10**6, 0], dp = [30000, 0])
    >>> theslab = Slab(ms = 250)
    >>> tr = ContSlabSingleRailTrack(rail = UIC60, pad = thepad, slab = theslab)
    >>> tr.pad = thepad
    >>> tr.slab = theslab
    ...
    """

    pad = Instance(ContPad)

    def validate_track(self):
        """Validate the track configuration."""

    def validate_single_rail_track(self):
        """Validate the single rail configuration."""

    def validate_slab_single_rail_track(self):
        """Validate the slab single rail configuration."""


class DiscrSlabSingleRailTrack(SlabSingleRailTrack):
    r"""Abstract base class for discrete slab single rail track classes.

    The pad and sleeper properties are discrete and the slab is assumed to be rigid.

    Attributes
    ----------
    rail : Rail
        Rail instance.
    slab : Slab
        Slab instance.
    pad : DiscrPad
        Discrete pad instance.
    mount_prop : dict
        Dictionary for discrete mounting positions (x-> (Pad, None)).
    """

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

    @abc.abstractmethod
    def validate_discr_slab_single_rail_track(self):
        """Validate the discrete slab single rail configuration."""


class SimplePeriodicSlabSingleRailTrack(DiscrSlabSingleRailTrack):
    r"""Single rail slab track with simple periodic support.

    All mounting properties are uniform and no variation is allowed. Slab is assumed to be rigid.

    +---------+-----------+------------------+-------------+
    | Layer   | Component | Condition        | Variability |
    +=========+===========+==================+=============+
    | /       | rail      | continuous       | no          |
    +---------+-----------+------------------+-------------+
    | 1st     | pads      | discrete         | no          |
    +---------+-----------+------------------+-------------+
    | 1st/2nd | slab      | discrete (rigid) | no          |
    +---------+-----------+------------------+-------------+
    | 2nd     | ballast   | /                | /           |
    +---------+-----------+------------------+-------------+

    Attributes
    ----------
    rail : Rail
        Rail instance.
    slab : Slab
        Slab instance.
    pad : DiscrPad
        Discrete pad instance.
    distance : float
        Distance between mounting positions.
    num_mount : int
        Number of mounting positions.
    mount_prop : dict
        Dictionary for discrete mounting positions (x-> (Pad, None)).


    Example
    --------
    >>> from rolland.database.rail.db_rail import UIC60
    >>> from rolland.components import DiscrPad, Slab
    >>> from rolland.track import SimplePeriodicSlabSingleRailTrack

    >>> thepad = DiscrPad(sp = [300*10**6, 0], dp = [30000, 0])
    >>> theslab = Slab(ms = 250)
    >>> tr = SimplePeriodicSlabSingleRailTrack(
    ...     rail=UIC60,
    ...     pad=thepad,
    ...     slab=theslab,
    ...     distance=0.6,
    ...     num_mount=100)
    >>> tr.mount_prop[0.0] = (thepad, None)
    >>> tr.mount_prop[0.6] = (thepad, None)
    >>> tr.mount_prop[1.2] = (thepad, None)
    ...
    """

    pad = Instance(DiscrPad)
    distance = Float()
    num_mount = Integer()

    def __init__(self, *args, **kwargs):
        # Set the mounting properties
        super().__init__(*args, **kwargs)
        for _i in range(self.num_mount):
            # Calculate the mounting position
            # Use Decimal to avoid floating-point representation errors
            x = float(Decimal(str(_i)) * Decimal(str(self.distance)))
            self.mount_prop[x] = (self.pad, None)

    def validate_track(self):
        """Validate the track configuration."""

    def validate_single_rail_track(self):
        """Validate the single rail configuration."""

    def validate_slab_single_rail_track(self):
        """Validate the slab single rail configuration."""

    def validate_discr_slab_single_rail_track(self):
        """Validate the discrete slab single rail configuration."""


class ArrangedSlabSingleRailTrack(DiscrSlabSingleRailTrack):
    """Single rail slab track with varying periodic support.

    Variations in the form of periodicaly or stochasticaly varying mounting properties are allowed.
    Slab is assumed to be rigid.

    +---------+-----------+------------------+---------------------+
    | Layer   | Component | Condition        | Variability         |
    +=========+===========+==================+=====================+
    | /       | rail      | continuous       | no                  |
    +---------+-----------+------------------+---------------------+
    | 1st     | pads      | discrete         | periodic/stochastic |
    +---------+-----------+------------------+---------------------+
    | 1st/2nd | slab      | discrete (rigid) | periodic/stochastic |
    +---------+-----------+------------------+---------------------+
    | 2nd     | ballast   | /                | /                   |
    +---------+-----------+------------------+---------------------+

    Attributes
    ----------
    rail : Rail
        Rail instance.
    slab : Slab
        Slab instance.
    pad : Arrangement
        Arrangement instance containing multiple pads.
    distance : Arrangement

        Arrangement instance containing multiple distances.
    num_mount : int
        Number of mounting positions.
    mount_prop : dict
        Dictionary for discrete mounting positions (x-> (Pad, None)).


    Example
    --------
    >>> from rolland.database.rail.db_rail import UIC60
    >>> from rolland.components import DiscrPad, Slab
    >>> from rolland.arrangement import PeriodicArrangement
    >>> from rolland.track import ArrangedSlabSingleRailTrack

    >>> thepadA = DiscrPad(sp = [300*10**6, 0], dp = [30000, 0])
    >>> thepadB = DiscrPad(sp = [400*10**6, 0], dp = [40000, 0])
    >>> theslab = Slab(ms = 250)
    >>> pad = PeriodicArrangement(item=[thepadA, thepadB])
    >>> distance = PeriodicArrangement(item=[0.65, 0.5])
    >>> tr = ArrangedSlabSingleRailTrack(
    ...     rail=UIC60,
    ...     pad=pad,
    ...     slab=theslab,
    ...     distance=distance,
    ...     num_mount=100)
    >>> tr.mount_prop[0.0] = (thepadA, None)
    >>> tr.mount_prop[0.65] = (thepadA, None)
    >>> tr.mount_prop[1.15] = (thepadB, None)
    >>> tr.mount_prop[1.8] = (thepadB, None)
    ...
    """

    pad = Instance(Arrangement)
    distance = Instance(Arrangement)
    num_mount = Integer()

    def __init__(self, *args, **kwargs):
        # Set the mounting properties
        super().__init__(*args, **kwargs)
        x = Decimal(str(0))
        for p, d in zip(self.pad.generate(self.num_mount),
                        self.distance.generate(self.num_mount), strict=False):
            self.mount_prop[float(Decimal(str(x)))] = (p, None)
            x += Decimal(str(d))

    def validate_track(self):
        """Validate the track configuration."""

    def validate_single_rail_track(self):
        """Validate the single rail configuration."""

    def validate_slab_single_rail_track(self):
        """Validate the slab single rail configuration."""

    def validate_discr_slab_single_rail_track(self):
        """Validate the discrete slab single rail configuration."""


class BallastedSingleRailTrack(SingleRailTrack):
    r"""Abstract base class for ballasted single rail track classes.

    Attributes
    ----------
    rail : Rail
        Rail instance.
    ballast : Ballast
        Ballast instance.
    """

    ballast = Instance(Ballast)

    @abc.abstractmethod
    def validate_ballasted_single_rail_track(self):
        """Validate the ballasted single rail configuration."""


class ContBallastedSingleRailTrack(BallastedSingleRailTrack):
    r"""Single rail slab track with ballasted support.

    All superstructure properties are continuous along the track.

    .. note:: Properties of ballast need to be defined as continious values (per meter).

    +---------+-----------+------------+-------------+
    | Layer   | Component | Condition  | Variability |
    +=========+===========+============+=============+
    | /       | rail      | continuous | no          |
    +---------+-----------+------------+-------------+
    | 1st     | pads      | continuous | no          |
    +---------+-----------+------------+-------------+
    | 1st/2nd | slab      | continuous | no          |
    +---------+-----------+------------+-------------+
    | 2nd     | ballast   | continuous | no          |
    +---------+-----------+------------+-------------+

    Attributes
    ----------
    rail : Rail
        Rail instance.
    pad : ContPad
        Continuous pad instance.
    slab : Slab
        Slab instance.
    ballast : Ballast
        Ballast instance.


    Example
    --------
    >>> from rolland.database.rail.db_rail import UIC60
    >>> from rolland.components import ContPad, Slab
    >>> from rolland.track import ContBallastedSingleRailTrack

    >>> thepad = ContPad(sp = [300*10**6, 0], dp = [30000, 0])
    >>> theslab = Slab(ms = 250)
    >>> tr = ContBallastedSingleRailTrack(rail = UIC60, pad = thepad, slab = theslab)
    >>> tr.pad = thepad
    >>> tr.slab = theslab
    ...
    """

    pad = Instance(ContPad)
    slab = Instance(Slab)

    def validate_track(self):
        """Validate the track configuration."""

    def validate_single_rail_track(self):
        """Validate the single rail configuration."""

    def validate_ballasted_single_rail_track(self):
        """Validate the ballasted single rail configuration."""


class DiscrBallastedSingleRailTrack(BallastedSingleRailTrack):
    """Abstract base class for discrete ballasted single rail track classes.

    The pad and sleeper properties are discrete.

    Attributes
    ----------
    rail : Rail
        Rail instance.
    ballast : Ballast
        Ballast instance.
    mount_prop : dict
        Dictionary for discrete mounting positions (x-> (Pad, Sleeper)).
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

    @abc.abstractmethod
    def validate_discr_ballasted_single_rail_track(self):
        """Validate the discrete ballasted single rail configuration."""


class SimplePeriodicBallastedSingleRailTrack(DiscrBallastedSingleRailTrack):
    """Single rail ballasted track with simple periodic support.

    All mounting properties are uniform and no variation is allowed.

    .. note:: Properties of ballast need to be defined as discrete values.


    +---------+-----------+------------+-------------+
    | Layer   | Component | Condition  | Variability |
    +=========+===========+============+=============+
    | /       | rail      | continuous | no          |
    +---------+-----------+------------+-------------+
    | 1st     | pads      | discrete   | no          |
    +---------+-----------+------------+-------------+
    | 1st/2nd | sleeper   | discrete   | no          |
    +---------+-----------+------------+-------------+
    | 2nd     | ballast   | discrete   | no          |
    +---------+-----------+------------+-------------+

    Attributes
    ----------
    rail : Rail
        Rail instance.
    ballast : Ballast
        Ballast instance.
    pad : ContPad
        Continuous pad instance.
    sleeper : Instance of :class:`~rolland.components.sleeper` class
        Sleeper instance.
    distance : float
        Distance between mounting positions.
    num_mount : int
        Number of mounting positions.
    mount_prop : dict


    Example
    --------
    >>> from rolland.database.rail.db_rail import UIC60
    >>> from rolland.components import DiscrPad, Sleeper
    >>> from rolland.track import SimplePeriodicBallastedSingleRailTrack

    >>> thepad = DiscrPad(sp = [300*10**6, 0], dp = [30000, 0])
    >>> thesleeper = Sleeper(ms = 150)
    >>> distance = 0.6
    >>> tr = SimplePeriodicBallastedSingleRailTrack(
    ...     rail=UIC60,
    ...     pad=thepad,
    ...     sleeper=thesleeper,
    ...     distance=distance,
    ...     num_mount=100)
    >>> tr.mount_prop[0.0] = (thepad, thesleeper)
    >>> tr.mount_prop[0.6] = (thepad, thesleeper)
    ...
    """

    sleeper = Instance(Sleeper)
    pad = Instance(DiscrPad)
    distance = Float()
    num_mount = Integer()

    def __init__(self, *args, **kwargs):
        # Set the mounting properties
        super().__init__(*args, **kwargs)
        for _i in range(self.num_mount):
            # Calculate the mounting position
            # Use Decimal to avoid floating-point representation errors
            x = float(Decimal(str(_i)) * Decimal(str(self.distance)))
            self.mount_prop[x] = (self.pad, self.sleeper)

    def validate_track(self):
        """Validate the track configuration."""

    def validate_single_rail_track(self):
        """Validate the single rail configuration."""

    def validate_ballasted_single_rail_track(self):
        """Validate the ballasted single rail configuration."""

    def validate_discr_ballasted_single_rail_track(self):
        """Validate the discrete ballasted single rail configuration."""


class ArrangedBallastedSingleRailTrack(DiscrBallastedSingleRailTrack):
    """Single rail ballasted track with varying periodic support.

    Variations in the form of periodicaly or stochasticaly varying mounting properties are allowed.

    .. note:: Properties of ballast need to be defined as discrete values.

    +---------+-----------+------------+---------------------+
    | Layer   | Component | Condition  | Variability         |
    +=========+===========+============+=====================+
    | /       | rail      | continuous | no                  |
    +---------+-----------+------------+---------------------+
    | 1st     | pads      | discrete   | periodic/stochastic |
    +---------+-----------+------------+---------------------+
    | 1st/2nd | sleepers  | discrete   | periodic/stochastic |
    +---------+-----------+------------+---------------------+
    | 2nd     | ballast   | discrete   | no                  |
    +---------+-----------+------------+---------------------+

    Attributes
    ----------
    rail : Rail
        Rail instance.
    ballast : Ballast
        Ballast instance.
    pad : Arrangement
        Arrangement instance containing multiple pads.
    sleeper : Arrangement
        Arrangement instance containing multiple sleepers.
    distance : Arrangement
        Arrangement instance containing multiple distances.
    num_mount : int
        Number of mounting positions.
    mount_prop : dict
        Dictionary for discrete mounting positions (x-> (Pad, Sleeper)).


    Example
    --------
    >>> from rolland.database.rail.db_rail import UIC60
    >>> from rolland.components import DiscrPad, Sleeper
    >>> from rolland.arrangement import PeriodicArrangement
    >>> from rolland.track import ArrangedBallastedSingleRailTrack

    >>> thepadA = DiscrPad(sp = [300*10**6, 0], dp = [30000, 0])
    >>> thepadB = DiscrPad(sp = [400*10**6, 0], dp = [40000, 0])
    >>> thesleeperA = Sleeper(ms = 150)
    >>> thesleeperB = Sleeper(ms = 200)
    >>> pad = PeriodicArrangement(item=[thepadA, thepadB])
    >>> distance = PeriodicArrangement(item=[0.65, 0.5])
    >>> sleeper = PeriodicArrangement(item=[thesleeperA, thesleeperB])
    >>> tr = ArrangedBallastedSingleRailTrack(
    ...     rail=UIC60,
    ...     pad=pad,
    ...     sleeper=sleeper,
    ...     distance=distance,
    ...     num_mount=100)
    >>> tr.mount_prop[0.0] = (thepadA, thesleeperA)
    >>> tr.mount_prop[0.65] = (thepadB, thesleeperB)
    >>> tr.mount_prop[1.15] = (thepadA, thesleeperA)
    >>> tr.mount_prop[1.8] = (thepadB, thesleeperB)
    ...
    """

    sleeper = Instance(Arrangement)
    pad = Instance(Arrangement)
    distance = Instance(Arrangement)
    num_mount = Integer()

    def __init__(self, *args, **kwargs):
        # Set the mounting properties
        super().__init__(*args, **kwargs)
        x = Decimal(str(0))
        for s, p, d in zip(self.sleeper.generate(self.num_mount),
                           self.pad.generate(self.num_mount),
                           self.distance.generate(self.num_mount), strict=False):
            self.mount_prop[float(Decimal(str(x)))] = (p, s)
            x += Decimal(str(d))

    def validate_track(self):
        """Validate the track configuration."""

    def validate_single_rail_track(self):
        """Validate the single rail configuration."""

    def validate_ballasted_single_rail_track(self):
        """Validate the ballasted single rail configuration."""

    def validate_discr_ballasted_single_rail_track(self):
        """Validate the discrete ballasted single rail configuration."""
