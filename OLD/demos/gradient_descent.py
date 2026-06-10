# gradient_descent.py
# Demo: descenso por gradiente sobre f(x) = (x - 3)^2 + 2.
# Muestra cómo "ajustar una perilla" para minimizar el error.
# Bloque 3 (~3 min).

import numpy as np
import matplotlib.pyplot as plt

# Función a minimizar: una cuadrática con mínimo en x=3, f=2.
def f(x):
    return (x - 3) ** 2 + 2

# Gradiente analítico: f'(x) = 2(x - 3).
def grad(x):
    return 2 * (x - 3)

# Hiperparámetros.
x = -4.0          # arrancamos lejos del mínimo
lr = 0.1          # learning rate (tamaño del pasito)
steps = 30        # cuántas iteraciones

# Historial para graficar.
xs, ys = [x], [f(x)]
for _ in range(steps):
    x = x - lr * grad(x)   # paso de descenso por gradiente
    xs.append(x)
    ys.append(f(x))

# Visualización.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Panel 1: la función y la trayectoria de la pelotita.
xx = np.linspace(-5, 8, 200)
ax1.plot(xx, f(xx), label="f(x) = (x-3)^2 + 2")
ax1.scatter(xs, ys, c="red", s=30, label="trayectoria")
ax1.set_title("Descenso por gradiente sobre f(x)")
ax1.set_xlabel("x (la 'perilla')"); ax1.set_ylabel("loss")
ax1.legend()

# Panel 2: la loss a lo largo de las iteraciones.
ax2.plot(ys, marker="o")
ax2.set_title("Loss vs iteración")
ax2.set_xlabel("iteración"); ax2.set_ylabel("loss")

plt.tight_layout()
plt.show()
