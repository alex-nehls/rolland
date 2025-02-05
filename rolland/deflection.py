"""Calculates Deflection."""
from numpy import empty, zeros
from scipy.sparse.linalg import splu
from traitlets import Float, HasTraits, Instance

from rolland import Track
from rolland.discretization import Discretization
from rolland.excitation import Excitation
from rolland.grid import Grid


class Deflection(HasTraits):
    """Base class for deflection."""

    # Track instance
    track = Instance(Track)

    # Grid instance
    grid = Instance(Grid)

    # Excitation instance
    excit = Instance(Excitation)

    # Discretization instance
    discr = Instance(Discretization)


class DeflectionFDMStampka(Deflection):
    """Deflection according to Stampka."""

    # Excitation point
    x_excit = Float()


    def initialize_start_values(self):
        """Set starting values of deflections to zero."""
        defl = empty((2 * self.grid.nx, self.grid.nt + 1))

        # Set starting values to zero for two time steps
        defl[:, 0:2] = zeros((2 * self.grid.nx, 2))
        return defl

    def calc_rightside_crank_nicolson(self, u1, u0, ind_excit, t):
        """Calculate right hand side of equation as in Katja Stampkas Paper."""
        # Write excitation force for time step t into force array
        f = zeros(2 * self.grid.nx)
        f[ind_excit] = self.excit.force[t]

        return (self.discr.B.dot(u1) + self.discr.C.dot(u0) + self.grid.dt ** 2 /
                (self.track.rail.mr * self.grid.dx) * f)


    def calc_deflection(self, defl):
        """Calculate deflection."""
        # Index of excitation point
        self.ind_excit = int(self.x_excit / self.grid.dx)

        # Factorization of matrix A
        factoriz = splu(self.discr.A)

        for t in range(1, self.grid.nt):
            # Calculate right hand side of equation
            b = self.calc_rightside_crank_nicolson(u1=defl[:, t], u0=defl[:, t - 1], ind_excit = self.ind_excit, t=t)

            # Calculate deflection for time step t
            u = factoriz.solve(b)

            # Save deflection
            defl[:, t + 1] = u[0:2 * self.grid.nx]

        return defl


    def __init__(self, *args, **kwargs):
        """Compute force array."""
        super().__init__(*args, **kwargs)
        # Initialize starting values
        defl = self.initialize_start_values()
        # Calculate deflection
        self.deflection = self.calc_deflection(defl)

