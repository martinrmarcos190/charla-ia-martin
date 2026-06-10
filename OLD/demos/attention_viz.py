# attention_viz.py
# Demo: visualización simple de una matriz de atención sobre una frase.
# Para que sea didáctico y sin dependencias pesadas, construimos una
# matriz "a mano" que ilustra patrones típicos: pronombre -> sustantivo,
# verbo -> sujeto, palabras temáticamente relacionadas.
# Bloque 5 (~3 min).

import numpy as np
import matplotlib.pyplot as plt

tokens = ["El", "modelo", "ajusta", "la", "función",
          "de", "loss", "con", "el", "gradiente", "."]
n = len(tokens)

# Matriz random suave + refuerzos en relaciones específicas.
rng = np.random.default_rng(42)
A = rng.uniform(0.0, 0.15, size=(n, n))

# Refuerzos didácticos (fila = quien atiende, columna = a quién):
A[2, 1] += 0.7   # 'ajusta' -> 'modelo'  (verbo -> sujeto)
A[4, 6] += 0.7   # 'función' -> 'loss'
A[6, 4] += 0.5   # 'loss' -> 'función'
A[9, 4] += 0.6   # 'gradiente' -> 'función'
A[9, 6] += 0.5   # 'gradiente' -> 'loss'
A[3, 4] += 0.6   # 'la' -> 'función' (artículo -> sustantivo)
A[8, 9] += 0.6   # 'el' -> 'gradiente'

# Cada fila suma 1 (softmax-like), como en atención real.
A = A / A.sum(axis=1, keepdims=True)

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(A, cmap="viridis")
ax.set_xticks(range(n)); ax.set_xticklabels(tokens, rotation=45, ha="right")
ax.set_yticks(range(n)); ax.set_yticklabels(tokens)
ax.set_xlabel("Atendido (key)")
ax.set_ylabel("Atendiendo (query)")
ax.set_title("Matriz de atención (ilustrativa)\nfila = token que mira, columna = token mirado")
fig.colorbar(im, ax=ax, fraction=0.046)
plt.tight_layout()
plt.show()
