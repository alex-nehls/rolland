"""Wheel type instances.

This module contains instances of the Wheel class representing different wheel types.

Wheel types:
    - w_type_a
    - w_type_b

Attributes
----------
    w_prof (str): Wheel running surface profile.
    w_geo (list): Wheel geometry coordinates [m].
    mw (float): Wheel mass [kg].
    mw_red (float): Reduced wheel mass (lateral dynamics) [kg].
    rw (float): Wheel radius [m].
"""


from src.components import Wheel

w_type_a = Wheel(
    w_type="w_type_a",
    w_prof="S1002",
    w_geo=[(0.0, 0.0)],
    mw=400.0,
    mw_red=5.0,
    rw=0.46
)

w_type_b = Wheel(
    w_type="w_type_b",
    w_prof="S1002",
    w_geo=[(0.0, 0.0)],
    mw=450.0,
    mw_red=5.5,
    rw=0.48
)