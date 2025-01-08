"""Defines all superstructure components."""

from traitlets import Float, HasTraits, Int, List, Tuple, Unicode


class Rail(HasTraits):
    """Rail class."""

    # Rail profile
    rl_prof = Unicode(default_value="UIC60")

    # Rail outline coordinates [m]
    rl_geo = List(Tuple(Float(), Float()), default_value=[(0.0, 0.0)], minlen=1)

    # Rail number
    rl_num = Int(default_value=1, min=1, max=2)

    # Rail bending stiffness [Nm^2]
    Br = Float()

    # Rail damping coefficient [Ns/m]
    dr = Float()

    # Rail mass per unit length [kg/m]
    mr = Float()


class Pad(HasTraits):
    """Rail pad class."""

    # Pad stiffness vertical/lateral [N/m]
    sp = List(Float(), default_value=[0.0, 0.0], maxlen=2)

    # Pad damping coefficient [Ns/m]
    dp = Float(default_value=0.0)

    # Pad width [m]
    wdthp = Float(default_value=0.0)