"""Defines all superstructure components."""

from traitlets import Float, HasTraits, Int, List, Tuple, Unicode

from database.db_rail import RAIL_DATABASE


class Rail(HasTraits):
    """Rail class."""

    # Rail profile
    rl_prof = Unicode(default_value="UIC60")

    # Rail number
    rl_num = Int(default_value=1, min=1, max=2)

    # Rail outline coordinates [m]
    rl_geo = List(Tuple(Float(), Float()), default_value=[(0.0, 0.0)], minlen=1)

    # Rail bending stiffness [Nm^2]
    Br = Float()

    # Rail damping coefficient [Ns/m]
    dr = Float()

    # Rail mass per unit length [kg/m]
    mr = Float()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_attributes_from_profile()

    def set_attributes_from_profile(self):
        attributes = RAIL_DATABASE.get(self.rl_prof, {})
        self.rl_geo = attributes.get("rl_geo", [(0.0, 0.0)])
        self.Br = attributes.get("Br", 0.0)
        self.dr = attributes.get("dr", 0.0)
        self.mr = attributes.get("mr", 0.0)


class Pad(HasTraits):
    """Rail pad class."""

    # Pad type (discr: discrete, cont: continuous)
    p_type = Unicode(default_value="discr").tag(config=True)

    # Pad stiffness vertical/lateral (discr: [N/m], cont: [N/m^2])
    sp = List(Float(), default_value=[0.0, 0.0], maxlen=2)

    # Pad damping coefficient [Ns/m]
    dp = Float()

    # Pad width [m]
    wdthp = Float()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.p_type == "cont":
            self.wdthp = None


class Sleeper(HasTraits):
    """Sleeper class."""

    # Sleeper mass [kg]
    ms = Float()

    # Sleeper length [m]
    ls = Float()

    # Sleeper bending stiffness [Nm^2]
    Bs = Float()

