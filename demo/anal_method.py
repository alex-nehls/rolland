from matplotlib import pyplot as plt
from numpy import arange, array

from rolland.components import Ballast, ContPad, DiscrPad, Slab, Sleeper
from rolland.database.rail.db_rail import UIC60
from rolland.methods.analytical import (
                                        HecklTBDiscr1LSupp,
                                        HecklTBDiscr2LSupp,
                                        ThompsonEBBCont1LSupp,
                                        ThompsonEBBCont2LSupp,
)
from rolland.track import (
    ContBallastedSingleRailTrack,
    ContSlabSingleRailTrack,
    SimplePeriodicBallastedSingleRailTrack,
    SimplePeriodicSlabSingleRailTrack,
)

track1 = ContSlabSingleRailTrack(
    rail=UIC60,
    pad=ContPad(sp=[300*10**6, 0], dp=[30000, 0]),
)

track2 = ContBallastedSingleRailTrack(
    rail=UIC60,
    pad=ContPad(sp=[300*10**6, 0], dp=[30000, 0]),
    slab=Slab(ms=250),
    ballast=Ballast(sb=[100*10**6, 0], db=[80000, 0]),
)

track3 = SimplePeriodicBallastedSingleRailTrack(
    rail=UIC60,
    pad=DiscrPad(sp=[300*10**6 * 0.6, 0], etap=0.1),
    sleeper=Sleeper(ms=150),
    ballast=Ballast(sb=[100*10**6 * 0.6, 0], etab=0.6),
    num_mount=300,
    distance=0.6,
)

track4 = SimplePeriodicSlabSingleRailTrack(
    rail=UIC60,
    pad=DiscrPad(sp=[300*10**6 * 0.6, 0], etap=0.1),
    slab=Slab(ms=150),
    num_mount=300,
    distance=0.6,
)

method1 = ThompsonEBBCont1LSupp(
    track=track1,
    f=arange(10, 10000, 10),
    F=1,
    x=array([0, 10]),
)

method2 = ThompsonEBBCont2LSupp(
    track=track2,
    f=arange(10, 10000, 10),
    F=1,
    x=array([0, 10]),
)


method3 = HecklTBDiscr2LSupp(
    track=track3,
    f=arange(10, 10000, 10),
    F=1,
    x=array([299*0.3 + 0.3]),
    x_excit=299*0.3 + 0.3,
)


method4 = HecklTBDiscr1LSupp(
    track=track4,
    f=arange(10, 10000, 10),
    F=1,
    x=array([299*0.3 + 0.3]),
    x_excit=299*0.3 + 0.3,
)


fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 20))

ax1.loglog(method1.f, abs(method1.Yb[0, :]))
ax1.set_title('Yb over f for method1')
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Yb [m/N]')
ax1.grid(True)

ax2.loglog(method2.f, abs(method2.Yb[0, :]))
ax2.set_title('Yb over f for method2')
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('Yb [m/N]')
ax2.grid(True)

ax3.loglog(method3.f, abs(method3.Yb[0, :]))
ax3.set_title('Yb over f for method3')
ax3.set_xlabel('Frequency [Hz]')
ax3.set_ylabel('Yb [m/N]')
ax3.grid(True)

ax4.loglog(method4.f, abs(method4.Yb[0, :]))
ax4.set_title('Yb over f for method4')
ax4.set_xlabel('Frequency [Hz]')
ax4.set_ylabel('Yb [m/N]')
ax4.grid(True)

plt.tight_layout()
plt.show()
