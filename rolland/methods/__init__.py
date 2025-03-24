# ------------------------------------------------------------------------------
# Rolland
# ------------------------------------------------------------------------------

"""The Rolland library: several classes for the implementation of rolling noise calculation."""


from .analytical import (
    EBBCont1LSupp,
    EBBCont2LSupp,
    TSDiscr1LSupp,
    TSDiscr2LSupp,
)

__all__ = ["EBBCont1LSupp",
           "TSDiscr2LSupp",
           "TSDiscr1LSupp",
           "EBBCont2LSupp"]



