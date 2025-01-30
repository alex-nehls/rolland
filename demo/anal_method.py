from matplotlib import pyplot as plt
from numpy import array, linspace

from rolland.components import Ballast, DiscrPad, Slab, Sleeper
from rolland.database.rail.db_rail import UIC60
from rolland.methods.analytical import (
    HecklTBDiscr1LSupp,
    HecklTBDiscr2LSupp,
    ThompsonTSDiscr1LSupp,
    ThompsonTSDiscr2LSupp,
)
from rolland.track import (
                                        SimplePeriodicBallastedSingleRailTrack,
                                        SimplePeriodicSlabSingleRailTrack,
)


track_cont_slab = ContSlabSingleRailTrack(
    rail=UIC60,
    pad=ContPad(sp=[300*10**6, 0], dp=[30000, 0]),
)

track_cont_ball = ContBallastedSingleRailTrack(
    rail=UIC60,
    pad=ContPad(sp=[300*10**6, 0], dp=[30000, 0]),
    slab=Slab(ms=250),
    ballast=Ballast(sb=[100*10**6, 0], db=[80000, 0]),
)


track_discr_ball = SimplePeriodicBallastedSingleRailTrack(
    rail=UIC60,
    pad=DiscrPad(sp=[300*10**6, 0], etap=0.25),
    sleeper=Sleeper(ms=162),
    ballast=Ballast(sb=[50*10**6, 0], etab=1),
    num_mount=241,
    distance=0.6,
)

track_discr_slab = SimplePeriodicSlabSingleRailTrack(
    rail=UIC60,
    pad=DiscrPad(sp=[300*10**6, 0], etap=0.25),
    slab=Slab(ms=162),
    num_mount=241,
    distance=0.6,
)
"""
method1 = ThompsonEBBCont1LSupp(
    track=track_cont_slab,
    f=arange(10, 10000, 10),
    F=1,
    x=array([0, 10]),
)

method2 = ThompsonEBBCont2LSupp(
    track=track_cont_ball,
    f=arange(10, 10000, 10),
    F=1,
    x=array([0, 10]),
)
"""

method1 = ThompsonTSDiscr2LSupp(track=track_discr_ball, f=linspace(20, 3000, 1500), F=1, x=array([240 * 0.3 + 0.6]),
                                x_excit=240*0.3 + 0.6)

method2 = ThompsonTSDiscr1LSupp(track=track_discr_slab, f=linspace(20, 3000, 1500), F=1, x=array([240 * 0.3 + 0.6]),
                                x_excit=240*0.3 + 0.6)


method3 = HecklTBDiscr2LSupp(track=track_discr_ball, f=linspace(20, 3000, 1500), F=1, x=array([240*0.3 + 0.6]),
    x_excit=240*0.3 + 0.6)

method4 = HecklTBDiscr1LSupp(track=track_discr_slab, f=linspace(20, 3000, 1500), F=1, x=array([240*0.3 + 0.6]),
    x_excit=240*0.3 + 0.6)



fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 15))

# Plot ax1 and ax3 in one plot
ax1.loglog(method1.f, abs(method1.Yb[0, :]), label='method1')
ax1.loglog(method3.f, abs(method3.Yb[0, :]), label='method3')
ax1.set_title('Yb over f for method1 and method3')
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Yb [m/N]')
ax1.grid(True)
ax1.legend()

# Plot ax2 and ax4 in one plot
ax2.loglog(method2.f, abs(method2.Yb[0, :]), label='method2')
ax2.loglog(method4.f, abs(method4.Yb[0, :]), label='method4')
ax2.set_title('Yb over f for method2 and method4')
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('Yb [m/N]')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()
