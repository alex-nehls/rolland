"""Defines all superstructure components."""

from traitlets import Enum, Float, HasTraits, Int, List, Tuple

from database.db_rail import RAIL_DATABASE
from database.db_rail_roughn import RAIL_ROUGHNESS_DATABASE


class Rail(HasTraits):
    """Rail class."""

    # Rail profile
    rl_prof = Enum(list(RAIL_DATABASE.keys()), default_value="UIC60")

    # Rail number
    rl_num = Int(default_value=1, min=1, max=2)

    # Rail outline coordinates [m]
    rl_geo = List(Tuple(Float(), Float()), default_value=[(0.0, 0.0)], minlen=1)

    # Beam type (TS: Timoshenko, EB: Euler-Bernoulli)
    bm_type = Enum(["TS", "EB"], default_value="TS").tag(config=True)

    # Elastic modulus of rail [Pa]
    E = Float()

    # Shear modulus of rail [Pa]
    G = Float()

    # Poisson's ratio of rail [-]
    nu = Float()

    # Timoshenko shear correction factor [-]
    kap = Float()

    # Rail mass per unit length [kg/m]
    mr = Float()

    # Rail damping coefficient [Ns/m]
    dr = Float()

    # Rail shear center with respect to centroid in z-direction [m]
    gammar = Float()

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_attributes_from_profile()
        self.set_roughness_attributes()

    def set_attributes_from_profile(self):
        attributes = RAIL_DATABASE.get(self.rl_prof, {})
        self.rl_geo = attributes.get("rl_geo", [(0.0, 0.0)])
        self.E = attributes.get("E", 0.0)
        self.G = attributes.get("G", 0.0)
        self.nu = attributes.get("nu", 0.0)
        self.kap = attributes.get("kap", 0.0)
        self.mr = attributes.get("mr", 0.0)
        self.dr = attributes.get("dr", 0.0)
        self.gammar = attributes.get("gammar", 0.0)
        self.Iyr = attributes.get("Iyr", 0.0)
        self.Izr = attributes.get("Izr", 0.0)
        self.Itr = attributes.get("Itr", 0.0)
        self.Ar = attributes.get("Ar", 0.0)
        self.Asr = attributes.get("Asr", 0.0)
        self.Vr = attributes.get("Vr", 0.0)

    # Rail contact filter type (r_rough_a, r_rough_b, r_rough_c, ...)
    r_rough_type = Enum(list(RAIL_ROUGHNESS_DATABASE.keys()), default_value="r_rough_a")

    # Rail roughness/contact filter [f, m]
    r_rough = Tuple(List(Float()), List(Float()), default_value=([0, 0], [0.0, 0.0]), minlen=2, maxlen=2)

    def set_roughness_attributes(self):
        attributes = RAIL_ROUGHNESS_DATABASE.get(self.r_rough_type, {})
        self.r_rough = attributes.get("r_rough", [(0.0, 0.0), (0.0, 0.0)])


class Pad(HasTraits):
    """Rail pad class."""

    # Pad type (discr: discrete, cont: continuous)
    p_type = Enum(["discr", "cont"], default_value="discr").tag(config=True)

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

    # Sleeper type (discr: discrete, cont: continuous)
    sl_type = Enum(["discr", "cont"], default_value="discr").tag(config=True)

    # Foundation type (slab, ballast)
    fnd_type = Enum(["slab", "ballast"], default_value="ballast").tag(config=True)

    # Sleeper mass [kg] (discr: [kg], cont: [kg/m])
    ms = Float()

    # Sleeper bending stiffness [Nm^2]
    Bs = Float()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.fnd_type == "slab":
            self.ms = 1e20
            self.Bs = 1e20

    # Sleeper length [m]
    ls = Float()


class Ballast(HasTraits):
    """Ballast class."""

    # Ballast stiffness [N/m]
    sb = Float()

    # Ballast damping coefficient [Ns/m]
    db = Float()
