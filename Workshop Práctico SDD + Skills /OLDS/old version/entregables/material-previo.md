# Material previo — Taller de Spec-Driven Development + Claude Skills

> **Para participantes.** Leelo y completá el checklist del final **antes** de la clase. Si llegás con el entorno verde, arrancamos directo con las manos en el teclado. Si llegás con algo roto, perdés tiempo tuyo y de todos.
> **Audiencia:** MLOps con base en ML clásico / infra, cómodos con terminal, Python, Git y Docker. Principiantes en agentes, usuarios básicos de Claude Code.

---

## 1. ¿Qué es SDD y por qué te va a importar?

Cuando le tirás un prompt suelto a un agente ("hacéme una API de inventario") pasa lo de siempre: el código *parece* correcto, pero no compila, o resuelve otra cosa, o elige un stack que no es el tuyo. A eso se le dice **vibe coding**, y está bien para un prototipo descartable, pero no escala a software serio. El problema no es la capacidad del modelo: es que lo tratamos como buscador cuando en realidad es un programador de a pares muy literal que necesita instrucciones sin ambigüedad.

**Spec-Driven Development (SDD)** da vuelta la jerarquía: en vez de que la spec sirva al código, el código sirve a la spec. La especificación es la **única fuente de verdad** (source of truth) y el código pasa a ser el output que se regenera. Para un MLOps esto es familiar: es **Infrastructure-as-Code, pero para el código**. Igual que no editás un servidor a mano sino que cambiás el Terraform y reaplicás, en SDD no parcheás el código: cambiás la spec y regenerás. Debuggear es arreglar la spec; refactorizar es reescribir para mayor claridad de la spec.

## 2. ¿Qué es Spec Kit?

**Spec Kit** es el toolkit open-source de GitHub que materializa SDD para agentes de código (Claude Code, Copilot, Gemini, etc.). Trae una CLI llamada `specify` que bootstrapea tu repo con plantillas y *slash-commands*. El flujo tiene fases con checkpoints: primero una **constitución** (principios no negociables del proyecto), después **specify** (el qué y el porqué), **plan** (el cómo técnico), **tasks** (desglose accionable) e **implement** (construcción). Vos manejás el volante (steering); el agente escribe.

## 3. Instalación y verificación del entorno

> Trabajá en macOS o Linux (en Windows, usá WSL2). Hacé cada paso y verificá antes de seguir.

**3.1. Python ≥ 3.11.** Verificá:
```bash
python3 --version   # esperado: Python 3.11.x o superior
```

**3.2. uv (gestor de entornos de Astral).**
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Cerrá y reabrí la terminal, después verificá:
uv --version        # esperado: uv 0.x.y (...)
```

**3.3. Git y Docker.**
```bash
git --version       # esperado: git version 2.30+
docker --version    # esperado: Docker version 2x.x
```

**3.4. Claude Code (instalador nativo, recomendado).**
```bash
curl -fsSL https://claude.ai/install.sh | bash
# Reabrí la terminal y verificá:
claude --version
claude doctor       # diagnóstico del entorno
```
La primera vez que corras `claude` dentro de un proyecto te va a abrir el navegador para loguearte (necesitás plan Pro/Max/Team/Enterprise).

> Alternativa npm (legada, todavía funciona): `npm install -g @anthropic-ai/claude-code` requiere Node.js 18+. **Nunca** la instales con `sudo`. Priorizá el instalador nativo, que no depende de Node.

**3.5. Spec Kit (CLI specify).**
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify check       # confirma que el CLI anda y qué agentes detecta
specify version
```

**3.6. Checklist "entorno listo"** (marcá todo antes de la clase):
- [ ] `python3 --version` ≥ 3.11
- [ ] `uv --version` responde
- [ ] `git --version` y `docker --version` responden
- [ ] `claude --version` responde y `claude doctor` no marca errores graves
- [ ] Me logueé en Claude Code (corrí `claude` una vez y autoricé en el navegador)
- [ ] `specify check` responde OK

## 4. Refresher mínimo de Flask + SQLite

Lo justo para no trabarte. Creá `app.py`:
```python
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB = "demo.db"

def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS items "
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)")
    con.commit(); con.close()

@app.get("/items")
def list_items():
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    rows = con.execute("SELECT id, name, price FROM items").fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])

@app.post("/items")
def add_item():
    data = request.get_json()
    con = sqlite3.connect(DB)
    cur = con.execute("INSERT INTO items (name, price) VALUES (?, ?)",
                      (data["name"], data["price"]))
    con.commit(); new_id = cur.lastrowid; con.close()
    return jsonify({"id": new_id}), 201

if __name__ == "__main__":
    init_db()
    app.run(port=5000, debug=True)
```
Corrélo y probá:
```bash
uv run --with flask app.py
# en otra terminal:
curl http://127.0.0.1:5000/items
curl -X POST http://127.0.0.1:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"GPU A100","price":12000}'
```

## 5. Referencias (video y docs)

Videos de 3blue1brown (Grant Sanderson) — para refrescar fundamentos visualmente:
- "But what is a Neural Network?" (Deep Learning, capítulo 1).
- "But what is a GPT? Visual intro to transformers" (capítulo 5).
- "Attention in transformers, step-by-step" (capítulo 6, video `eMlx5fFNoYc`, publicado 7-abr-2024).
- "Large Language Models explained briefly" (versión corta y accesible para quien tenga el tema como caja negra).

Documentación oficial:
- Spec Kit: github.com/github/spec-kit
- Claude Code: code.claude.com/docs
- Agent Skills: docs de Claude (Agent Skills overview) y el post de Anthropic Engineering "Equipping agents for the real world with Agent Skills".
- MCP: modelcontextprotocol.io y github.com/modelcontextprotocol/python-sdk
