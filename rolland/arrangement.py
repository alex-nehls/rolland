"""Arrangement classes for the definition of non-uniform mounting properties.

.. autosummary::
    :toctree: arrangement

    Arrangement
    PeriodicArrangement
    StochasticArrangement
"""

import random

from traitlets import Any, HasTraits


class Arrangement(HasTraits):
    """Base class for the definition of non-uniform mounting properties.

    Attributes
    ----------
    item : any
        Characteristic object or objects to repeat.
    """

    item = Any()

    def generate(self, num_mount):
        """Generate count repetitions of objects."""


class PeriodicArrangement(Arrangement):
    """Periodic arrangement of given objects.

    Given sequence of objects is repeated periodically when building track using
    :class:`~rolland.track.ArrangedSlabSingleRailTrack` or :class:`~rolland.track.ArrangedBallastedSingleRailTrack`
    class. Mounting position start at :math:`x=0`.

    Attributes
    ----------
    item : any
        Characteristic object or objects to repeat.

    Examples
    --------
    >>> from rolland.arrangement import PeriodicArrangement
    >>> thepadA = DiscrPad()
    >>> thepadB = DiscrPad()
    >>> pad = PeriodicArrangement(item=[thepadA, thepadB])
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
    """Stochastic arrangement of given objects.

    Given sequence of objects is repeated randomly when building track using
    :class:`~rolland.track.ArrangedSlabSingleRailTrack` or :class:`~rolland.track.ArrangedBallastedSingleRailTrack`
    class. Mounting position start at :math:`x=0`.

    Attributes
    ----------
    item : any
        Characteristic object or objects to repeat.

    Examples
    --------
    >>> from rolland.arrangement import StochasticArrangement
    >>> thepadA = DiscrPad()
    >>> thepadB = DiscrPad()
    >>> pad = StochasticArrangement(item=[thepadA, thepadB])
    """

    def generate(self, num_mount):
        """Generate count repetitions of objects."""
        for _ in range(num_mount):
            if isinstance(self.item, list):
                yield random.choice(self.item)
            else:
                yield self.item
