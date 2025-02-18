"""Defines deflection classes for FDM simulation.

.. autosummary::
    :toctree: deflection

    Deflection
    DeflectionFDMStampka
"""
from numpy import empty, zeros
from scipy.sparse.linalg import splu
from traitlets import Float, HasTraits, Instance

from rolland import Track
from rolland.discretization import Discretization
from rolland.excitation import Excitation
from rolland.grid import Grid


class Deflection(HasTraits):
    r"""Base class for grid classes.

    Attributes
    ----------
    track : Track
        Track instance.
    grid : Grid
        Grid instance.
    excit : Excitation
        Excitation instance.
    discr : Discretization
        Discretization instance.
    """

    track = Instance(Track)
    grid = Instance(Grid)
    excit = Instance(Excitation)
    discr = Instance(Discretization)


class DeflectionFDMStampka(Deflection):
    r"""Calculate deflection according to :cite:t:`stampka2022a`.

    Attributes
    ----------
    track : Track
        Track instance.
    grid : Grid
        Grid instance.
    excit : Excitation
        Excitation instance.
    discr : Discretization
        Discretization instance.
    x_excit : float
        Excitation point :math:`[m]`.
    deflection : numpy.ndarray
        Deflection array :math:`[m]`.
    ind_excit : int
        Index of excitation point :math:`[-]`.
    """

    # Excitation point
    x_excit = Float()


    def initialize_start_values(self):
        """Set starting values of deflections to zero.

        Returns
        -------
        defl : numpy.ndarray
            Array of deflections initialized to zero with shape (2 * nx, nt + 1).
        """
        defl = empty((2 * self.grid.nx, self.grid.nt + 1))

        # Set starting values to zero for two time steps
        defl[:, 0:2] = zeros((2 * self.grid.nx, 2))
        return defl


    def calc_rightside_crank_nicolson(self, u1, u0, ind_excit, t):
        """Calculate the right-hand side of the equation according to :cite:t:`stampka2022a`.

        Parameters
        ----------
        u1 : numpy.ndarray
            Deflection array at the current time step.
        u0 : numpy.ndarray
            Deflection array at the previous time step.
        ind_excit : int
            Index of the excitation point.
        t : int
            Current time step.

        Returns
        -------
        numpy.ndarray
            Right-hand side of the equation.
        """
        # Write excitation force for time step t into force array
        f = zeros(2 * self.grid.nx)
        f[ind_excit] = self.excit.force[t]

        return (self.discr.B.dot(u1) + self.discr.C.dot(u0) + self.grid.dt ** 2 /
                (self.track.rail.mr * self.grid.dx) * f)


    def calc_deflection(self, defl):
        """
        Calculate deflection.

        Parameters
        ----------
        defl : numpy.ndarray
            Array of deflections initialized to zero with shape (2 * nx, nt + 1).

        Returns
        -------
        defl : numpy.ndarray
            Array of calculated deflections with shape (2 * nx, nt + 1).
        """
        # Index of excitation point
        self.ind_excit = int(self.x_excit / self.grid.dx)

        # Factorization of matrix A (LU decomposition)
        factoriz = splu(self.discr.A)

        for t in range(1, self.grid.nt):
            # Calculate right hand side of equation
            b = self.calc_rightside_crank_nicolson(u1=defl[:, t], u0=defl[:, t - 1], ind_excit=self.ind_excit, t=t)

            # Calculate deflection for time step t
            u = factoriz.solve(b)

            defl[:, t + 1] = u[0:2 * self.grid.nx]
        return defl


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
        defl = self.initialize_start_values()
        # Calculate deflection
        self.deflection = self.calc_deflection(defl)

