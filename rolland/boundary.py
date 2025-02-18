"""Defines boundary classes for FDM simulation.

.. autosummary::
    :toctree: boundary

    PMLStampka
"""

from numpy import linspace
from traitlets import HasTraits, Instance

from rolland import Track
from rolland.grid import GridFDMStampka


class PMLStampka(HasTraits):
    r"""Calculate the boundary domain properties according to :cite:t:`stampka2022a`.

    A perfectly matched layer (PML) method is used which increases the rail damping
    coefficient in the boundary domain.

    Attributes
    ----------
    track : Track
        Track instance.
    grid : GridFDMStampka
        Grid instance.
    pml : numpy.ndarray
        Array containing the damping values in the boundary domain :math:`[-]`.
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
