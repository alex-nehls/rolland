"""
Track Vibration Analysis using Rolland API.
Moving load simulation for railway track dynamic response.

This script demonstrates velocity-dependent mobility calculation for a
ballasted railway track under moving wheel loads.

Workflow:
    1. Define railway track model (rail, pad, sleeper, ballast)
    2. Set up boundary conditions and excitation
    3. Run FDM simulation for multiple velocities
    4. Calculate and save mobility/receptance frequency responses
"""

# Import required components from Rolland library
from rolland                        import DiscrPad, Sleeper, Ballast
from rolland.database.rail.db_rail  import UIC60  # Standard rail profile
from rolland                        import SimplePeriodicBallastedSingleRailTrack
from rolland.excitation             import ConstantForce
from rolland import(
    PMLRailDampVertic,
    DiscretizationEBBVerticConst,
    DeflectionEBBVertic)
from rolland.postprocessing import(
    Response as resp,
    TDR)
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import os
from pathlib import Path

# =============================================================================
# 1. TRACK DEFINITION
# =============================================================================
# Create a ballasted single rail track model with periodic supports
track = SimplePeriodicBallastedSingleRailTrack(
    rail    = UIC60,                # Standard UIC60 rail profile
    pad     = DiscrPad(
                sp = [300e6, 0],    # Pad Stiffness [N/m]
                dp = [18000, 0]     # Pad Damping [Ns/m]
    ),
    sleeper = Sleeper(ms=150),      # Sleeper mass [kg]
    ballast = Ballast(
                sb = [150e6, 0],    # Ballast stiffness [N/m]
                db = [48000, 0]     # Ballast damping [Ns/m]
    ),
    num_mount   = 100,               # Number of discrete mounting positions
    distance    = 0.6               # Distance between sleepers [m]
)

# =============================================================================
# 2. SIMULATION SETUP
# =============================================================================
# Define boundary conditions (Perfectly Matched Layer absorbing boundary)
boundary    = PMLRailDampVertic(l_bound = 10.0)  # width of boundary domain

# Output directory
output_dir = Path('mobility_plots')
output_dir.mkdir(exist_ok=True)

# clear mobility plots directory
for file in output_dir.glob('*.png'):
    os.remove(file)

# =============================================================================
# 3. VELOCITY SWEEP SIMULATION
# =============================================================================
velocities = np.arange(5, 40, 5)  # 5 to 40 m/s in 5 m/s steps
# velocities = [60]

for vel in velocities:
    print(f"Computing velocity: {vel} m/s ({vel*3.6:.1f} km/h)")
    
    # Define moving load excitation
    starting_position = 15.0
    excitation = ConstantForce(
        x_excit         = [starting_position],
        # x_excit         = [starting_position,
        #                    starting_position + 2.5],    # Starting positions [m]
        velocity        = float(vel),                   # Velocity [m/s]
        force_amplitude = 65000.0                       # [N]
    )

    # Discretize domain
    discretization = DiscretizationEBBVerticConst(track=track, bound=boundary)

    # Solve for deflection
    deflection_results = DeflectionEBBVertic(
        discr=discretization,
        excit=excitation
    )

    # =============================================================================
    # 4. POSTPROCESSING - Frequency Response
    # =============================================================================
    t = np.linspace(0, discretization.req_simt, 
                    len(deflection_results.contact_point_deflection[0]))
    fs = 1 / (t[1] - t[0])

    # FFT of force (includes ramp and random components)
    force_fft = fft(deflection_results.force[10000:])

    # Process each contact point
    for i, contact_defl in enumerate(deflection_results.contact_point_deflection):
        deflection_fft = fft(contact_defl[10000:])
        freqs = fftfreq(len(t[10000:]), 1/fs)
        omega = 2 * np.pi * freqs
        
        # Calculate FRFs
        mobility = 1j * omega * deflection_fft / force_fft  # [m/s/N]
        receptance = deflection_fft / force_fft  # [m/N]

        # Filter to 0-2000 Hz
        mask = (freqs >= 0) & (freqs <= 2000)

        plt.figure(figsize=(10, 5))
        plt.subplot(2, 1, 1)
        plt.plot(freqs[mask], np.abs(mobility[mask]), 'b-', linewidth=1)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Mobility [m/Ns]')
        plt.yscale('log')
        plt.grid(True)
        plt.title(f'Mobility - {vel} m/s')

        plt.subplot(2, 1, 2)
        plt.plot(freqs[mask], np.abs(receptance[mask]), 'r-', linewidth=1)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Receptance [m/N]')
        plt.yscale('log')
        plt.grid(True)
        plt.title(f'Receptance - {vel} m/s')

        plt.suptitle(f'Contact Point {i+1} - {vel} m/s')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(str(output_dir / f'mobility_receptance_v{vel:03d}_wheel{i+1}.png'), dpi=300, bbox_inches='tight')
        plt.close()

    # Optional: Clear memory
    plt.close('all')

# 4.1 Plot deflection over time
deflection = np.transpose(deflection_results.deflection)
deflection = deflection[:, :deflection.shape[1] // 2]  # Take only the rail deflection part, drop sleeper part
resp.plotMatrix(
    deflection      = deflection, 
    track           = track,
    simulation_time = discretization.req_simt,
)


# # 4.2 Calculate frequency response at excitation point
# response = resp(results = deflection_results)

# # 4.3 Plot both mobility and receptance in two subplots
# resp.plot_mobility_receptance(
#     freq=response.freq,
#     mob=response.mob,
#     rez=response.rez,
#     title=f'Frequency Response - {vel} m/s',
#     x_label='Frequency [Hz]',
#     mob_label='Mobility [m/Ns]',
#     rez_label='Receptance [m/N]',
#     colors=['b', 'r'],
#     plot_type='loglog',
# )

# # 4.4 Calculate Track Decay Rate (TDR)
# tdr = TDR(results = deflection_results)

# # 4.5 Plot Track Decay Rate (TDR)
# resp.plot([(tdr.freq, tdr.tdr)],
#     # ['SimplePeriodicBallastedSingleRailTrack'],
#     title='Track-Decay-Rate',
#     x_label='f [Hz]',
#     y_label='TDR [dB/m]',
#     plot_type='loglog')