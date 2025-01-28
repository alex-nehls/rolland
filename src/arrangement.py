import random

from traitlets import Any, HasTraits


class Arrangement(HasTraits):
    """Base class for object arrangements."""

    # Characteristic object or objects to repeat
    item = Any()

    def generate(self, num_mount):
        """Generate count repetitions of objects."""


class PeriodicArrangment(Arrangement):
    """Periodic arrangement of objects.

    Fills the track with a periodic sequence of objects.
    """

    def generate(self, num_mount):
        c = 0
        while c<num_mount:
            if isinstance(self.item, list):
                for item_ in self.item:
                    yield item_
                    c += 1
            else:
                yield self.item
                c += 1


class StochasticArrangement(Arrangement):
    """Stochastic arrangement of objects.

    Fills the track with a stochastic sequence of objects.
    """

    def generate(self, num_mount):
        for _ in range(num_mount):
            if isinstance(self.item, list):
                yield random.choice(self.item)
            else:
                yield self.item

