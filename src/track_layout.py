"""Defines the track layout."""

from traitlets import Float, HasTraits, Instance, List, Tuple, Union


class LayoutConst(HasTraits):
    """Defines a constant layout value."""

    # Value of constant layout parameter
    value = Union((Float(), List(Float())))


class LayoutPeriod(HasTraits):
    """Defines a periodic layout."""

    # Period of variable layout parameter
    period = Union((List(Float()), List(Tuple(Float(), Float()))))


class LayoutStoch(HasTraits):
    """Defines a stochastic layout."""

    # Mean value of stochastic layout
    mean = Union((Float(), List(Float())))

    # Standard deviation of stochastic layout
    std = Union((Float(), List(Float())))

    # Minimum limit of stochastic layout
    lim_min = Union((Float(), List(Float())))

    # Maximum limit of stochastic layout
    lim_max = Union((Float(), List(Float())))



class TrackLayout(HasTraits):
    """Defines the track layout."""

    # Layout of pad stiffness
    lay_pad_stiff = Union((Instance(LayoutConst), Instance(LayoutPeriod), Instance(LayoutStoch)),
                          default_value=None)

    # Layout of sleeper mass
    lay_slep_mass = Union((Instance(LayoutConst), Instance(LayoutPeriod), Instance(LayoutStoch)),
                          default_value=None)

    # Layout of sleeper distance
    lay_slep_dist = Union((Instance(LayoutConst), Instance(LayoutPeriod), Instance(LayoutStoch)),
                          default_value=None)
