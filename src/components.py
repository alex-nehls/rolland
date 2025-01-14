"""Defines all superstructure components."""

from traitlets import Enum, Float, HasTraits, List, Tuple

from database.db_rail import RAIL_DATABASE
from database.db_wheel import WHEEL_DATABASE
from database.db_wheel_prof import WHEEL_PROF_DATABASE


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


class Wheel(HasTraits):
    """Wheel class."""

    # Wheel type (w_type_a, w_type_b, ...)
    w_type = Enum(list(WHEEL_DATABASE.keys()), default_value="w_type_a")

    # Wheel running surface profile
    w_prof = Enum(list(WHEEL_PROF_DATABASE.keys()), default_value="S1002")

    # Wheel geometry coordinates [m]
    w_geo = List(Tuple(Float(), Float()),
                 default_value=WHEEL_DATABASE.get("w_type_a", {}).get("w_geo", [(0.0, 0.0)]), minlen=1)

    # Wheel mass [kg]
    mw = Float(default_value=WHEEL_DATABASE.get("w_type_a", {}).get("mw", 0.0))

    # Reduced wheel mass (lateral dynamics) [kg]
    mw_red = Float(default_value=WHEEL_DATABASE.get("w_type_a", {}).get("mw_red", 0.0))

    # Wheel radius [m]
    rw = Float(default_value=WHEEL_DATABASE.get("w_type_a", {}).get("rw", 0.0))


class WheelGreensfunc(HasTraits):
    """Wheel Greens function class."""

    # Green's function type
    w_gf = Array()

    # Green's function frequency values [Hz]
    w_gf_freq = Array()



class Roughness(HasTraits):
    """Roughness class."""

    # Rail roughness type (r_rough_a, r_rough_b, r_rough_c, ...)
    r_rough_type = Enum(list(RAIL_ROUGHNESS_DATABASE.keys()), default_value="r_rough_a")

    # Rail roughness spectrum [f, m]
    r_rough = Tuple(List(Float()), List(Float()),
                    default_value=RAIL_ROUGHNESS_DATABASE.get("r_rough_a", {})
                    .get("r_rough", ([0.0, 0.0], [0.0, 0.0])), minlen=2, maxlen=2)

    # Rail roughness frequency values [Hz]
    r_rough_f = List(Float(),
                     default_value=RAIL_ROUGHNESS_DATABASE.get("r_rough_a", {}).get("r_rough", [0.0, 0.0]), minlen=2)

    # Wheel roughness type (w_rough_a, w_rough_b, w_rough_c, ...)
    w_rough_type = Enum(list(WHEEL_ROUGHNESS_DATABASE.keys()), default_value="w_rough_a")

    # Wheel roughness spectrum [f, m]
    w_rough = Tuple(List(Float()), List(Float()))

    # Contact filter [f, m]
    c_filter = Any()


class Damping(HasTraits):
    """Damping class."""

    # Rail loss factor [-]
    etar = Float()

    # Rail resonance frequency [Hz]
    fresr = Float()

    # Rail damping coefficient (viscous) [Ns/m]
    dr = Float()

    # Pad loss factor [-]
    etap = Float()

    # Pad resonance frequency [Hz]
    fresp = Float()

    # Pad damping coefficient (viscous) for continuous pad [Ns/m^2]
    dp_cont = Float()

    # Pad damping coefficient (viscous) for discrete pad [Ns/m]
    dp_discr = Float()

    # Ballast loss factor [-]
    etab = Float()

    # Ballast resonance frequency [Hz]
    fresb = Float()

    # Ballast damping coefficient (viscous) [Ns/m]
    db = Float()