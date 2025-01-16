"""Defines track structure."""

from scipy.stats import truncnorm
from traitlets import HasTraits, Instance, Integer

from src.components import Ballast, ContPad, DiscrPad, Rail, Sleeper
from src.track_layout import LayoutConst, LayoutPeriod, LayoutStoch, TrackLayout


class Track(HasTraits):
    """Base class for track structure."""

    # Ballast instance
    ballast = Instance(Ballast)

    def __init__(self, ballast):
        self.ballast = ballast


class SingleRailTrack(Track):
    """Single rail track class."""

    # Rail instance
    rail = Instance(Rail)

    def __init__(self, rail, ballast):
        super().__init__(ballast)
        self.rail = rail


class SlabbedSingleRailTrack(SingleRailTrack):
    """Slabbed single rail track class."""

    # Sleeper instance
    sleeper = Sleeper()

    def __init__(self, rail, ballast):

        # Set sleeper properties to infinity to avoid sleeper discplacement
        super().__init__(rail, ballast)
        self.sleeper = Sleeper()
        self.sleeper.ms = 1e20
        self.sleeper.Bs = 1e20
        self.sleeper.ls = 1e20
        self.sleeper.wdths = 1e20


class ContSlabbedSingleRailTrack(SlabbedSingleRailTrack):
    """Slabbed single rail track class with continuous mounting."""

    # Pad instance
    pad = Instance(ContPad)

    def __init__(self, rail, ballast, pad):
        super().__init__(rail, ballast)
        self.pad = pad


class DiscrSlappedSingleRailTrack(SlabbedSingleRailTrack):
    """Slabbed single rail track class with discrete mounting points."""

    # Number of mounting positions
    num_mount_pos = Integer(min=1)

    # Track layout instance (includes sleeper mass, sleeper distance, and pad stiffness layout)
    track_layout = Instance(TrackLayout)

    def calc_mount_pos(self):
        """Calculate mounting positions based on layout."""
        # Mounting positions are equally spaced
        if isinstance(self.track_layout.lay_slep_dist, LayoutConst):
            self.mount_pos = [self.track_layout.lay_slep_dist.value * i for i in range(self.num_mount_pos)]

        # Mounting positions with periodic layout
        elif isinstance(self.track_layout.lay_slep_dist, LayoutPeriod):
            period = self.track_layout.lay_slep_dist.period
            self.mount_pos = [round(sum(period[:i % len(period)]) + (i // len(period)) * sum(period), 10) for i in
                              range(self.num_mount_pos)]

        # Mounting positions with stochastic layout
        elif isinstance(self.track_layout.lay_slep_dist, LayoutStoch):

            mean = self.track_layout.lay_slep_dist.mean
            std = self.track_layout.lay_slep_dist.std
            lim_min = self.track_layout.lay_slep_dist.lim_min
            lim_max = self.track_layout.lay_slep_dist.lim_max

            # Generate mounting positions based on truncated normal distribution
            self.mount_pos = [0.0]
            while len(self.mount_pos) < self.num_mount_pos:
                value = truncnorm((lim_min - mean) / std, (lim_max - mean) / std, loc=mean, scale=std).rvs(1)[0]
                self.mount_pos.append(round(self.mount_pos[-1] + value, 5))


    def mount_properties(self, mount_pos):
        """Calculate mounting properties based on layout and generate
        dictionary with properties for each mounting position.
        """
        # Mounting properties dictionary
        self.mount_prop = {}

        # Pad stiffness with constant layout
        if isinstance(self.track_layout.lay_pad_stiff, LayoutConst):
            for pos in mount_pos:
                self.mount_prop[pos] = DiscrPad(sp=self.track_layout.lay_pad_stiff.value)

        # Pad stiffness with periodic layout
        elif isinstance(self.track_layout.lay_pad_stiff, LayoutPeriod):
            # Pad stiffness with periodic layout
            period = self.track_layout.lay_pad_stiff.period
            for i, pos in enumerate(mount_pos):
                self.mount_prop[pos] = DiscrPad(sp=period[i % len(period)])

        # Pad stiffness with stochastic layout
        elif isinstance(self.track_layout.lay_pad_stiff, LayoutStoch):
            #
            mean = self.track_layout.lay_pad_stiff.mean
            std = self.track_layout.lay_pad_stiff.std
            lim_min = self.track_layout.lay_pad_stiff.lim_min
            lim_max = self.track_layout.lay_pad_stiff.lim_max

            # Generate pad stiffness properties based on truncated normal distribution
            for pos in mount_pos:
                value = [round(truncnorm((lim_min[i] - mean[i]) / std[i], (lim_max[i] - mean[i]) / std[i], loc=mean[i],
                                         scale=std[i]).rvs(1)[0], 5) for i in range(len(mean))]
                self.mount_prop[pos] = DiscrPad(sp=value)


    def __init__(self, rail, ballast, track_layout, num_mount_pos):
        super().__init__(rail, ballast)
        self.track_layout = track_layout
        self.num_mount_pos = num_mount_pos
        self.calc_mount_pos()
        self.mount_properties(self.mount_pos)









