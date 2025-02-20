import numpy as np

# Gegebene Punktkoordinaten für Passpunkte
passpunkte = np.array([    [  1560.0,  30590.0, 494086.687, 5795436.910],
    [ 46900.0,  22530.0, 494043.548, 5795420.795],
    [ 23820.0,   2010.0, 494052.974, 5795450.206],
    [ 71890.0,   5450.0, 494013.342, 5795422.786],
    [ 35430.0,  34170.0, 494059.338, 5795416.599]
])


# Koordinaten des Neupunktes
neupunkt = [50.017, 19.810]  # y, x

# Anzahl der Passpunkte
N = passpunkte.shape[0]
A = np.zeros((2 * N, 4))
B = np.zeros((2 * N, 1))

# Gerade Zeilen für Y-Koordinaten
for i in range(N):
    A[2 * i, 0] = 1
    A[2 * i, 1] = 0
    A[2 * i, 2] = passpunkte[i, 0]
    A[2 * i, 3] = passpunkte[i, 1]
    B[2 * i, 0] = passpunkte[i, 2]

# Ungerade Zeilen für X-Koordinaten
for i in range(N):
    A[2 * i + 1, 0] = 0
    A[2 * i + 1, 1] = 1
    A[2 * i + 1, 2] = passpunkte[i, 1]
    A[2 * i + 1, 3] = -passpunkte[i, 0]
    B[2 * i + 1, 0] = passpunkte[i, 3]

# Berechnung der Transformationsparameter
Norm = np.transpose(A) @ A
Q = np.linalg.inv(Norm)
HW = Q @ np.transpose(A)
X = HW @ B  # X enthält die Transformationsparameter

# Berechnung der Restklaffungen
V = B - A @ X

# Berechnung von Standardabweichungen
# Gerade Zeilen (Y-Richtungen)
ys2 = sum(V[i, 0]**2 for i in range(0, 2 * N, 2))
sy = np.sqrt(ys2 / (N - 1))

# Ungerade Zeilen (X-Richtungen)
xs2 = sum(V[i, 0]**2 for i in range(1, 2 * N, 2))
sx = np.sqrt(xs2 / (N - 1))

# Mittlerer Punktfehler
mp = np.sqrt(sy**2 + sx**2)

# Transformierte Koordinaten des Neupunktes
Y_Neu = X[0] + neupunkt[0] * X[2] + neupunkt[1] * X[3]
X_Neu = X[1] + neupunkt[1] * X[2] - neupunkt[0] * X[3]

# Ausgabe der Ergebnisse
print("Transformationsparameter:")
print(f"  Ty = {X[0][0]:+.6f}")
print(f"  Tx = {X[1][0]:+.6f}")
print(f"  a (cos) = {X[2][0]:+.6f}")
print(f"  b (sin) = {X[3][0]:+.6f}")
print()
print(f"Restklaffungen (Residuen) in mm:")
for i in range(N):
    vy = -V[2 * i, 0] * 1000
    vx = -V[2 * i + 1, 0] * 1000
    print(f"  Punkt {i+1}: vy={vy:+.1f} mm, vx={vx:+.1f} mm")
print()
print(f"Mittlerer Punktfehler (mp): {mp:.3f} mm")
print()
# Berechnung des Maßstabs
s = np.sqrt(X[2][0]**2 + X[3][0]**2)
print(f"Maßstab (s): {s:.8f}")
print()
print("Transformierte Koordinaten des Neupunktes:")
print(f"  Y_Neu = {Y_Neu[0]:+.3f} m")
print(f"  X_Neu = {X_Neu[0]:+.3f} m")
