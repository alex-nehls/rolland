"""Discretization of Differential Equation."""
import warnings

from numpy import ones, zeros
from scipy.sparse import SparseEfficiencyWarning, csc_matrix, diags, eye
from traitlets import HasTraits, Instance

from rolland.boundary import PMLStampka
from rolland.grid import Grid
from rolland.track import (
    ArrangedBallastedSingleRailTrack,
    ArrangedSlabSingleRailTrack,
    ContBallastedSingleRailTrack,
    ContSlabSingleRailTrack,
    SimplePeriodicBallastedSingleRailTrack,
    SimplePeriodicSlabSingleRailTrack,
    SingleRailTrack,
)


class Discretization(HasTraits):
    """Base class for discretization."""

    # Grid instance
    grid = Instance(Grid)


class DiscretizationFDMStampka(Discretization):
    """Finite Difference Method (FDM) discretization for Stampka's model."""

    # Track instance
    track = Instance(SingleRailTrack)

    # Boundary instance
    bound = Instance(PMLStampka)

    def build_matrix(self, vec_dr, vec_sp, vec_dp, vec_ms, vec_sb, vec_db):
        """Build matrices A,B and C according to Stampka."""
        #   Suppressing warning
        warnings.simplefilter("ignore", category=SparseEfficiencyWarning)

        # simplification factor
        r = (self.track.rail.E * self.track.rail.Iyr) * self.grid.dt ** 2 / (2 * self.track.rail.mr * self.grid.dx ** 4)

        # Coefficient matrix for x'''' (4th derivative)
        D_diagonals = [ones(self.grid.nx - 2),  # noqa: N806
                       (-4) * ones(self.grid.nx - 1),
                       6 * ones(self.grid.nx),
                       (-4) * ones(self.grid.nx - 1),
                       ones(self.grid.nx - 2)]

        D = diags(D_diagonals, [-2, -1, 0, 1, 2])  # noqa: N806
        Eye = eye(self.grid.nx)  # noqa: N806

        A11_1_diagonals = self.grid.dt / self.track.rail.mr * (vec_dr + vec_dp)  # noqa: N806
        A11_1_diagonals += self.grid.dt ** 2 / (2 * self.track.rail.mr) * vec_sp  # noqa: N806
        A11_1 = diags([A11_1_diagonals], [0])  # noqa: N806
        A11 = (r * D + Eye + A11_1).tocsc()  # noqa: N806

        B11_1_diagonals = self.grid.dt / self.track.rail.mr * (vec_dr + vec_dp)  # noqa: N806
        B11_1 = diags([B11_1_diagonals], [0])  # noqa: N806
        B11 = (2 * Eye + B11_1).tocsc()  # noqa: N806

        C11_1_diagonals = self.grid.dt ** 2 / (2 * self.track.rail.mr) * vec_sp  # noqa: N806
        C11_1 = diags([C11_1_diagonals], [0])  # noqa: N806
        C11 = (-(Eye + C11_1 + r * D)).tocsc()  # noqa: N806

        A12_diagonals = -self.grid.dt / self.track.rail.mr * vec_dp  # noqa: N806
        A12_diagonals += -self.grid.dt ** 2 / (2 * self.track.rail.mr) * vec_sp  # noqa: N806
        A12 = diags([A12_diagonals], [0]).tocsc()  # noqa: N806

        A21_diagonals = -self.grid.dt * vec_dp / vec_ms  # noqa: N806
        A21_diagonals += -self.grid.dt ** 2 / (2 * vec_ms) * vec_sp  # noqa: N806
        A21 = diags([A21_diagonals], [0]).tocsc()  # noqa: N806

        A22_1_diagonals = self.grid.dt * ((vec_dp + vec_db) / vec_ms)  # noqa: N806
        A22_1_diagonals += self.grid.dt ** 2 / (2 * vec_ms) * (vec_sp + vec_sb)  # noqa: N806
        A22_1 = diags([A22_1_diagonals], [0])  # noqa: N806
        A22 = (Eye + A22_1).tocsc()  # noqa: N806

        B12_diagonals = -self.grid.dt / self.track.rail.mr * vec_dp  # noqa: N806
        B12 = diags([B12_diagonals], [0]).tocsc()  # noqa: N806

        B21_diagonals = -self.grid.dt * vec_dp / vec_ms  # noqa: N806
        B21 = diags([B21_diagonals], [0]).tocsc()  # noqa: N806

        B22_1_diagonals = self.grid.dt * (vec_db + vec_dp) / vec_ms  # noqa: N806
        B22_1 = diags([B22_1_diagonals], [0])  # noqa: N806
        B22 = (2 * Eye + B22_1).tocsc()  # noqa: N806

        C12_diagonals = self.grid.dt ** 2 / (2 * self.track.rail.mr) * vec_sp  # noqa: N806
        C12 = diags([C12_diagonals], [0]).tocsc()  # noqa: N806

        C21_diagonals = self.grid.dt ** 2 / (2 * vec_ms) * vec_sp  # noqa: N806
        C21 = diags([C21_diagonals], [0]).tocsc()  # noqa: N806

        C22_1_diagonals = self.grid.dt ** 2 * (vec_sp + vec_sb) / (2 * vec_ms)  # noqa: N806
        C22_1 = diags([C22_1_diagonals], [0])  # noqa: N806
        C22 = (-(Eye + C22_1)).tocsc()  # noqa: N806

        self.A = csc_matrix((2 * self.grid.nx, 2 * self.grid.nx))  # noqa: N806
        self.A[0:self.grid.nx, 0:self.grid.nx] = A11
        self.A[0:self.grid.nx, self.grid.nx:2 * self.grid.nx] = A12
        self.A[self.grid.nx:2 * self.grid.nx, 0:self.grid.nx] = A21
        self.A[self.grid.nx:2 * self.grid.nx, self.grid.nx:2 * self.grid.nx] = A22

        self.B = csc_matrix((2 * self.grid.nx, 2 * self.grid.nx))  # noqa: N806
        self.B[0:self.grid.nx, 0:self.grid.nx] = B11
        self.B[0:self.grid.nx, self.grid.nx:2 * self.grid.nx] = B12
        self.B[self.grid.nx:2 * self.grid.nx, 0:self.grid.nx] = B21
        self.B[self.grid.nx:2 * self.grid.nx, self.grid.nx:2 * self.grid.nx] = B22

        self.C = csc_matrix((2 * self.grid.nx, 2 * self.grid.nx))  # noqa: N806
        self.C[0:self.grid.nx, 0:self.grid.nx] = C11
        self.C[0:self.grid.nx, self.grid.nx:2 * self.grid.nx] = C12
        self.C[self.grid.nx:2 * self.grid.nx, 0:self.grid.nx] = C21
        self.C[self.grid.nx:2 * self.grid.nx, self.grid.nx:2 * self.grid.nx] = C22

class DiscretizationFDMStampkaLinear(DiscretizationFDMStampka):
    """Finite Difference Method (FDM) discretization for Stampka's model with linear parameters.

    The superstructure design defined remains constant during the simulation.
    """

    def __init__(self, *args, **kwargs):
        """Calculate superstructure property vectors."""
        super().__init__(*args, **kwargs)
        self.initialize_vectors()
        self.add_boundary_conditions()
        self.handle_track_specific_logic()

        self.build_matrix(self.vec_dr, self.vec_sp, self.vec_dp, self.vec_ms, self.vec_sb, self.vec_db)

    def initialize_vectors(self):
        """Initialize the vectors."""
        self.vec_dr = self.track.rail.dr * ones(self.grid.nx)
        self.vec_sp = zeros(self.grid.nx)
        self.vec_dp = zeros(self.grid.nx)
        self.vec_ms = ones(self.grid.nx)
        self.vec_sb = zeros(self.grid.nx)
        self.vec_db = zeros(self.grid.nx)

    def add_boundary_conditions(self):
        """Add boundary conditions."""
        self.vec_dr[:self.bound.pml.size] += self.bound.pml[::-1]
        self.vec_dr[-self.bound.pml.size:] += self.bound.pml

    def handle_track_specific_logic(self):
        """Handle track-specific logic."""
        if isinstance(self.track, ContSlabSingleRailTrack):
            self.vec_sp += self.track.pad.sp[0]
            self.vec_dp += self.track.pad.dp[0]
            self.vec_ms += self.track.slab.ms

        elif isinstance(self.track, SimplePeriodicSlabSingleRailTrack | ArrangedSlabSingleRailTrack):
            self.handle_periodic_slab_track()

        elif isinstance(self.track, ContBallastedSingleRailTrack):
            self.vec_sp += self.track.pad.sp[0]
            self.vec_dp += self.track.pad.dp[0]
            self.vec_ms += self.track.slab.ms
            self.vec_sb += self.track.ballast.sb[0]
            self.vec_db += self.track.ballast.db[0]

        elif isinstance(self.track, SimplePeriodicBallastedSingleRailTrack | ArrangedBallastedSingleRailTrack):
            self.handle_periodic_ballasted_track()

        else:
            msg = "Track type not recognized!"
            raise ValueError(msg)

    def handle_periodic_slab_track(self):
        """Handle periodic slab track."""
        mount_pos = list(self.track.mount_prop.keys())
        for i in mount_pos:
            self.vec_sp[int(i / self.grid.dx)] = self.track.mount_prop[i][0].sp[0]
            self.vec_dp[int(i / self.grid.dx)] = self.track.mount_prop[i][0].dp[0]
        self.vec_ms += self.track.slab.ms

    def handle_periodic_ballasted_track(self):
        """Handle periodic ballasted track."""
        mount_pos = list(self.track.mount_prop.keys())
        for i in mount_pos:
            self.vec_sp[int(i / self.grid.dx)] = self.track.mount_prop[i][0].sp[0]
            self.vec_dp[int(i / self.grid.dx)] = self.track.mount_prop[i][0].dp[0]
            self.vec_ms[int(i / self.grid.dx)] = self.track.mount_prop[i][1].ms
        self.vec_sb += self.track.ballast.sb[0]
        self.vec_db += self.track.ballast.db[0]


