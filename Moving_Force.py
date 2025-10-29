"""
Track Vibration Analysis using Rolland API.
Example simulation for quasistatic excitation of rail vibration.

This simulation is build using the following structure:
    1. Create a railway track model
    2. Apply excitation and boundary conditions
    3. Run a vibration simulation
    4. Analyze and plot the results
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

# 1. TRACK DEFINITION ----------------------------------------------------------
# Create a ballasted single rail track model with periodic supports
track = SimplePeriodicBallastedSingleRailTrack(
    rail    = UIC60,                # Standard UIC60 rail profile
    pad     = DiscrPad(
                sp = [180e6, 0],      # Stiffness properties [N/m]
                dp = [18000, 0]       # Damping properties [Ns/m]
    ),
    sleeper = Sleeper(ms=150),      # Sleeper mass [kg]
    ballast = Ballast(
                sb = [105e6, 0],      # Ballast stiffness [N/m]
                db = [48000, 0]       # Ballast damping [Ns/m]
    ),
    num_mount   = 60,               # Number of discrete mounting positions
    distance    = 0.6               # Distance between sleepers [m]
)

# 2. SIMULATION SETUP ---------------------------------------------------------
# Define boundary conditions (Perfectly Matched Layer absorbing boundary)
boundary    = PMLRailDampVertic(l_bound = 5.0)  # width of boundary domain

# Create output directory for plots
output_dir = Path('mobility_plots')
output_dir.mkdir(exist_ok=True)

# Velocity loop
# velocities = np.arange(5, 105, 5)  # 5 to 100 m/s in 5 m/s steps
velocities = [10]

for vel in velocities:
    print(f"Calculating for velocity {vel} m/s ({vel*3.6:.0f} km/h)")
    
    # Define excitation with current velocity
    excitation = ConstantForce(
        x_excit=[15.0],
        velocity=float(vel),
        force_amplitude=50000.0
    )

    # 3. DISCRETIZATION & SIMULATION ----------------------------------------------
    # Set up numerical discretization parameters
    discretization = DiscretizationEBBVerticConst(
        track = track,
        bound = boundary,
    )

    # Run the simulation and calculate deflection over time
    deflection_results = DeflectionEBBVertic(
        discr = discretization,
        excit = excitation
    )

    # 4. POSTPROCESSING & VISUALIZATION -------------------------------------------
    # 4.0 Calculate and plot mobility spectrum for each contact point
    t = np.linspace(0, discretization.req_simt, len(deflection_results.contact_point_deflection[0]))
    fs = 1/(t[1] - t[0])

    # Get FFT of force once (same for all wheels)
    force_time = deflection_results.force
    force_fft = fft(force_time)

    # Create and save plots for each wheel
    for i, contact_defl in enumerate(deflection_results.contact_point_deflection):
        # Perform FFT of deflection
        deflection_fft  = fft(contact_defl)
        freqs           = fftfreq(len(t), 1/fs)
        omega           = 2 * np.pi * freqs
        mobility        = 1j * omega * deflection_fft / force_fft
        receptance      = deflection_fft / force_fft

        # Filter for frequencies up to 2 kHz
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
# deflection = np.transpose(deflection_results.deflection)
# deflection = deflection[:, :deflection.shape[1] // 2]  # Take only the rail deflection part, drop sleeper part
# resp.plotMatrix(
#     deflection      = deflection, 
#     track           = track,
#     simulation_time = discretization.req_simt,
# )


# 4.2 Calculate frequency response at excitation point
response = resp(results = deflection_results)

# 4.3 Plot both mobility and receptance in two subplots
resp.plot_mobility_receptance(
    freq=response.freq,
    mob=response.mob,
    rez=response.rez,
    title=f'Frequency Response - {vel} m/s',
    x_label='Frequency [Hz]',
    mob_label='Mobility [m/Ns]',
    rez_label='Receptance [m/N]',
    colors=['b', 'r'],
    plot_type='loglog',
)

# 4.4 Calculate Track Decay Rate (TDR)
tdr = TDR(results = deflection_results)

# 4.5 Plot Track Decay Rate (TDR)
resp.plot([(tdr.freq, tdr.tdr)],
    # ['SimplePeriodicBallastedSingleRailTrack'],
    title='Track-Decay-Rate',
    x_label='f [Hz]',
    y_label='TDR [dB/m]',
    plot_type='loglog')