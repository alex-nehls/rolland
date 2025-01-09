"""Defines all rail components.

The database contains the following rail profiles:
- UIC60
- UIC54

The database contains the following rail properties in SI units:
- Rail contour coordinates (rl_geo)
- Elastic modulus (E)
- Shear modulus (G)
- Poisson's ratio (nu)
- Timoshenko shear correction factor (kap)
- Rail mass per unit length (mr)
- Rail damping coefficient (dr)
- Rail shear center with respect to centroid in z-direction (gammar)
- Area moment of inertia of rail around y-axis (Iyr)
- Area moment of inertia of rail around z-axis (Izr)
- Torsional constant of rail (Itr)
- Cross-sectional area of rail (Ar)
- Surface area per unit length of rail (Asr)
- Volume per unit length of rail (Vr)
"""

RAIL_DATABASE = {
"UIC60": {
    "rl_geo": [ # arbitrary values!
        (0, 4.6), (1, 4.5), (2, 5.3), (3, 4.8), (4, 9.8), (5, 3.7), (6, 7.9), (7, 2.1), (8, 0.5), (9, 1.7),
        (10, 2.0), (11, 2.6), (12, 8.0), (13, 8.2), (14, 1.8), (15, 8.4), (16, 5.3), (17, 7.9), (18, 5.5),
        (19, 7.0), (20, 0.6), (21, 3.6), (22, 6.2), (23, 4.3), (24, 1.1), (25, 5.2), (26, 0.0), (27, 3.6),
        (28, 1.1), (29, 5.3), (30, 0.9), (31, 7.0), (32, 5.9), (33, 8.8), (34, 7.4), (35, 4.4), (36, 2.3),
        (37, 7.5), (38, 6.9), (39, 2.4), (40, 0.9), (41, 7.8), (42, 8.4), (43, 5.7), (44, 8.3), (45, 5.5),
        (46, 7.8), (47, 2.0), (48, 4.4), (49, 2.7)
    ],
    "E": 210e9,
    "G": 81e9,
    "nu": 0.3,
    "kap": 0.0,
    "mr": 60.2,
    "dr": 0.00,
    "gammar": 0.0,
    "Iyr": 3038.30e-8,
    "Izr": 512.30e-8,
    "Itr": 209.20e-8,
    "Ar": 76.70e-4,
    "Asr": 0.688,
    "Vr": 7670.00e-6,
},

"UIC54": {
    "rl_geo": [ # arbitrary values!
        (0, 4.6), (1, 4.5), (2, 5.3), (3, 4.8), (4, 9.8), (5, 3.7), (6, 7.9), (7, 2.1), (8, 0.5), (9, 1.7),
        (10, 2.0), (11, 2.6), (12, 8.0), (13, 8.2), (14, 1.8), (15, 8.4), (16, 5.3), (17, 7.9), (18, 5.5),
        (19, 7.0), (20, 0.6), (21, 3.6), (22, 6.2), (23, 4.3), (24, 1.1), (25, 5.2), (26, 0.0), (27, 3.6),
        (28, 1.1), (29, 5.3), (30, 0.9), (31, 7.0), (32, 5.9), (33, 8.8), (34, 7.4), (35, 4.4), (36, 2.3),
        (37, 7.5), (38, 6.9), (39, 2.4), (40, 0.9), (41, 7.8), (42, 8.4), (43, 5.7), (44, 8.3), (45, 5.5),
        (46, 7.8), (47, 2.0), (48, 4.4), (49, 2.7)
    ],
    "E": 0.0,
    "G": 0.0,
    "nu": 0.0,
    "kap": 0.0,
    "mr": 54.0,
    "dr": 0.00,
    "gammar": 0.0,
    "Iyr": 0.0,
    "Izr": 0.0,
    "Itr": 0.0,
    "Ar": 0.0,
    "Asr": 0.0,
    "Vr": 0.0,
}
}
