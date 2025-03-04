# ------------------------------------------------------------------------------
# Rolland
# ------------------------------------------------------------------------------

"""The Rolland library: several classes for the implementation of rolling noise calculation."""


from .analytical import (
    ThompsonEBBCont1LSupp,
    ThompsonEBBCont2LSupp,
    ThompsonTSDiscr1LSupp,
    ThompsonTSDiscr2LSupp,
)

__all__ = ["ThompsonEBBCont1LSupp",
           "ThompsonTSDiscr2LSupp",
           "ThompsonTSDiscr1LSupp",
           "ThompsonEBBCont2LSupp"]



