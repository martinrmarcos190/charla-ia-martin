# tokenization.py
# Demo: cómo tiktoken (el tokenizador BPE oficial de OpenAI) parte texto.
# Documentación: https://github.com/openai/tiktoken
# Bloque 5 (~2 min).

import tiktoken

# Encoding o200k_base es el usado por GPT-4o y modelos posteriores.
enc = tiktoken.get_encoding("o200k_base")

ejemplos = [
    "Hello, world!",
    "Hola, mundo, ¿cómo andás?",
    "MLOps developers love Docker images.",
    "Los desarrolladores MLOps aman las imágenes de Docker.",
]

for texto in ejemplos:
    ids = enc.encode(texto)
    # decode_single_token_bytes devuelve los bytes de cada token.
    pieces = [enc.decode_single_token_bytes(t).decode("utf-8", errors="replace")
              for t in ids]
    print(f"\nTexto:   {texto!r}")
    print(f"Tokens:  {pieces}")
    print(f"IDs:     {ids}")
    print(f"Total:   {len(ids)} tokens")
