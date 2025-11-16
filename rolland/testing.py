### harmonic frequencies ###

# import math
# d_s = 0.6
# # E   = 210e11  # Nordborg elasticity modulus
# E   = 210e9
# Iyr = 3038.30e-8
# # Izr = 512.30e-8
# # Itr = 209.20e-8
# # Ipr = 3550.60e-8
# B   = E * Iyr
# m   = 60.2  # rail mass per unit length
# v = [25, 60, 80]  # velocities to simulate [m/s]

# f_PPF = math.pi/(2*d_s**2)*math.sqrt(B/m)
# print(f"Predicted PPF frequency: {f_PPF:.2f} Hz")
# f_SPF = [vi/d_s for vi in v]
# for vi, fsi in zip(v, f_SPF):
#     print(f"Velocity: {vi} m/s -> Predicted SPF frequency: {fsi:.2f} Hz")

### read in data from csv ###

import csv
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('C:/Users/Alex/repositories/rolland/nordborg_result.csv', sep=',', header=None)

plt.figure(figsize=(10, 6))
plt.plot(df.iloc[:, 0], df.iloc[:, 1], linewidth=1)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Receptance [m/N]')
plt.yscale('log')
plt.grid(True)
plt.title('Receptance vs Frequency')
plt.tight_layout()
plt.show()

# plt.figure(figsize=(10, 6))
# plt.plot(df.loc[:, 0], df.loc[:, 1], linewidth=1)
# a = df.loc[:, 0]
# b = df.loc[:, 1]
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('Receptance [m/N]')
# plt.yscale('log')
# plt.grid(True)
# plt.title('Receptance - 60 m/s')

# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.savefig('C:/Users/Alex/repositories/rolland/nordborg_receptance.png', dpi=300, bbox_inches='tight')