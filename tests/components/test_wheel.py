
from database.db_wheel import WHEEL_DATABASE
from database.db_wheel_prof import WHEEL_PROF_DATABASE
from database.db_wheel_roughn import WHEEL_ROUGHNESS_DATABASE
from src.components import Wheel


def test_wheel_initialization():
    wheel = Wheel(w_type="w_type_a", w_prof="S1002", w_rough_type="w_rough_a", w_deform="deform")

    assert wheel.w_type == "w_type_a"
    assert wheel.w_prof == "S1002"
    assert wheel.mw == WHEEL_DATABASE["w_type_a"]["mw"]
    assert wheel.mw_red == WHEEL_DATABASE["w_type_a"]["mw_red"]
    assert wheel.rw == WHEEL_DATABASE["w_type_a"]["rw"]
    assert wheel.dw == WHEEL_DATABASE["w_type_a"]["dw"]
    assert wheel.w_greensf.size > 0
    assert wheel.w_geo == WHEEL_PROF_DATABASE["S1002"]["w_geo"]
    assert wheel.w_rough == WHEEL_ROUGHNESS_DATABASE["w_rough_a"]["w_rough"]

def test_wheel_deformability():
    wheel = Wheel(w_deform="rigid")
    assert wheel.w_deform == "rigid"
    assert wheel.w_greensf.size == 0

    wheel = Wheel(w_deform="deform")
    assert wheel.w_deform == "deform"
    assert wheel.w_greensf is not None
