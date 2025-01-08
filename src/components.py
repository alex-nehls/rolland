"""Defines all superstructure components."""

from traitlets import Float, HasTraits


class Pad(HasTraits):
    """rail pad class."""

    sp = Float(default_value=0.0)
    dp = Float(default_value=0.0)
    wdthp = Float(default_value=0.0)

