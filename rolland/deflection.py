"""Defines deflection classes for FDM simulation.

.. autosummary::
    :toctree: deflection

    Deflection
    DeflectionEBBVertic
"""

import abc

from numpy import empty, linspace, zeros
import numpy as np
from scipy.sparse.linalg import splu
from traitlets import Instance, Bool

from .abstract_traits import ABCHasTraits
from .discretization import Discretization
from .excitation import Excitation


class Deflection(ABCHasTraits):
    r"""Abstract base class for deflection classes.

    Attributes
    ----------
    excit : Excitation
        Excitation instance.
    discr : Discretization
        Discretization instance.
    """

    discr = Instance(Discretization)
    excit = Instance(Excitation)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.track = self.discr.track

    @abc.abstractmethod
    def validate_deflection(self):
        """Validate deflection."""


class DeflectionEBBVertic(Deflection):
    r"""Calculate deflection according to :cite:t:`stampka2022a`.

    Attributes
    ----------
    track : Track
        Track instance.
    excit : Excitation
        Excitation instance.
    discr : Discretization
        Discretization instance.
    deflection : numpy.ndarray
        Deflection array :math:`[m]`.
    store_deflection : bool
        If True, store the full deflection matrix. If False, only store contact-point deflections.
    excitation_index : int
        Index of excitation point :math:`[-]`.
    """
    store_deflection = Bool(default_value=True)

    def __init__(self, *args, **kwargs):
        """
        Initialize the DeflectionFDMStampka class.

        Parameters
        ----------
        *args : tuple
            Variable length argument list.
        **kwargs : dict
            Arbitrary keyword arguments.

        Attributes
        ----------
        deflection : numpy.ndarray
            Array of calculated deflections with shape (2 * nx, nt + 1).
        """
        super().__init__(*args, **kwargs)

        # Initialize starting values
        self.calc_force()
        defl = self.initialize_start_values()

        # Calculate deflection
        self.deflection = self.calc_deflection(defl)

    def validate_deflection(self):
        """Validate deflection."""

    def initialize_start_values(self):
        # TODO: add option to initialize with static deflection instead of zeros
        """Set starting values of deflections to zero.

        Returns
        -------
        defl : numpy.ndarray
            Array of deflections initialized to zero with shape (2 * nx, nt + 1).
        """
        defl = empty((2 * self.discr.nx, self.discr.nt + 1))

        # Set starting values to zero for two time steps
        defl[:, 0:2] = zeros((2 * self.discr.nx, 2))
        return defl

    def calc_force(self):
        """Calculate force array."""
        t = linspace(0, self.discr.sim_t, self.discr.nt)
        self.force = self.excit.force(t)

    def calc_rightside_crank_nicolson(self, u1, u0, excitation_index, t):
        """Calculate the right-hand side of the equation according to :cite:t:`stampka2022a`.

        Parameters
        ----------
        u1 : numpy.ndarray
            Deflection array at the current time step.
        u0 : numpy.ndarray    
            Deflection array at the previous time step.
        excitation_index : int
            Index of the excitation point.
        t : int
            Current time step.

        Returns
        -------
        numpy.ndarray
            Right-hand side of the equation.
        """
        # create empty force array with length equal to number of DOFs (2*nx)
        f = zeros(2 * self.discr.nx)

        # Handle multiple excitation points if excitation_index is a list
        if isinstance(excitation_index, list):
            for idx in excitation_index:
                f[idx] = self.force[t]
        else:
            f[excitation_index] = self.force[t]

        return (self.discr.B.dot(u1) + self.discr.C.dot(u0) + self.discr.dt ** 2 /
                (self.track.rail.mr * self.discr.dx) * f)


    def calc_deflection(self, defl):
        """Calculate deflection using Crank-Nicolson time-stepping.
        
        For moving loads, contact point positions are updated each timestep
        based on velocity: position(t) = initial_position + velocity * t
        
        Returns
        -------
        defl : numpy.ndarray
            Full deflection history (2*nx, nt+1) containing rail and sleeper DOFs
        """
        # Convert single excitation point to list for uniform handling
        if not isinstance(self.excit.x_excit, list):
            self.excit.x_excit = [self.excit.x_excit]
        
        # Calculate initial indices for all excitation points
        self.excitation_indices = [int(x / self.discr.dx) for x in self.excit.x_excit]
        
        # Array for storing deflection at contact points over time
        self.contact_point_deflection = [[] for _ in self.excitation_indices]
        
        # Factorization of matrix A (LU decomposition)
        self.factoriz = splu(self.discr.A)

        # # static defletion at t=0 (initial condition)
        # eps = 1e-12  # convergence criterion
        # diff = np.inf  # initialize difference for convergence check
        # while diff > eps:  # iterate until convergence
        #     defl_old = defl.copy()  # create a copy of the current deflection array TODO: drop need to copy
        #     self.crank_nicolson_step(defl, t=0, excitation_pos=self.excitation_indices)
        #     diff = np.max(np.abs(defl - defl_old))  # update difference for convergence check

        for i in range(len(self.excitation_indices)):
            # Store initial deflection at contact points (should be zero at t=0)
            self.contact_point_deflection[i].append(defl[self.excitation_indices[i],0])  # initial deflection at t=0

        # loop for calculating deflection at each time step
        # NOTE: starts from t=1 because we need defl at t-1 and t-2 for the Crank-Nicolson scheme
        for t in range(1, self.discr.nt):
            # Calculate current positions based on velocity
            dx = round((self.excit.velocity * t * self.discr.dt) / self.discr.dx)   # Calculate how many grid points the load has moved
            excitation_pos = [idx + dx for idx in self.excitation_indices]          # Update excitation indices for current time step
            
            self.crank_nicolson_step(defl, t, excitation_pos)

            # Store deflection at each contact point
            for i, idx in enumerate(excitation_pos):
                contact_deflection = defl[idx, t]
                self.contact_point_deflection[i].append(contact_deflection) # Store deflection at newly calculated contact point
        return defl # TODO: check why deflection is longer than contact_defl and force
    
    def crank_nicolson_step(self, defl, t, excitation_pos):
        # Calculate right hand side of equation
        b = self.calc_rightside_crank_nicolson(
            u1 = defl[:, t-1],
            u0 = defl[:, t-2],
            excitation_index = excitation_pos,
            t = t
        )
        # Calculate deflection for time step t
        u = self.factoriz.solve(b)
        defl[:, t] = u[0:2 * self.discr.nx]

        return

##################################################################################################################################
##################################################################################################################################
# f = f_old
# for i in range(max_iter):
#     y_r = rail_deflection(f)            # Schienenverformung
#     y_s = roughness(f)                  # Gleisrauheit
#     y_w = wheel_deflection(f)           # Radverformung
#     delta_lin = y_r + y_s - y_w         # geometrische Eindringung

#     if delta_lin <= 0:
#         f = 0
#         break

#     f_new = (delta_lin / C)**(3/2)      # Hertz-Gesetz
#     if abs(f_new - f) < eps:            # Fehlerprüfung
#         f = f_new
#         break
#     f = f_new
##################################################################################################################################
##################################################################################################################################