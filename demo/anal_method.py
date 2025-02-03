from matplotlib import pyplot as plt
from numpy import array, linspace

from rolland.components import Ballast, DiscrPad, Slab, Sleeper, ContPad
from rolland.database.rail.db_rail import UIC60
from rolland.methods.analytical import (
    ThompsonEBBCont1LSupp,
    ThompsonEBBCont2LSupp,
    ThompsonTSDiscr1LSupp,
    ThompsonTSDiscr2LSupp,
    HecklTBDiscr1LSupp,
    HecklTBDiscr2LSupp,
)

from rolland.track import (
    ContBallastedSingleRailTrack,
    ContSlabSingleRailTrack,
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


track_discr_slab = SimplePeriodicSlabSingleRailTrack(
    rail=UIC60,
    pad=DiscrPad(sp=[300*10**6, 0], etap=0.25),
    slab=Slab(ms=162),
    num_mount=241,
    distance=0.6,
)

track_discr_ball = SimplePeriodicBallastedSingleRailTrack(
    rail=UIC60,
    pad=DiscrPad(sp=[300*10**6, 0], etap=0.25),
    sleeper=Sleeper(ms=162),
    ballast=Ballast(sb=[50*10**6, 0], etab=1),
    num_mount=241,
    distance=0.6,
)


method_1 = ThompsonEBBCont1LSupp(track=track_cont_slab, f=linspace(20, 3000, 1500),
                                 force=1, x=array([0, 10]))

method_2 = ThompsonEBBCont2LSupp(track=track_cont_ball, f=linspace(20, 3000, 1500),
                                 force=1, x=array([0, 10]))


method_3 = ThompsonTSDiscr2LSupp(track=track_discr_ball, f=linspace(20, 3000, 1500),
                                 force=1, x=array([240 * 0.3 + 0.6]), x_excit=240*0.3 + 0.6)

method_4 = ThompsonTSDiscr1LSupp(track=track_discr_slab, f=linspace(20, 3000, 1500),
                                 force=1, x=array([240 * 0.3 + 0.6]), x_excit=240*0.3 + 0.6)


method_5 = HecklTBDiscr2LSupp(track=track_discr_ball, f=linspace(20, 3000, 1500),
                              force=1, x=array([240*0.3 + 0.6]), x_excit=240*0.3 + 0.6)

method_6 = HecklTBDiscr1LSupp(track=track_discr_slab, f=linspace(20, 3000, 1500),
                              force=1, x=array([240*0.3 + 0.6]), x_excit=240*0.3 + 0.6)



fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 20))

# Plot method_1 and method_2 in one plot
ax1.loglog(method_1.f, abs(method_1.mobility[0, :]), label='ThompsonEBBCont1LSupp', color='black')
ax1.loglog(method_2.f, abs(method_2.mobility[0, :]), label='ThompsonEBBCont2LSupp', color='blue')
ax1.set_title('Yb over f for method_1 and method_2')
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Yb [m/N]')
ax1.grid(True)
ax1.legend()

# Plot method_3 and method_5 in one plot
ax2.loglog(method_3.f, abs(method_3.mobility[0, :]), label='ThompsonTSDiscr2LSupp', color='black')
ax2.loglog(method_5.f, abs(method_5.mobility[0, :]), label='HecklTBDiscr2LSupp', color='blue')
ax2.set_title('Yb over f for method_3 and method_5')
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('Yb [m/N]')
ax2.grid(True)
ax2.legend()

# Plot method_4 and method_6 in one plot
ax3.loglog(method_4.f, abs(method_4.mobility[0, :]), label='ThompsonTSDiscr1LSupp', color='black')
ax3.loglog(method_6.f, abs(method_6.mobility[0, :]), label='HecklTBDiscr1LSupp', color='blue')
ax3.set_title('Yb over f for method_4 and method_6')
ax3.set_xlabel('Frequency [Hz]')
ax3.set_ylabel('Yb [m/N]')
ax3.grid(True)
ax3.legend()

plt.tight_layout()
plt.show()