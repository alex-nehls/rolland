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

class HertzianForce(MovingExcitation):
    """Hertzian force excitation class for single or multiple moving loads.

    Attributes
    ----------
    x_excit : list or float
        Starting position(s) of excitation point(s) :math:`[m]`.
    initial_force : float
        Force amplitude per wheel :math:`[N]`.
    velocity : float
        Velocity of the moving load (train) :math:`[m/s]`.
    """
    vel_ramp_fraction   = Float(default_value=0.1)  # fraction of total time for acceleration
    initial_force   = Float(default_value=65000.0)
    x_excit         = Union([List(), Float(default_value = 50.0)])
    velocity        = Float(default_value=27.78)  # default 100 km/h in m/s
    
    def validate_excitation(self):
        """Validate excitation parameters."""

    def force(self, t):
        """Compute force array (contains force over time)."""
        n = len(t)
        force_array = []
        self.ramp_length = int(self.ramp_fraction * n)
        
        # Linear ramp up
        for i in range(self.ramp_length):
            force_array.append(self.force_amplitude * (i / self.ramp_length))
            
        # constant force after ramp up
        constant_part = [self.force_amplitude] * (n - self.ramp_length)

        # concatenating the rampup with the constant part
        force_array.extend(constant_part)

        return force_array

class RandomForce(MovingExcitation):
    """Random force excitation class for single or multiple moving loads.

    Attributes
    ----------
    x_excit : list or float
        Starting position(s) of excitation point(s) :math:`[m]`.
    force_amplitude : float
        Force amplitude per wheel :math:`[N]`.
    ramp_fraction : float
        Fraction of the total simulation time used for the force buildup :math:`[-]`.
    velocity : float
        Velocity of the moving load (train) :math:`[m/s]`.
    """
    vel_ramp_fraction   = Float(default_value=0.1)  # fraction of total time for acceleration
    ramp_fraction   = Float(default_value=0.1)  # fraction of total time for ramp up
    force_amplitude = Float(default_value=65000.0)
    x_excit         = Union([List(), Float(default_value = 50.0)])
    velocity        = Float(default_value=27.78)  # default 100 km/h in m/s
    
    def validate_excitation(self):
        """Validate excitation parameters."""

    def force(self, t):
        """Compute force array (contains force over time)."""
        n = len(t)
        force_array = []
        self.ramp_length = int(self.ramp_fraction * n)
        
        # Linear ramp up
        for i in range(self.ramp_length):
            force_array.append(self.force_amplitude * (i / self.ramp_length))
            
        # random force between force_amplitude and 2*force_amplitude
        constant_part = [self.force_amplitude] * (n - self.ramp_length)
        np.random.seed(42)  # für Reproduzierbarkeit
        random_part = np.random.uniform(
            low     = 0 * self.force_amplitude,
            high    = 1 * self.force_amplitude,
            size    = n - self.ramp_length
        )

        # concatenating the rampup with the constant and random part
        force_array.extend(constant_part + random_part)

        return force_array