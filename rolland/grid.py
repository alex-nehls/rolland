"""Grid classes."""
from traitlets import Float, HasTraits, Instance, Integer

from rolland import Track


class GridFDMStampka(HasTraits):
    """Calculate grid parameters for FDM simulation."""

    # Track instance
    track = Instance(Track)

    # Step size in time [s]
    dt = Float()

    # Requested beam length [m]
    req_l = Float()

    # Requested simulation time [s]
    req_simt = Float()

    # Coefficient for dx calculation (must be >= 1) [-]
    bx = Float()

    # Number of spatial steps in single sided boundary domain [-]
    n_bound = Integer()


    def __init__(self, *args, **kwargs):
        """Compute grid parameters."""
        super().__init__(*args, **kwargs)
        # Number of time steps [-]
        self.nt = int(self.req_simt / self.dt)

        # Actual simulation time [s]
        self.sim_t = self.nt * self.dt

        # Minimum step size in space [m]
        dx_min = self.bx * ((self.track.rail.E * self.track.rail.Iyr) /
                            (6 * self.track.rail.mr)) ** (1 / 4) * self.dt ** (1 / 2)

        # Updated spatial step size. Ensures that default sleeper spacing 0.6 m is a multiple of dx
        self.dx = 0.6 / (0.6 // dx_min)

        # Updated stability coefficient
        self.bx_upd = self.dx / (((self.track.rail.E * self.track.rail.Iyr) / (6 * self.track.rail.mr)) ** (1 / 4)
                       * self.dt ** (1 / 2))

        # Number of spatial steps [-]
        self.nx = int(self.req_l / self.dx + (2 * self.n_bound)) + 1

        # Actual beam length [m]
        self.l_domain = (self.nx - 1) * self.dx

        # Length of boundary area [m]
        self.l_bound = self.n_bound * self.dx
