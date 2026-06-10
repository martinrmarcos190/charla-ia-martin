# embeddings_similarity.py
# Demo: convertir frases en vectores y medir similitud coseno.
# Modelo: sentence-transformers/all-MiniLM-L6-v2 (~80 MB, corre en CPU,
# embeddings de 384 dimensiones).
# Docs: https://www.sbert.net/
# Bloque 4 (~3 min).

from sentence_transformers import SentenceTransformer
import numpy as np

# La primera ejecución descarga el modelo y lo cachea en ~/.cache/.
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

frases = [
    "El perro corre por el parque.",
    "El gato duerme en el sillón.",
    "Factura electrónica AFIP comprobante tipo A.",
]

# encode() devuelve un array (N, 384). Normalizamos para que el producto
# punto = similitud coseno directamente.
emb = model.encode(frases, normalize_embeddings=True)
print("Shape del embedding:", emb.shape)

# Similitud coseno como producto punto entre vectores normalizados.
sim = emb @ emb.T

print("\nMatriz de similitud coseno:")
header = " | ".join(f"frase {i}" for i in range(len(frases)))
print(f"{'':40}{header}")
for i, f in enumerate(frases):
    fila = "  ".join(f"{x:+.3f}" for x in sim[i])
    print(f"frase {i}: {f[:38]:38}  {fila}")

# Lectura esperada: los pares de mascotas (0,1) dan score alto;
# cualquiera vs AFIP (2) da score bajo. La geometría = el significado.
