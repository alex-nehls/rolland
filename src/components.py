"""Defines all superstructure components."""

from traitlets import Enum, Float, HasTraits, List, Tuple
from traittypes import Array

from database.db_rail import RAIL_DATABASE
from database.db_wheel import WHEEL_DATABASE
from database.db_wheel_prof import WHEEL_PROF_DATABASE
from database.db_wheel_roughn import WHEEL_ROUGHNESS_DATABASE


class Rail(HasTraits):
    """Rail class."""

    # Rail profile
    rl_prof = Enum(list(RAIL_DATABASE.keys()), default_value="UIC60")

    # Rail outline coordinates [m]
    rl_geo = List(Tuple(Float(), Float()),
                  default_value=RAIL_DATABASE.get("UIC60", {}).get("rl_geo", [(0.0, 0.0)]), minlen=1)

    # Youngs modulus of rail [Pa]
    E = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("E", 0.0))

    # Shear modulus of rail [Pa]
    G = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("G", 0.0))

    # Poisson's ratio of rail [-]
    nu = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("nu", 0.0))

    # Timoshenko shear correction factor [-]
    kap = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("kap", 0.0))

    # Rail mass per unit length [kg/m]
    mr = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("mr", 0.0))

    # Rail damping coefficient [Ns/m]
    dr = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("dr", 0.0))

    # Rail shear center [m]
    gamr = List(Float(), default_value=RAIL_DATABASE.get("UIC60", {}).get("gamr", [0.0, 0.0]), minlen=2, maxlen=2)

    # Center of gravity [m]
    epsr = List(Float(), default_value=RAIL_DATABASE.get("UIC60", {}).get("epsr", [0.0, 0.0]), minlen=2, maxlen=2)

    # Area moment of inertia of rail around y-axis [m^4]
    Iyr = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("Iyr", 0.0))

    # Area moment of inertia of rail around z-axis [m^4]
    Izr = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("Izr", 0.0))

    # Torsional constant of rail [m^4]
    Itr = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("Itr", 0.0))

    # Cross-sectional area of rail [m^2]
    Ar = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("Ar", 0.0))

    # Surface area per unit length of rail [m^2/m]
    Asr = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("Asr", 0.0))

    # Volume per unit length of rail [m^3/m]
    Vr = Float(default_value=RAIL_DATABASE.get("UIC60", {}).get("Vr", 0.0))


class DiscrPad(HasTraits):
    """Discr pad class."""

    # Pad stiffness vertical/lateral (total value) [N/m]
    sp = List(Float(), default_value=[0.0, 0.0], maxlen=2)

    # Pad width [m]
    wdthp = Float()

class ContPad(HasTraits):
    """Cont pad class."""

    # Pad stiffness vertical/lateral (per meter) [N/m^2]
    sp = List(Float(), default_value=[0.0, 0.0], maxlen=2)

    # Pad width [m]
    wdthp = None


class Sleeper(HasTraits):
    """Sleeper class."""

    # Sleeper mass [kg]
    ms = Float()

    # Sleeper bending stiffness [Nm^2]
    Bs = Float()

    # Sleeper length [m]
    ls = Float()

    # Sleeper width [m]
    wdths = Float()


class Ballast(HasTraits):
    """Ballast class."""

    # Ballast stiffness [N/m]
    sb = Float()

    # Ballast damping coefficient [Ns/m]
    db = Float()


class Wheel(HasTraits):
    """Wheel class."""

    # Wheel type (w_type_a, w_type_b, ...)
    w_type = Enum(list(WHEEL_DATABASE.keys()), default_value="w_type_a")

    # Wheel running surface profile
    w_prof = Enum(list(WHEEL_PROF_DATABASE.keys()), default_value="S1002")

    # Wheel running surface coordinates [m]
    w_geo = List(Tuple(Float(), Float()), default_value=[(0.0, 0.0)], minlen=1)

    # wheel deformability (rigid, deformable)
    w_deform = Enum(["rigid", "deform"], default_value="rigid")

    # Wheel mass [kg]
    mw = Float()

    # Reduced wheel mass (lateral dynamics) [kg]
    mw_red = Float()

    # Wheel radius [m]
    rw = Float()

    # Wheel damping coefficient [Ns/m]
    dw = Float()

    # Green’s function type
    w_greensf = Array()

    # Wheel contact filter type (w_rough_a, w_rough_b, w_rough_c, ...)
    w_rough_type = Enum(list(WHEEL_ROUGHNESS_DATABASE.keys()), default_value="w_rough_a")

    # Wheel roughness/contact filter [f, m]
    w_rough = Tuple(List(Float()), List(Float()), default_value=([0.0, 0.0], [0.0, 0.0]), minlen=2, maxlen=2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_attributes_from_profile()
        self.set_profile_attributes()
        self.set_roughness_attributes()
        if self.w_deform == "rigid":
            self.w_greensf = []


    def set_attributes_from_profile(self):
        attributes = WHEEL_DATABASE.get(self.w_type, {})
        self.mw = attributes.get("mw", 0.0)
        self.mw_red = attributes.get("mw_red", 0.0)
        self.rw = attributes.get("rw", 0.0)
        self.dw = attributes.get("dw", 0.0)
        self.w_greensf = attributes.get("w_greensf", [])

    def set_profile_attributes(self):
        attributes = WHEEL_PROF_DATABASE.get(self.w_prof, {})
        self.w_geo = attributes.get("w_geo", [(0.0, 0.0), (0.0, 0.0)])

    def set_roughness_attributes(self):
        attributes = WHEEL_ROUGHNESS_DATABASE.get(self.w_rough_type, {})
        self.w_rough = attributes.get("w_rough", [(0.0, 0.0), (0.0, 0.0)])
