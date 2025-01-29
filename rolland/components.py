"""Defines all superstructure components."""
from traitlets import Float, HasTraits, List, Tuple, Unicode
from traittypes import Array


class Rail(HasTraits):
    """Rail class."""

    # Rail outline coordinates [m]
    rl_geo = List(Tuple(Float(), Float()))

    # Youngs modulus of rail [Pa]
    E = Float()

    # Shear modulus of rail [Pa]
    G = Float()

    # Poisson's ratio of rail [-]
    nu = Float()

    # Timoshenko shear correction factor [-]
    kap = Float()

    # Rail mass per unit length [kg/m]
    mr = Float()

    # Density of rail [kg/m^3]
    rho = Float()

    # Rail loss factor [-]
    etar = Float()

    # Rail resonance frequency [Hz]
    fresr = Float()

    # Rail damping coefficient (viscous) [Ns/m]
    dr = Float()

    # Rail shear center [m]
    gamr = List(Float())

    # Center of gravity [m]
    epsr = List(Float())

    # Area moment of inertia of rail around y-axis [m^4]
    Iyr = Float()

    # Area moment of inertia of rail around z-axis [m^4]
    Izr = Float()

    # Torsional constant of rail [m^4]
    Itr = Float()

    # Cross-sectional area of rail [m^2]
    Ar = Float()

    # Surface area per unit length of rail [m^2/m]
    Asr = Float()

    # Volume per unit length of rail [m^3/m]
    Vr = Float()


class RailRoughness(HasTraits):
    """Rail roughness class."""

    # Rail roughness spectrum [f, m]
    r_rough = Tuple(List(Float()), List(Float()))


class DiscrPad(HasTraits):
    """Discr pad class."""

    # Pad stiffness vertical/lateral (total value) [N/m]
    sp = List(Float(), default_value=[0.0, 0.0], maxlen=2)

    # Pad width [m]
    wdthp = Float()

    # Pad loss factor [-]
    etap = Float()

    # Pad resonance frequency [Hz]
    fresp = List(Float(), default_value=[0.0, 0.0], maxlen=2)

    # Pad damping coefficient (viscous) for discrete pad [Ns/m]
    dp = List(Float(), default_value=[0.0, 0.0], maxlen=2)


class ContPad(HasTraits):
    """Cont pad class."""

    # Pad stiffness vertical/lateral (per meter) [N/m^2]
    sp = List(Float(), default_value=[0.0, 0.0], maxlen=2)

    # Pad loss factor [-]
    etap = Float()

    # Pad resonance frequency [Hz]
    fresp = List(Float(), default_value=[0.0, 0.0], maxlen=2)

    # Pad damping coefficient (viscous) for continuous pad [Ns/m^2]
    dp = List(Float(), default_value=[0.0, 0.0], maxlen=2)


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


class Slab(HasTraits):
    """Slab class."""

    # Slab mass per unit length [kg/m]
    ms = Float()

    # Slab depth [m]
    ls = Float()


class Ballast(HasTraits):
    """Ballast class."""

    # Ballast stiffness [N/m]
    sb = List(Float(), default_value=[0.0, 0.0], maxlen=2)

    # Ballast loss factor [-]
    etab = Float()

    # Ballast resonance frequency [Hz]
    fresb = List(Float(), default_value=[0.0, 0.0], maxlen=2)

    # Ballast damping coefficient (viscous) [Ns/m]
    db = List(Float(), default_value=[0.0, 0.0], maxlen=2)



class Wheel(HasTraits):
    """Wheel class."""

    # Wheel cross-sectional geometry coordinates [m]
    w_geo_cross_sec = List(Tuple(Float(), Float()))

    # Wheel running surface profile
    w_prof = Unicode()

    # Wheel geometry coordinates [m]
    w_geo = List(Tuple(Float(), Float()))

    # Wheel mass [kg]
    mw = Float()

    # Reduced wheel mass (lateral dynamics) [kg]
    mw_red = Float()

    # Wheel radius [m]
    rw = Float()


class WheelRoughness(HasTraits):
    """Wheel roughness class."""

    # Wheel roughness spectrum [f, m]
    w_rough = Tuple(List(Float()), List(Float()))


class WheelGreensfunc(HasTraits):
    """Wheel Greens function class."""

    # Green's function type
    w_gf = Array()

    # Green's function frequency values [Hz]
    w_gf_freq = Array()
