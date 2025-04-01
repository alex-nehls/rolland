"""Arrangement classes for the definition of non-uniform mounting properties.

.. autosummary::
    :toctree: arrangement

    Arrangement
    PeriodicArrangement
    RandomArrangement
"""

import abc
import random

from scipy.stats import truncnorm
from traitlets import Any

from .abstract_traits import ABCHasTraits


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


class RandomArrangement(Arrangement):
    r"""Random arrangement of given objects.

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
    >>> from rolland.arrangement import RandomArrangement
    >>> from rolland.track import ArrangedBallastedSingleRailTrack

    >>> thepadA = DiscrPad(sp = [300*10**6, 0], dp = [30000, 0])
    >>> thepadB = DiscrPad(sp = [400*10**6, 0], dp = [40000, 0])
    >>> thesleeperA = Sleeper(ms = 150)
    >>> thesleeperB = Sleeper(ms = 200)
    >>> pad = RandomArrangement(item=[thepadA, thepadB])
    >>> distance = RandomArrangement(item=[0.65, 0.5])
    >>> sleeper = RandomArrangement(item=[thesleeperA, thesleeperB])
    >>> tr = ArrangedBallastedSingleRailTrack(
    ...     rail=UIC60,
    ...     pad=pad,
    ...     sleeper=sleeper,
    ...     distance=distance,
    ...     num_mount=100)
    """

    def generate(self, num_mount):
        """Generate count repetitions of objects."""
        for _ in range(num_mount):
            if isinstance(self.item, list):
                yield random.choice(self.item)
            else:
                yield self.item

    @staticmethod
    def trunc_norm(mean, sd, minv, max_v) -> float:
        """Calculate truncated normal distribution.

        Parameters
        ----------
        mean : float
            Mean value.
        sd : float
            Standard deviation.
        minv : float
            Minimum value.
        max_v : float
            Maximum value.

        Returns
        -------
        object
        """
        sd = sd + 1e-6  # Low value added to avoid error.
        minv = minv - 1e-6
        max_v = max_v + 1e-6
        return float(truncnorm((minv - mean) / sd, (max_v - mean) / sd, loc=mean, scale=sd).rvs(1))
