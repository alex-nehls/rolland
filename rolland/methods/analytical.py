from numpy import abs, array, exp, eye, lib, linalg, newaxis, pi, real, sqrt, zeros, zeros_like
from traitlets import Float, HasTraits, Instance
from traittypes import Array

from rolland.track import (
    ContBallastedSingleRailTrack,
    ContSlabSingleRailTrack,
    DiscrBallastedSingleRailTrack,
    DiscrSlabSingleRailTrack,
)


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
        self.omega_0 = sqrt(sp / mr)            # Resonance frequency rail <--> pads [Hz]
        self.omega_1 = sqrt(sb / ms)            # Resonance frequency ballast <--> slab [Hz]
        self.omega_2 = sqrt((sp + sb) / ms)     # Resonance frequency rail <--> slab [Hz]

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

class ThompsonTBDiscr(AnalyticalMethods):
    """Analytical solution for a discrete single rail track.

    According to:
    Thompson - RAILWAY NOISE AND VIBRATION - CHAPTER 3.5.1 TRACK VIBRATION (PERIODICALLY SUPPORTED TRACK.)
    """

    # Coordinate of excitation point [m]
    x_excit = Float()

    # Greens function of free Timoshenko Beam (eq. 3.69)
    def calc_greens_func(self, xm, xn, k_p, k_d, f_p, f_d):
        """Calculate Green's function for any two points xm and xn."""
        dist = abs(xm - xn)
        term1 = exp(-1j * k_p * dist)
        term2 = exp(-k_d * dist)
        term3 = 1  # term3 = exp(1j * self.omega * t) usually dropped (acc. to Heckl)
        return f_p * term1 + (f_d * term2) * term3

    def compute_mobility_common(self, track, ms, sb, etab):
        """Common mobility computation for 1-layer and 2-layer support."""
        mr = track.rail.mr
        rho = track.rail.rho
        etar = track.rail.etar
        etap = track.pad.etap
        kap = track.rail.kap
        youm = track.rail.E * (1 + (1j * etar))
        shearm = track.rail.G * (1 + (1j * etar))
        ar = track.rail.Ar
        aream = track.rail.Iyr
        bend_stiff = youm * aream
        sp = track.pad.sp[0]
        sb = sb

        # Positions of point forces [m]
        x_n = array(list(track.mount_prop.keys()))

        # Resonance frequencies
        self.f_0 = real(sqrt(sp / mr)) / (2 * pi)       # Resonance frequency rail <--> pads [Hz]
        self.f_1 = real(sqrt(sb / ms)) / (2 * pi)       # Resonance frequency ballast <--> sleepers [Hz]
        self.f_2 = real(sqrt(sp + sb)) / (2 * pi)       # Resonance frequency rail <--> sleepers [Hz]

        # Dynamic stiffness (eq. 3.68)
        impend = (sp * (1 + (1j * etap)) * ((sb * (1 + (1j * etab))) - (ms * (self.omega ** 2)))) / (
                    (sp * (1 + (1j * etap))) + (sb * (1 + (1j * etab))) - (ms * (self.omega ** 2)))

        k__p = (self.omega ** 2 / 2) * ((rho / youm) + (rho / shearm * kap) + lib.scimath.sqrt(
            ((rho / youm) - (rho / shearm * kap)) ** 2 + (4 * rho * ar) / (youm * aream * self.omega ** 2)))

        k__d = -(self.omega ** 2 / 2) * ((rho / youm) + (rho / shearm * kap) - lib.scimath.sqrt(
            ((rho / youm) - (rho / shearm * kap)) ** 2 + (4 * rho * ar) / (youm * aream * self.omega ** 2)))

        # Free bending wave (e.q. 3.71)
        k_p = lib.scimath.sqrt(k__p)

        # Bending wave near field (e.q. 3.71)
        k_d = lib.scimath.sqrt(k__d)

        # Amplitude of propagating bending wave (eq. 3.70)
        f_p = (1j / (youm * aream * shearm * kap)) * (((rho * aream * self.omega ** 2) - (shearm * kap * ar)
                                                 - (youm * aream * k__p)) / (2 * ar * k_p * (k__p + k__d)))

        # Peak value of bending wave near-field (eq. 3.70)
        f_d = (1 / (youm * aream * shearm * kap)) * (((rho * aream * self.omega ** 2) - (shearm * kap * ar)
                                                + (youm * aream * k__d)) / (2 * ar * k_d * (k__p + k__d)))

        # Displacements at reaction points
        uxn = zeros((self.f.size, x_n.size), dtype=complex)

        # Displacements at requested points
        self.ux = zeros((self.x.size, self.f.size), dtype=complex)


        for f in range(self.f.size):

            # Greens function matrix reaction points <--> reaction points
            greensm_mn = self.calc_greens_func(x_n[:, newaxis], x_n[newaxis, :], k_p[f], k_d[f], f_p[f], f_d[f])

            # Greens function matrix reaction points <--> excitation point
            greensm_exc = self.calc_greens_func(x_n, self.x_excit, k_p[f], k_d[f], f_p[f], f_d[f])

            # m = I + impend * greensm_mn
            m = eye(x_n.size) + impend[f] * greensm_mn

            # Calculate displacements at reaction points (eq. 3.76)
            uxn[f, :] = linalg.solve(m, greensm_exc)

            for p in range(self.x.size):

                # Greens function matrix requested points <--> reaction points
                greensm_xn = self.calc_greens_func(self.x[p], x_n, k_p[f], k_d[f], f_p[f], f_d[f])


                # Greens function matrix requested points <--> excitation point
                greensm_xf = self.calc_greens_func(self.x[p], self.x_excit, k_p[f], k_d[f], f_p[f], f_d[f])
                self.ux[p, f] = - impend[f] * greensm_xn.dot(uxn[f, :]) + greensm_xf

        self.Yb = (self.ux * self.omega * 1j) / self.F


class ThompsonTSDiscr1LSupp(ThompsonTBDiscr):
    """Solution for a discrete single rail track consisting of 1-layer support.

    Slab can be considered as rigid.
    """

    # Track instance
    track = Instance(DiscrSlabSingleRailTrack)

    def compute_mobility(self):
        """Compute the mobility of the track."""
        self.compute_mobility_common(self.track, self.track.slab.ms, 1e20, 0)


class ThompsonTSDiscr2LSupp(ThompsonTBDiscr):
    """Solution for a discrete single rail track consisting of 2-layer support."""

    # Track instance
    track = Instance(DiscrBallastedSingleRailTrack)

    def compute_mobility(self):
        """Compute the mobility of the track."""
        self.compute_mobility_common(self.track, self.track.sleeper.ms,
                                     self.track.ballast.sb[0], self.track.ballast.etab)


class HecklTBDiscr(AnalyticalMethods):
    """Analytical solution for a discrete single rail track.

    According to Heckl, M.A., 1995. Railway noise–Can random sleeper spacings help?.
    Acta Acustica United with Acustica, 81(6), pp.559-564.
    """

    # Coordinate of excitation point [m]
    x_excit = Float()

    def calc_greens_func(self, xm, xn, k_p, k_d, f_p, f_d):
        """Calculate Green's function for any two points xm and xn."""
        dist = abs(xm - xn)
        term1 = exp(-1j * k_p * dist)
        term2 = exp(-k_d * dist)
        term3 = 1  # term3 = exp(1j * self.omega * t) usually dropped (acc. to Heckl)
        return f_p * term1 + (f_d * term2) * term3

    def compute_mobility_common(self, track, ms, sb, etab):
        """Common mobility computation for 1-layer and 2-layer support."""
        mr = track.rail.mr
        rho = track.rail.rho
        etar = track.rail.etar
        etap = track.pad.etap
        youm = track.rail.E
        shearm = track.rail.G
        aream = track.rail.Iyr
        bend_stiff = youm * aream
        sp = track.pad.sp[0] * (1 + (etap * 1j))
        sb = sb * (1 + (etab * 1j))

        # Positions of point forces [m]
        x_n = array(list(track.mount_prop.keys()))

        # Resonance frequencies
        self.f_0 = real(sqrt(sp / mr)) / (2 * pi)       # Resonance frequency rail <--> pads [Hz]
        self.f_1 = real(sqrt(sb / ms)) / (2 * pi)       # Resonance frequency ballast <--> sleepers [Hz]
        self.f_2 = real(sqrt(sp + sb)) / (2 * pi)       # Resonance frequency rail <--> sleepers [Hz]

        # Dynamic stiffness (eq. 6)
        impend = (ms * self.omega ** 2 * sp - sp * sb) / (ms * self.omega ** 2 - (sp + sb))

        # Wave numbers (eq. 2a)
        k_c = self.omega * lib.scimath.sqrt(rho / youm)
        k_t = self.omega * lib.scimath.sqrt(rho / shearm)

        # Free bending wave (eq. 2a)
        k_p = lib.scimath.sqrt(1/2 * (k_c ** 2 + k_t ** 2 +
                                      lib.scimath.sqrt((k_c ** 2 + k_t ** 2) ** 2 - 4 *
                                                       (k_c**2 * k_t**2 - (k_c**2 * mr * youm) / (bend_stiff * rho)))))

        # Bending wave near field (eq. 2b)
        k_d = lib.scimath.sqrt(1/2 * (k_c ** 2 + k_t ** 2 -
                                      lib.scimath.sqrt((k_c ** 2 + k_t ** 2) ** 2 - 4 *
                                                       (k_c**2 * k_t**2 - (k_c**2 * mr * youm) / (bend_stiff * rho)))))

        # Amplitude of propagating bending wave (eq. 3a)
        f_p = (1j * ((rho ** 2 * bend_stiff / (youm * mr)) * self.omega ** 2 - shearm -
                     (bend_stiff * rho * k_p ** 2) / mr) / (bend_stiff * shearm * 2 * k_p * (k_p ** 2 + k_d ** 2)))

        # Peak value of bending wave near-field (eq. 3b)
        f_d = (1j * ((rho ** 2 * bend_stiff / (youm * mr)) * self.omega ** 2 - shearm +
                     (bend_stiff * rho * k_d ** 2) / mr) / (bend_stiff * shearm * 2 * k_d * (k_p ** 2 + k_d ** 2)))

        # Displacements at reaction points
        uxn = zeros((self.f.size, x_n.size), dtype=complex)

        # Displacements at requested points
        self.ux = zeros((self.x.size, self.f.size), dtype=complex)


        for f in range(self.f.size):

            # Greens function matrix reaction points <--> reaction points
            greensm_mn = self.calc_greens_func(x_n[:, newaxis], x_n[newaxis, :], k_p[f], k_d[f], f_p[f], f_d[f])

            # Greens function matrix reaction points <--> excitation point
            greensm_exc = self.calc_greens_func(x_n, self.x_excit, k_p[f], k_d[f], f_p[f], f_d[f])

            # m = I + impend * greensm_mn
            m = eye(x_n.size) + impend[f] * greensm_mn

            # u(x_n) = greensm_exc - (I + impend * greensm_mn)
            uxn[f, :] = linalg.solve(m, greensm_exc)

            for p in range(self.x.size):

                # Greens function matrix requested points <--> reaction points
                greensm_xn = self.calc_greens_func(self.x[p], x_n, k_p[f], k_d[f], f_p[f], f_d[f])

                # Greens function matrix requested points <--> excitation point
                greensm_xf = self.calc_greens_func(self.x[p], self.x_excit, k_p[f], k_d[f], f_p[f], f_d[f])
                self.ux[p, f] = - impend[f] * greensm_xn.dot(uxn[f, :]) + greensm_xf

        self.Yb = (self.ux * self.omega * 1j) / self.F


class HecklTBDiscr1LSupp(HecklTBDiscr):
    """Solution for a discrete single rail track consisting of 1-layer support.

    Slab can be considered as rigid.
    """

    # Track instance
    track = Instance(DiscrSlabSingleRailTrack)

    def compute_mobility(self):
        """Compute the mobility of the track."""
        self.compute_mobility_common(self.track, self.track.slab.ms, 1e20, 0)


class HecklTBDiscr2LSupp(HecklTBDiscr):
    """Solution for a discrete single rail track consisting of 2-layer support."""

    # Track instance
    track = Instance(DiscrBallastedSingleRailTrack)

    def compute_mobility(self):
        """Compute the mobility of the track."""
        self.compute_mobility_common(self.track, self.track.sleeper.ms,
                                     self.track.ballast.sb[0], self.track.ballast.etab)
