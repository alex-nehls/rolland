"""Defines all superstructure components."""

from traitlets import Float, HasTraits, List


class Pad(HasTraits):
    """Rail pad class."""

    # Pad stiffness vertical/lateral [N/m]
    sp = List(Float(), default_value=[0.0, 0.0], maxlen=2)

    # Pad damping coefficient [Ns/m]
    dp = Float(default_value=0.0)

    # Pad width [m]
    wdthp = Float(default_value=0.0)