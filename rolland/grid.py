"""Defines grid classes for FDM simulation.

.. autosummary::
    :toctree: grid

    Grid
    GridFDMStampka
"""

import abc

from traitlets import Float, Instance, Integer

from .abstract_traits import ABCHasTraits
from .track import Track


class Grid(ABCHasTraits):
    r"""Abstract base class for grid classes.

    Attributes
    ----------
    track : Track
        Track instance.
    """

    # Track instance
    track = Instance(Track)

    @abc.abstractmethod
    def validate_grid(self):
        """Validate grid parameters."""

class GridFDMStampka(Grid):
    r"""Calculate grid parameters for FDM simulation according to :cite:t:`stampka2022a`.

    The spatial step size :math:`\Delta x` is adjusted to ensure that the default sleeper spacing
    of :math:`0.6 \, \text{m}` is a multiple of :math:`\Delta x`. Since a sleeper spacing of
    :math:`0.6 \, \text{m}` commonly used in practice, this ensures that the grid is aligned with
    the sleeper positions.

    Attributes
    ----------
    track : Track
        Track instance.
    dt : float
        Step size in time :math:`[s]`.
    req_simt : float
        Requested simulation time :math:`[s]`.
    bx : float
        Stability coefficient for dx calculation (must be :math:`b_x \geq 1`) :math:`[-]`.
    n_bound : int
        Number of spatial steps in single sided boundary domain :math:`[-]`.
    nt : int
        Number of time steps :math:`[-]`.
    sim_t : float
        Actual simulation time :math:`[s]`.
    dx : float
        Step size in space :math:`[m]`.
    bx_upd : float
        Updated stability coefficient :math:`[-]`.
    nx : int
        Number of spatial steps :math:`[-]`.
    l_domain : float
        Actual track length (calculation + boundary domain) :math:`[m]`.
    l_bound : float
        Length of boundary area :math:`[m]`.
    """

    dt = Float()
    req_simt = Float()
    bx = Float()
    n_bound = Integer()

    def validate_grid(self):
        """Validate grid parameters."""

    def __init__(self, *args, **kwargs):
        """Compute grid parameters."""
        super().__init__(*args, **kwargs)
        self.nt = int(self.req_simt / self.dt)
        self.sim_t = self.nt * self.dt
        dx_min = self.bx * ((self.track.rail.E * self.track.rail.Iyr) /
                            (6 * self.track.rail.mr)) ** (1 / 4) * self.dt ** (1 / 2)
        self.dx = 0.6 / (0.6 // dx_min)

        self.bx_upd = self.dx / (((self.track.rail.E * self.track.rail.Iyr) / (6 * self.track.rail.mr)) ** (1 / 4)
                       * self.dt ** (1 / 2))
        self.nx = int(self.track.l_track / self.dx) + 1

        self.l_domain = (self.nx - 1) * self.dx
        self.l_bound = self.n_bound * self.dx
