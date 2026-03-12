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
        """
        Validate deflection.
        """




class DeflectionEBBVertic(Deflection):
    r"""
    Calculate deflection according to :cite:t:`stampka2022a`.

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


    def __getstate__(self):
        """
        Get the state of the object for pickling.
        The method is needed for saving the state of the object without the non-pickleable LU factorization.
        """
        state = self.__dict__.copy()    # Get the object's state as a dictionary
        if 'factoriz' in state:
            state['factoriz'] = None    # Remove the non-pickleable SuperLU object
        return state


    def __setstate__(self, state):
        """
        Set the state of the object during unpickling.
        """
        self.__dict__.update(state)     # Restore the object's state


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
        """
        Validate deflection.
        """

    def initialize_start_values(self):
        """
        Set starting values of deflections to zero.

        Returns
        -------
        defl : numpy.ndarray
            Array of deflections initialized to zero with shape (2*nx, nt).
        """
        defl = empty((2 * self.discr.nx, self.discr.nt))

        # Set starting values to zero for two time steps
        defl[:, 0:2] = zeros((2 * self.discr.nx, 2))    # NOTE: can this be dropped?
        return defl


    def interpolate(self, position, values):
        """
        Interpolate value at a given position between two nodes using linear interpolation.
        """
        upper_idx       = int(np.ceil(position))
        lower_idx       = int(np.floor(position))
        upper_weight    = position - lower_idx
        lower_weight    = upper_idx - position
        result          = lower_weight*values[lower_idx] + upper_weight*values[upper_idx]
        return result


    def calc_force(self):
        """Calculate force array."""
        t = linspace(0, self.discr.sim_t, self.discr.nt)
        self.force = self.excit.force(t)


    def calc_rightside_crank_nicolson(self, defl, u1, u0, excitation_pos, t):
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
        f_vec = zeros(2 * self.discr.nx)

        for pos in excitation_pos:
            if len(self.force) <= t:
                # Initialize variables for Hertzian contact calculation
                force = -np.inf  # Initial force
                max_iter = 100  # Maximum number of iterations
                eps = 1e-6  # Convergence criterion



                nu = self.track.rail.nu  # Poisson's ratio of the rail
                G = self.track.rail.G  # Shear modulus of the rail
                Ra = 0.35 # NOTE: hardcoded parameter, get from wheel geometry if available
                alpha = 1 # NOTE: hardcoded parameter, get from wheel geometry if available
                C = ((2*(1-nu))/(G*np.sqrt(Ra)))**(2/3) * alpha

                static_force = self.excit.force_amplitude  # Static force at t=0, can be adjusted if needed
                delta_0 = C*static_force**(2/3)  # Initial guess for penetration based on static force, can be adjusted if needed


                for i in range(max_iter):
                    # TODO: function for interpolation --> handle on point
                    # TODO: function for spreading --> also handle on point
                    # TODO: fix this whole mess!!!

                    # Calculate rail deflection, roughness, and wheel deflection
                    y_r = self.interpolate(pos, u1)                     # Interpolated rail deflection at excitation point
                    y_s = self.interpolate(pos, self.excit.roughness)   # Interpolated track roughness at excitation point
                    # y_w = wheel_deflection                            # Wheel deflection TODO: add wheel deflection calculation

                    # Calculate geometric penetration
                    # TODO: get this right, check directions of deflection and roughness, and add wheel deflection
                    # y_r: rail deflection, positive if rail moves downwards
                    delta_lin = self.y_static - y_r # NOTE: are the directions of y_r & y_s correct?
                    delta_lin += delta_0

                    if delta_lin <= 0: # NOTE: should we check before adding delta_0?
                        force = 0
                        self.force.append(force)  # Store the converged force value for the current time step
                        break

                    # Update force using Hertzian contact law
                    force_new = (delta_lin / C) ** (3 / 2)

                    if abs(force_new - force) < eps:
                        force = force_new
                        self.force.append(force)  # Store the converged force value for the current time step
                        break

                    # Update force for the next iteration
                    force = force_new
                else:
                    print("Warning: Hertzian contact calculation did not converge.")
            else:
                force = self.force[t]
                if t == len(self.force)-1:
                    self.final_pos = pos

            
            # distribute force to the two nearest grid points using linear interpolation
            lower_idx = int(np.floor(pos))
            upper_idx = int(np.ceil(pos))
            weight_upper = pos - lower_idx
            weight_lower = 1 - weight_upper
            f_vec[lower_idx] += force * weight_lower
            f_vec[upper_idx] += force * weight_upper

        return (self.discr.B.dot(u1) + self.discr.C.dot(u0) + self.discr.dt ** 2 /
                (self.track.rail.mr * self.discr.dx) * f_vec)


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

        nx = self.discr.nx
        self.excit.roughness = list(np.fft.ifft(np.fft.fft(np.random.randn(nx))/np.maximum(1,np.arange(nx))).real * 2e-6)

        for i in range(len(self.excitation_indices)):
            # Store initial deflection at contact points (should be zero at t=0)
            self.contact_point_deflection[i].append(defl[self.excitation_indices[i],0])  # initial deflection at t=0

        # loop for calculating deflection at each time step
        # NOTE: starts from t=1 because we need defl at t-1 and t-2 for the Crank-Nicolson scheme
        for t in range(1, self.discr.nt):
            if t == 5000:
                a = "checkpoint"  # TODO: remove hardcoded checkpoint for debugging
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
        if t%100 == 0 and t > 4545:
            debug = True
        b = self.calc_rightside_crank_nicolson(
            defl = defl,
            u1 = defl[:, t-1],
            u0 = defl[:, t-2],
            excitation_pos = excitation_pos,
            t = t
        )
        # Calculate deflection for time step t
        u = self.factoriz.solve(b)
        defl[:, t] = u[0:2 * self.discr.nx]

        if t == 4544:   # TODO: this is crazy hardcoded for debugging, needs to be fixed ASAP
            pos = excitation_pos[0]
            self.y_static = self.interpolate(pos, defl[:, t])  # Store deflection after ramp for Hertzian contact calculation




        return