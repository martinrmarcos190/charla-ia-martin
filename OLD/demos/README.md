# Demos — Fundamentos de IA

Cuatro demos self-contained para correr **en local**, sin claves de API, con dependencias mínimas. Probados con Python 3.11+.

## Dos formatos

- **`Fundamentos_de_IA_demos.ipynb`** — *recomendado para la clase.* Notebook con las 4 demos; corrés celda por celda y los plots se renderizan **inline**. Abrilo con `jupyter lab` / `jupyter notebook` o desde VS Code.
- **Scripts `.py` sueltos** — misma lógica, uno por demo, para correr desde la terminal (los plots abren ventana aparte).

## Setup único (en una venv limpia)

```bash
python -m venv .venv && source .venv/bin/activate
pip install tiktoken sentence-transformers matplotlib numpy
```

> **Importante:** la primera vez que se corre `embeddings_similarity.py`, `sentence-transformers` baja el modelo `all-MiniLM-L6-v2` (~80 MB). **Correlo una vez antes de la clase** para que el cacheo no rompa el flujo en vivo.

## Las demos

| Archivo | Bloque | Dura | Qué muestra |
|---|---|---|---|
| `gradient_descent.py` | 3 — Redes y backprop | ~3 min | Pelotita bajando una cuadrática por descenso de gradiente + loss vs iteración |
| `embeddings_similarity.py` | 4 — Embeddings | ~3 min | Tres frases → vectores 384-D → matriz de similitud coseno |
| `tokenization.py` | 5 — Transformers | ~2 min | Cómo BPE (tiktoken `o200k_base`) parte texto ES vs EN en subwords |
| `attention_viz.py` | 5 — Transformers | ~3 min | Heatmap ilustrativo de una matriz de atención |

## Cómo correrlas

**Notebook (recomendado):**

```bash
pip install jupyterlab           # si no lo tenés
jupyter lab Fundamentos_de_IA_demos.ipynb
```

Corré la celda de setup, después la **Demo 2 una vez** para cachear el modelo, y listo.

**Scripts sueltos:**

```bash
python demos/gradient_descent.py
python demos/embeddings_similarity.py
python demos/tokenization.py
python demos/attention_viz.py
```

Las que usan matplotlib (`gradient_descent.py`, `attention_viz.py`) abren una ventana; las otras dos imprimen en consola.

## Notas de timing

- Si vas corto de tiempo, **Demo 4 (`attention_viz.py`) es la salteable**.
- Los Bloques 3, 4 y 5 dependen más de sus demos que el resto.
