import math

d_s = 0.6
# E   = 210e11  # Nordborg elasticity modulus
E   = 210e9
Iyr = 3038.30e-8
# Izr = 512.30e-8
# Itr = 209.20e-8
# Ipr = 3550.60e-8
B   = E * Iyr
m   = 60.2  # rail mass per unit length
v = [25, 60, 80]  # velocities to simulate [m/s]

f_PPF = math.pi/(2*d_s**2)*math.sqrt(B/m)
print(f"Predicted PPF frequency: {f_PPF:.2f} Hz")

f_SPF = [vi/d_s for vi in v]
for vi, fsi in zip(v, f_SPF):
    print(f"Velocity: {vi} m/s -> Predicted SPF frequency: {fsi:.2f} Hz")