## harmonic frequencies ###

import math
d_s = 0.6
# E   = 210e11  # Nordborg elasticity modulus
E   = 210e9
Iyr = 3038.30e-8
# Izr = 512.30e-8
# Itr = 209.20e-8
# Ipr = 3550.60e-8
B   = E * Iyr
print(f"Bending stiffness B: {B:.2f} Nm^2")
m   = 60.2  # rail mass per unit length
v = [25, 60, 80]  # velocities to simulate [m/s]

f_PPF = math.pi/(2*d_s**2)*math.sqrt(B/m)
print(f"Predicted PPF frequency: {f_PPF:.2f} Hz")
f_SPF = [vi/d_s for vi in v]
for vi, fsi in zip(v, f_SPF):
    print(f"Velocity: {vi} m/s -> Predicted SPF frequency: {fsi:.2f} Hz")

### read in data from csv ###

# import csv
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np


# with open('C:/Users/Alex/repositories/rolland/nordborg_data_sharp.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=';')
#     frequencies = []
#     receptances = []
#     for row in csv_reader:
#         frequencies.append(float(str.replace(row[0], ',', '.')))
#         receptances.append(float(str.replace(row[1], ',', '.')))

# # Interpolate to equally spaced frequencies
# freq_interp = np.linspace(0, 2000, 2000)
# receptance_interp = np.interp(freq_interp, frequencies, receptances)

# # Plot the interpolated data
# plt.figure(figsize=(12, 6))
# plt.plot(freq_interp, receptance_interp, linewidth=1.5)
# plt.xlabel('Frequency [Hz]', fontsize=12)
# plt.ylabel('Receptance [m/N]', fontsize=12)
# plt.grid(True, alpha=0.3)
# plt.title('Interpolated Receptance vs Frequency', fontsize=14)
# plt.tight_layout()
# plt.show()








# df = pd.read_csv('C:/Users/Alex/repositories/rolland/nordborg_data.csv', sep=';', header=None)
# a = df.loc[:, 0]
# b = df.loc[:, 1]

# # a[137] = 1375

# ### plot data ###
# plt.figure(figsize=(10, 6))
# plt.plot(b, a, linewidth=1)
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('Receptance [m/N]')
# plt.yscale('log')
# plt.grid(True)
# plt.title('Receptance vs Frequency')
# plt.tight_layout()
# plt.show()


