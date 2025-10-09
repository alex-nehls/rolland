"""Defines excitation classes for FDM simulation.

.. autosummary::
    :toctree: excitation

    Excitation
    StationaryExcitation
    GaussianImpulse
    MovingExcitation
"""

import abc

from numpy import exp
from traitlets import Float, List, Union

from .abstract_traits import ABCHasTraits


class Excitation(ABCHasTraits):
    """Abstract base class for excitation."""

    @abc.abstractmethod
    def validate_excitation(self):
        """Validate excitation parameters."""


class StationaryExcitation(Excitation):
    """Abstract base class for stationary excitation."""


class GaussianImpulse(StationaryExcitation):
    """Gaussian impulse excitation class.

    Gaussian impulse according to :cite:t:`stampka2022a`. This excitation type is used for
    non-moving sources.

    Attributes
    ----------
    sigma : float
        Pulse parameter (regulates pulse-time) :math:`[-]`.
    a : float
        Pulse parameter (regulates amplitude) :math:`[s]`.
    x_excit : float
        Excitation position :math:`[m]`.
    """

    sigma = Float(default_value=0.7e-4)
    a = Float(default_value=0.5e2)
    x_excit = Union([List(), Float(default_value=50.0)])

    def validate_excitation(self):
        """Validate excitation parameters."""

    def validate_stationary_excitation(self):
        """Validate stationary excitation parameters."""

    def force(self, t):
        """Compute force array (contains force over time)."""
        tg = t - 4 * self.sigma
        return self.a * tg / self.sigma ** 2 * exp(-tg ** 2 / self.sigma ** 2)


class MovingExcitation(Excitation):
    """Moving excitation class."""


class ConstantForce(MovingExcitation):
    """Constant force excitation class.

    This excitation type is used for moving sources.

    Attributes
    ----------
    x_excit : float
        Excitation position :math:`[m]`.
    """

    force_amplitude = Float(default_value=50000.0)
    # x_excit_start = Union([List(), Float(default_value=50.0)])    # TODO: use this as starting point and move every timestep
    x_excit = Union([List(), Float(default_value=50.0)])            # NOTE: doesn't work for multiple excitation points

    def validate_excitation(self):
        """Validate excitation parameters."""

    def force(self, t):
        """Compute force array (contains force over time)."""
        force_array = [self.force_amplitude] * len(t)
        return force_array