"""Defines excitation classes for FDM simulation.

.. autosummary::
    :toctree: excitation

    Excitation
    StationaryExcitation
    GaussianImpulse
    MovingExcitation
"""

import abc
import numpy as np

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

    sigma = Float(default_value = 0.7e-4)
    a = Float(default_value = 0.5e2)
    x_excit = Union([List(), Float(default_value = 50.0)])

    def validate_excitation(self):
        """Validate excitation parameters."""

    def validate_stationary_excitation(self):
        """Validate stationary excitation parameters."""

    def force(self, t):
        """Compute force array (contains force over time)."""
        tg          = t - 4 * self.sigma
        force_array = self.a*tg / self.sigma**2 * np.exp(-tg**2 / self.sigma**2)
        return force_array


class MovingExcitation(Excitation):
    """Moving excitation class."""


class ConstantForce(MovingExcitation):
    """Constant force excitation class for single or multiple moving loads.

    Attributes
    ----------
    x_excit : list or float
        Starting position(s) of excitation point(s) :math:`[m]`.
    force_amplitude : float
        Force amplitude per wheel :math:`[N]`.
    """

    force_amplitude = Float(default_value=65000.0)
    x_excit = Union([List(), Float(default_value = 50.0)])
    velocity = Float(default_value=27.78)  # default 100 km/h in m/s

    def validate_excitation(self):
        """Validate excitation parameters."""

    def force(self, t):
        """Compute force array (contains force over time)."""
        n = len(t)
        ramp_length = int(0.05 * n)  # 10% of total length
        force_array = []
        
        # Linear ramp up for first 10%
        for i in range(ramp_length):
            force_array.append(self.force_amplitude * (i / ramp_length))
            
        # Constant force with random component for remaining 90%
        np.random.seed(42)  # für Reproduzierbarkeit
        # random_component = np.random.uniform(
        #     low     = -0.1 * self.force_amplitude,
        #     high    = 0.1 * self.force_amplitude,
        #     size    = n - ramp_length
        # )
        # random_component = np.random.uniform(
        #     low     = 0,
        #     high    = self.force_amplitude,
        #     size    = n - ramp_length
        # )
        constant_part = [self.force_amplitude] * (n - ramp_length)


        # force_array.extend(np.array(constant_part) + random_component)
        force_array.extend(np.array(constant_part))


        return force_array