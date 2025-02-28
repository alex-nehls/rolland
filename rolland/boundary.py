"""Defines boundary classes for FDM simulation.

.. autosummary::
    :toctree: boundary

    PMLStampka
"""

from grid import GridFDMStampka
from numpy import linspace
from traitlets import HasTraits, Instance


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

    # Grid instance
    grid = Instance(GridFDMStampka)

    def __init__(self, *args, **kwargs):
        """Calculate boundary properties."""
        super().__init__(*args, **kwargs)
        # Boundary Coefficient

        youm = self.grid.track.rail.E
        shearm = self.grid.track.rail.Iyr
        mr = self.grid.track.rail.mr
        dt = self.grid.dt
        dx = self.grid.dx
        n_bound = self.grid.n_bound
        l_bound = self.grid.l_bound
        # Rail stiffness

        r = (youm * shearm) / mr *  dt ** 2 / dx ** 4

        # Rail damping coefficient in boundary domain
        drbc = r / 2 * mr / dt

        # Grid points in boundary domain
        xbc = linspace(0, l_bound, int(n_bound))

        # Function for increasing damping, added to dr
        self.pml = drbc * xbc ** 7 / (dx * n_bound) ** 7
