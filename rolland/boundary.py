"""Boundary conditions for rolland model."""
from numpy import linspace
from traitlets import HasTraits, Instance

from rolland import Track
from rolland.grid import GridFDMStampka


class PMLStampka(HasTraits):
    """Increase rail damping coefficient in boundary domain.

    According to Stampka.
    """

    # Track instance
    track = Instance(Track)

    # Grid instance
    grid = Instance(GridFDMStampka)

    def __init__(self, *args, **kwargs):
        """Calculate boundary properties."""
        super().__init__(*args, **kwargs)
        # Boundary Coefficient
        r = (self.track.rail.E * self.track.rail.Iyr) / self.track.rail.mr *  self.grid.dt ** 2 / self.grid.dx ** 4

        # Rail damping coefficient in boundary domain
        drbc = r / 2 * self.track.rail.mr / self.grid.dt

        # Grid points in boundary domain
        xbc = linspace(0, self.grid.l_bound, int(self.grid.n_bound))

        # Function for increasing damping, added to dr
        self.pml = drbc * xbc ** 7 / (self.grid.dx * self.grid.n_bound) ** 7