"""Wheel database."""

from numpy import array

WHEEL_DATABASE = {
    "w_type_a": {
        "mw": 400.0,
        "mw_red": 5.0,
        "rw": 0.46,
        "dw": 0.05,
        "w_greensf": array([[0.1, 0.2, 0.3],
                            [0.1, 0.2, 0.3]])
    },

    "w_type_b": {
        "mw": 450.0,
        "mw_red": 5.5,
        "rw": 0.48,
        "dw": 0.06,
        "w_greensf": array([[0.1, 0.2, 0.3],
                            [0.1, 0.2, 0.3]])
    },
}
