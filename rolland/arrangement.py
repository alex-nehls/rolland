"""Arrangement classes for the definition of non-uniform mounting properties.

.. autosummary::
    :toctree: arrangement

    Arrangement
    PeriodicArrangement
    StochasticArrangement
"""

import abc
import random

from abstract_traits import ABCHasTraits
from traitlets import Any


class Arrangement(ABCHasTraits):
    r"""Abstract base class for the definition of non-uniform mounting properties.

    Attributes
    ----------
    item : any
        Characteristic object or objects to repeat.
    """

    item = Any()

    @abc.abstractmethod
    def generate(self, num_mount):
        """Generate count repetitions of objects."""


class PeriodicArrangement(Arrangement):
    r"""Periodic arrangement of given objects.

    Given sequence of objects is repeated periodically when building track using
    :class:`~rolland.track.ArrangedSlabSingleRailTrack` or
    :class:`~rolland.track.ArrangedBallastedSingleRailTrack` class. Mounting positions start at
    :math:`x=0`.

    Attributes
    ----------
    item : any
        Characteristic object or objects to repeat.

    Example
    --------
    >>> from rolland.database.rail.db_rail import UIC60
    >>> from rolland.components import DiscrPad, Sleeper
    >>> from rolland.arrangement import PeriodicArrangement
    >>> from track import ArrangedBallastedSingleRailTrack

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

    def generate(self, num_mount):
        """Generate count repetitions of objects."""
        c = 0
        while c < num_mount:
            if isinstance(self.item, list):
                for item_ in self.item:
                    yield item_
                    c += 1
            else:
                yield self.item
                c += 1


class StochasticArrangement(Arrangement):
    r"""Stochastic arrangement of given objects.

    Given sequence of objects is repeated randomly when building track using
    :class:`~rolland.track.ArrangedSlabSingleRailTrack` or
    :class:`~rolland.track.ArrangedBallastedSingleRailTrack` class. Mounting positions start at
    :math:`x=0`.

    Attributes
    ----------
    item : any
        Characteristic object or objects to repeat.

    Example
    --------
    >>> from rolland.database.rail.db_rail import UIC60
    >>> from rolland.components import DiscrPad, Sleeper
    >>> from rolland.arrangement import StochasticArrangement
    >>> from rolland.track import ArrangedBallastedSingleRailTrack

    >>> thepadA = DiscrPad(sp = [300*10**6, 0], dp = [30000, 0])
    >>> thepadB = DiscrPad(sp = [400*10**6, 0], dp = [40000, 0])
    >>> thesleeperA = Sleeper(ms = 150)
    >>> thesleeperB = Sleeper(ms = 200)
    >>> pad = StochasticArrangement(item=[thepadA, thepadB])
    >>> distance = StochasticArrangement(item=[0.65, 0.5])
    >>> sleeper = StochasticArrangement(item=[thesleeperA, thesleeperB])
    >>> tr = ArrangedBallastedSingleRailTrack(
    ...     rail=UIC60,
    ...     pad=pad,
    ...     sleeper=sleeper,
    ...     distance=distance,
    ...     num_mount=100)
    >>> tr.mount_prop[0.0] = (thepadA, thesleeperA)
    >>> tr.mount_prop[0.65] = (thepadB, thesleeperA)
    >>> tr.mount_prop[1.3] = (thepadB, thesleeperA)
    >>> tr.mount_prop[1.8] = (thepadA, thesleeperB)
    ...
    """

    def generate(self, num_mount):
        """Generate count repetitions of objects."""
        for _ in range(num_mount):
            if isinstance(self.item, list):
                yield random.choice(self.item)
            else:
                yield self.item
