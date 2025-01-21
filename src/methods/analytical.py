from numpy import exp, pi, sqrt, zeros, zeros_like
from traitlets import HasTraits, Instance
from traittypes import Array

from src.track import ContBallastedSingleRailTrack, ContSlabSingleRailTrack


class AnalyticalMethods(HasTraits):
    """Base class for analytical methods."""

    # Excitation frequencies [Hz]
    f = Array()

    # Force amplitude corresponding to the excitation frequencies f [N]
    F = Array()

    # Distances to the excitation point [m]
    x = Array()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize_attributes()
        self.compute_mobility()
        self.compute_vibration()

    def initialize_attributes(self):
        """Initialize computed attributes."""
        self.omega = 2 * pi * self.f
        self.Yb = zeros((len(self.x), len(self.f)), dtype=complex)
        self.vb = zeros_like(self.Yb)
        self.ub = zeros_like(self.Yb)

    def compute_mobility(self):
        """Compute the mobility of the track."""
        message = "Subclasses must implement compute_mobility."
        raise NotImplementedError(message)

    def compute_vibration(self):
        """Calculate the frequency response of the track."""
        self.vb = self.Yb * self.F
        self.ub = self.vb / (self.omega * 1j)


class ThompsonEBBCont1LSupp(AnalyticalMethods):
    """Analytical solution for a continuous slab single rail track with a 1-layer support.

    According to chapter 3.2 (Thompson, D., 2024. Railway Noise and Vibration
    (Second Edition). Elsevier).
    """

    # Track instance
    track = Instance(ContSlabSingleRailTrack)

    def compute_mobility(self):
        """Compute the mobility of the track."""
        mr = self.track.rail.mr
        sp = self.track.pad.sp[0]
        dp = self.track.pad.dp[0]

        # Resonance frequency rail <--> foundation [Hz]
        self.omega_0 = sqrt(sp / mr)

        # Wave number
        k_p = ((self.omega ** 2 * mr - sp - 1j * self.omega * dp) /
               (self.track.rail.E * self.track.rail.Iyr)) ** (1/4)

        # Compute mobility using vectorized operations
        abs_x = abs(self.x[:, None])  # Broadcast x over omega
        term1 = exp(-1j * k_p * abs_x)
        term2 = -1j * exp(-k_p * abs_x)
        self.Yb = (self.omega / (4 * (self.track.rail.E * self.track.rail.Iyr) * k_p ** 3)
                   * (term1 + term2))
        return self.Yb, self.omega_0


class ThompsonEBBCont2LSupp(AnalyticalMethods):
    """Analytical solution for a continuous ballasted single rail track with a 2-layer support.

    According to chapter 3.3 (Thompson, D., 2024. Railway Noise and Vibration (Second Edition).
    Elsevier).
    """

    # Track instance
    track = Instance(ContBallastedSingleRailTrack)

    def compute_mobility(self):
        """Compute the mobility of the track."""
        mr = self.track.rail.mr
        sp = self.track.pad.sp[0]
        sb = self.track.ballast.sb[0]
        dp = self.track.pad.dp[0]
        db = self.track.ballast.db[0]
        ms = self.track.slab.ms

        # Resonance frequencies
        self.omega_0 = sqrt(sp / mr)
        self.omega_1 = sqrt(sb / ms)
        self.omega_2 = sqrt((sp + sb) / ms)

        # Dynamic stiffness
        sp_tot = sp + 1j * self.omega * dp
        sb_tot = sb + 1j * self.omega * db
        s_tot = (sp_tot * (sb_tot - ms * self.omega ** 2)) / (sp_tot + sb_tot - ms * self.omega ** 2)

        k_p = ((self.omega ** 2 * mr - s_tot - 1j * self.omega * dp) /
                (self.track.rail.E * self.track.rail.Iyr)) ** (1/4)

        # Compute mobility using vectorized operations
        abs_x = abs(self.x[:, None])  # Broadcast x over omega
        term1 = exp(-1j * k_p * abs_x)
        term2 = -1j * exp(-k_p * abs_x)
        self.Yb = (self.omega / (4 * (self.track.rail.E * self.track.rail.Iyr) * k_p ** 3)
                   * (term1 + term2))
        return self.Yb, self.omega_0, self.omega_1, self.omega_2

