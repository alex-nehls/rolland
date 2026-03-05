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
from rolland.database.rail.db_rail  import UIC60, NORDBORG  # rail profiles
from rolland                        import SimplePeriodicBallastedSingleRailTrack
from rolland.excitation             import RandomForce
from rolland import(
    PMLRailDampVertic,
    DiscretizationEBBVerticConst,
    DeflectionEBBVertic)
from rolland.postprocessing import(
    Response as resp,
    TDR)
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import math
from scipy.fft  import fft, fftfreq
from pathlib    import Path


# =============================================================================
# 0. TESTING PARAMETERS
# =============================================================================
store_deflection    = False     # TODO: this is not implemented yet!
starting_position   = 80.0      # Starting position [m]
num_mount           = 400       # Number of discrete mounting positions
distance            = 0.6       # Distance between sleepers [m]
l_bound             = 40.0      # width of boundary domain
req_simt            = 1         # Required simulation time [s]
dt                  = 2.2e-5    # time step [s]
velocities          = [60]      # Velocities to simulate [m/s]
# velocities          = [25, 60, 80]      # Velocities to simulate [m/s]
# velocities          = np.arange(5, 101, 5)  # 5 to 100 m/s in 5 m/s steps
ramp_fraction       = 0.1       # fraction of total time for ramp up
force_amplitude     = 65000.0   # Force amplitude [N]
# compare_nordborg     = False     # Compare with Nordborg results


# =============================================================================
# 1. TRACK DEFINITION
# =============================================================================
# Create a ballasted single rail track model with periodic supports
track = SimplePeriodicBallastedSingleRailTrack(
    rail    = NORDBORG, # rail profile with parameters according to Nordborg paper
    # rail    = UIC60,   # UIC60 rail profile
    pad     = DiscrPad(
                sp = [300e6, 0],    # Pad Stiffness [N/m]
                dp = [18000, 0],    # Pad Damping [Ns/m]
                # eta_p = 0.15      # Pad loss factor [-]
    ),
    sleeper = Sleeper(ms=150),      # Sleeper mass [kg]
    ballast = Ballast(
                sb = [150e6, 0],    # Ballast stiffness [N/m]
                db = [48000, 0],    # Ballast damping [Ns/m]
                # eta_b = 0.4       # Ballast loss factor [-]
    ),
    num_mount   = num_mount,        # Number of discrete mounting positions
    distance    = distance          # Distance between sleepers [m]
)

ppf = math.pi/(2*distance**2) * math.sqrt(track.rail.E*track.rail.Iyr / track.rail.mr) # first pinned-pinned frequency	

# =============================================================================
# 2. SIMULATION SETUP
# =============================================================================
# Define boundary conditions (Perfectly Matched Layer absorbing boundary)
boundary = PMLRailDampVertic(l_bound = l_bound)  # width of boundary domain

# Output directory
output_dir = Path('mobility_plots')
output_dir.mkdir(exist_ok=True)

# clear mobility plots directory
for file in output_dir.glob('*.png'):
    os.remove(file)

# =============================================================================
# 3. VELOCITY SWEEP SIMULATION
# =============================================================================
for vel in velocities:
    print(f"Computing velocity: {vel} m/s ({vel*3.6:.1f} km/h)")
    
    # Define moving load excitation
    excitation = RandomForce(
        ramp_fraction   = ramp_fraction,
        x_excit         = [starting_position],
        # x_excit         = [starting_position,
        #                    starting_position + 2.5],
        velocity        = float(vel),
        force_amplitude = force_amplitude
    )

    # Discretize domain
    discretization = DiscretizationEBBVerticConst(
        dt          = dt,           # time step [s]
        req_simt    = req_simt,     # requested simulation time [s]
        track       = track,        
        bound       = boundary)

    # Solve for deflection
    deflection_results = DeflectionEBBVertic(
        store_deflection = store_deflection,
        discr            = discretization,
        excit            = excitation
    )

    # =============================================================================
    # 4. POSTPROCESSING - Frequency Response
    # =============================================================================
    t = np.linspace(0, req_simt, len(deflection_results.contact_point_deflection[0]))   # time array

    # cut the ramp part from the results to avoid transient effects in the FFT
    ramp_length = 10000
    
    # FFT of force, cut ramp part
    force_fft = fft(deflection_results.force[ramp_length:])

    # Process each contact point
    for i, deflection in enumerate(deflection_results.contact_point_deflection):

        # Fast Fourier Transform of deflection at contact point
        deflection_fft = fft(deflection[ramp_length:])  # FFT of deflection at contact point, cut ramp part
        freqs = fftfreq(len(t[ramp_length:]), dt)       # FFT sample frequencies
        omega = 2 * np.pi * freqs                       # FFT angular sample frequencies
        
        # Calculate FRFs
        mobility = 1j * omega * deflection_fft / force_fft  # [m/s/N]
        receptance = deflection_fft / force_fft             # [m/N]

        # Filter to 0-2000 Hz
        mask = (freqs >= 0) & (freqs <= 2000)

        # plot individual velocity
        plt.plot(freqs[mask], 20*np.log10(np.abs(receptance[mask])), linewidth=1)
        plt.xlabel('Frequenz [Hz]')
        plt.ylabel('Rezeptanz [m/N]')
        plt.title(f'Rezeptanz - {vel} m/s')
        plt.grid(True)
        plt.suptitle(f'Kontaktpunkt {i+1} - {vel} m/s')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(str(output_dir / f'mobility_receptance_v{vel:03d}_wheel{i+1}.png'), dpi=300, bbox_inches='tight')
        plt.close()

        # collect data for overall plot (only first contact point)
        all_receptance = [] # [vel, freq, mobility, receptance]
        if i == 0:
            with np.errstate(divide='ignore', invalid='ignore'):
                mobility_db = 20 * np.log10(np.abs(mobility[mask]))
                receptance_db = 20 * np.log10(np.abs(receptance[mask]))
                mobility_db[np.isneginf(mobility_db)] = -300        # Replace -inf with a large negative value
                receptance_db[np.isneginf(receptance_db)] = -300    # Replace -inf with a large negative value
            all_receptance.append((vel, freqs[mask], mobility_db, receptance_db))

        # overall plot for all velocities
        if vel == velocities[-1] and i == 0:
            plt.figure(figsize=(10, 5))
            for v, freq, mobility, receptance in all_receptance:
                plt.plot(freq, receptance, label=f'{v} m/s', linewidth=1)
                plt.xlabel('Frequenz [Hz]')
                plt.ylabel('Receptance [dB re m/N]')
                plt.grid(True)
                plt.legend()
                plt.tight_layout()
            plt.savefig(str(output_dir / 'receptance_all_velocities.png'), dpi=300, bbox_inches='tight')


            # Optional:
            # fetch Nordborg data for comparison
            with open('nordborg_data_sharp.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                frequencies = []
                receptances = []
                for row in csv_reader:
                    frequencies.append(float(str.replace(row[0], ',', '.')))
                    receptances.append(float(str.replace(row[1], ',', '.')))

            # Interpolate to equally spaced frequencies
            freq_interp = np.linspace(0, 2000, 2000)
            receptance_interp = np.interp(freq_interp, frequencies, receptances)

            plt.figure(figsize=(10, 5))
            plt.plot(freq_interp, receptance_interp, label='Vergleichsdaten (Nordborg)', linewidth=1)
            for v, freq, mobility, receptance in all_receptance:
                if v == 60:
                    plt.plot(freq, receptance, label=f'Simulation', linewidth=1)
            plt.xlabel('Frequenz [Hz]')
            plt.ylabel('Rezeptanz [dB re 1 m/N]')
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.savefig(str(output_dir / 'receptance_60_Nordborg.png'), dpi=300, bbox_inches='tight')

    # Optional: Clear memory
    plt.close('all')

    # # 4.1 Plot deflection over time
    # deflection = np.transpose(deflection_results.deflection)
    # deflection = deflection[:, :deflection.shape[1] // 2]  # Take only the rail deflection part, drop sleeper part
    # resp.plotMatrix(
    #     deflection      = deflection, 
    #     track           = track,
    #     simulation_time = discretization.req_simt,
    # )

    # 4.2 Calculate frequency response at excitation point
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