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
from pathlib    import Path
import matplotlib.pyplot as plt

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
    excitation_pos : int
        Index of excitation point :math:`[-]`.
    """
    store_deflection = Bool(default_value=True)

    def __getstate__(self):
        # Get the object's state as a dictionary
        state = self.__dict__.copy()
        # Remove the non-pickleable SuperLU object
        if 'factoriz' in state:
            state['factoriz'] = None
        return state

    def __setstate__(self, state):
        # Restore the object's state
        self.__dict__.update(state)
        # Reinitialize the SuperLU object if needed (optional)
        if self.discr and hasattr(self.discr, 'A'):
            self.factoriz = splu(self.discr.A)

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
            Array of calculated deflections with shape (2*nx, nt).
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
            Array of deflections initialized to zero with shape (2*nx, nt).
        """
        defl = empty((2 * self.discr.nx, self.discr.nt))

        # Set starting values to zero for two time steps
        defl[:, 0:2] = zeros((2 * self.discr.nx, 2))
        return defl

    def calc_force(self):
        """Calculate force array."""
        t = linspace(0, self.discr.sim_t, self.discr.nt)
        self.force = self.excit.force(t)

    def calc_rightside_crank_nicolson(self, u1, u0, excitation_pos, t):
        """Calculate the right-hand side of the equation according to :cite:t:`stampka2022a`.

        Parameters
        ----------
        u1 : numpy.ndarray
            Deflection array at the current time step.
        u0 : numpy.ndarray    
            Deflection array at the previous time step.
        excitation_pos : int
            Index of the excitation point (not rounded).
        t : int
            Current time step.

        Returns
        -------
        numpy.ndarray
            Right-hand side of the equation.
        """
        # create empty force array with length equal to number of DOFs (2*nx)
        f = zeros(2 * self.discr.nx)










        # distribute force to the two nearest grid points using linear interpolation
        for pos in excitation_pos:
            lower_idx = int(np.floor(pos))
            upper_idx = int(np.ceil(pos))
            weight_upper = pos - lower_idx
            weight_lower = 1 - weight_upper
            f[lower_idx] += self.force[t] * weight_lower
            f[upper_idx] += self.force[t] * weight_upper

        return (self.discr.B.dot(u1) + self.discr.C.dot(u0) + self.discr.dt ** 2 /
                (self.track.rail.mr * self.discr.dx) * f)


    def calc_deflection(self, defl):
        #################################################
        # TODO: flip defl to (nt, 2*nx) in whole script
        #################################################
        """Calculate deflection using Crank-Nicolson time-stepping.
        For moving loads, contact point positions are updated each timestep
        based on velocity: position(t) = initial_position + velocity*t

        Returns
        -------
        defl : numpy.ndarray
            Full deflection history (2*nx, nt) containing rail and sleeper DOFs
        """
        
        # Calculate initial indices for all excitation points
        self.excitation_indices = [int(x / self.discr.dx) for x in self.excit.x_excit]
        
        # Array for storing deflection at contact points over time
        self.contact_point_deflection = [[] for _ in self.excitation_indices]
        
        # Factorization of matrix A (LU decomposition)
        self.factoriz = splu(self.discr.A)

        

        # # calculate static defletion at t=0 (initial condition)
        # defl_static = zeros((2*self.discr.nx, 10000))   # TODO: put back to 3
        # eps = 2e-6  # convergence criterion
        # step = 0  # initialize time step for static deflection calculation
        # diff = np.inf  # initialize difference for convergence check
        # while diff > eps:  # iterate until convergence is met
        #     pos = step % 3  # position in the static deflection array (0, 1, or 2)  TODO: put back in use
        #     self.crank_nicolson_step(defl_static, t=step, excitation_pos=self.excitation_indices)
        #     if step > 1:
        #         diff = np.max(np.abs( defl_static[:,step] - defl_static[:,step-1] ))  # update difference for convergence check
        #     step += 1
        #     if step == 10000:
        #         break
        #     # if step % 100 == 0:
        #     #     print(f"Static deflection calculation - Step {step}, Max difference: {diff:.2e}")
        # defl[:, 0] = defl_static[:, step-1]  # set initial deflection to converged static deflection
        # defl[:, -1] = defl_static[:, step-1]  # set deflection to be used for t-2 in first dynamic step to converged static deflection

        

        # # 4.6 Plot deflection as individual frames
        # # =============================================================================
        # # Create output directory for frames
        # output_dir = Path('mobility_plots')
        # output_dir.mkdir(exist_ok=True)

        # frames_dir = output_dir / 'frames'

        # # Clear the frames directory if it already exists
        # if frames_dir.exists():
        #     for file in frames_dir.glob('*'):
        #         file.unlink()  # Delete each file in the directory
        # else:
        #     frames_dir.mkdir(exist_ok=True)  # Create the directory if it doesn't exist

        # # Extract deflection data
        # deflection_static = np.transpose(defl_static)
        # deflection_static = deflection_static[:, :deflection_static.shape[1] // 2]  # Take only the rail deflection_static part

        # # Loop through each time step and save a frame as a PNG
        # for step in range(deflection_static.shape[0]): # loop through time steps
        #     if step//60 == 0 or step % 100 == 0:  # Save every 20th frame to reduce number of images
        #         plt.figure(figsize=(10, 5))
        #         plt.plot(deflection_static[step, :], lw=2, label='deflection_static')
        #         plt.xlim(0, deflection_static.shape[1])  # Set x-axis limits to the number of discrete points
        #         plt.ylim(np.max(deflection_static), np.min(deflection_static))
        #         plt.xlabel('Position along the rail')
        #         plt.ylabel('deflection_static [m]')
        #         plt.title(f'Rail deflection_static - Time Step {step}')
        #         plt.grid(True)
        #         plt.legend()  # Add legend to show labels
        #         plt.tight_layout()
        #         plt.savefig(frames_dir / f'frame_{step:04d}.png', dpi=300, bbox_inches='tight')
        #         plt.close()

        for i in range(len(self.excitation_indices)):
            # Store initial deflection at contact points (should be zero at t=0)
            self.contact_point_deflection[i].append(defl[self.excitation_indices[i],0])  # initial deflection at t=0

        # loop for calculating deflection at each time step
        # NOTE: starts from t=1 because we need defl at t-1 and t-2 for the Crank-Nicolson scheme
        for t in range(1, self.discr.nt):
            # Calculate current positions based on velocity with ramp-up
            ramp_steps = int(self.excit.ramp_fraction * self.discr.nt)  # number of time steps for velocity ramp-up
            if t < ramp_steps:
                current_velocity = self.excit.velocity * (t / ramp_steps)  # Linearly ramp up velocity
                # print (f"Time step {t}: Ramping velocity - Current velocity: {current_velocity:.2f} m/s")
            else:
                current_velocity = self.excit.velocity  # Use full velocity after ramp-up
                if t == ramp_steps:
                    print(f"Time step {t}: Velocity ramp-up complete - Current velocity: {current_velocity:.2f} m/s")
                    # print(f"Time step {t}: Force ramp-up complete - Current force: {self.force[t]:.2f} N") TODO: add correct force print

            dx = (current_velocity * t * self.discr.dt) / self.discr.dx  # Calculate how many grid points the load has moved
            excitation_pos = [idx + dx for idx in self.excitation_indices]  # Update excitation indices for current time step
            excitation_round = [int(pos) for pos in excitation_pos]  # Round to nearest grid point indices for storing deflection
            
            # calculate deflection for current time step using Crank-Nicolson scheme
            self.crank_nicolson_step(defl, t, excitation_pos)

            # Store deflection at each contact point
            for i, idx in enumerate(excitation_round):
                contact_deflection = defl[idx, t]
                self.contact_point_deflection[i].append(contact_deflection) # Store deflection at newly calculated contact point
        return defl
    
    def crank_nicolson_step(self, defl, t, excitation_pos):
        # Calculate right hand side of equation
        b = self.calc_rightside_crank_nicolson(
            u1 = defl[:, t-1],
            u0 = defl[:, t-2],
            excitation_pos = excitation_pos,
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