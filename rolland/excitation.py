"""Defines excitation classes for FDM simulation.

.. autosummary::
    :toctree: excitation

    Excitation
    StationaryExcitation
    GaussianImpulse
    MovingExcitation
"""


from numpy import exp, linspace
from traitlets import Float, HasTraits, Instance

from rolland import GridFDMStampka


class Excitation(HasTraits):
    """Base class for excitation."""


class StationaryExcitation(Excitation):
    """Stationary excitation class."""

class GaussianImpulse(StationaryExcitation):
    """Gaussian impulse excitation class.

    Approach according to Stampka.
    """

    # Grid instance
    grid = Instance(GridFDMStampka)

    # Pulse parameter (regulates pulse-time) [-]
    sigma = Float(default_value=0.7e-4)

    # Pulse parameter (regulates amplitude) [s]
    a = Float(default_value=0.5e2)


    def __init__(self, *args, **kwargs):
        """Compute force array."""
        super().__init__(*args, **kwargs)
        # Time array
        t = linspace(0, self.grid.sim_t, self.grid.nt)

        # Compute force array (contains force over time)
        tg = t - 4 * self.sigma
        self.force = self.a * tg / self.sigma ** 2 * exp(-tg ** 2 / self.sigma ** 2)


class MovingExcitation(Excitation):
    """Moving excitation class."""

