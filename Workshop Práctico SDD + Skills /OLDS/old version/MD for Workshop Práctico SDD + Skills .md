# Taller práctico (Clase 3): Spec-Driven Development + Claude Skills para MLOps — 150 min

## TL;DR
- Materiales completos y verificados contra documentación oficial de mediados de 2026: Spec Kit v0.8.18 (29-may-2026) con comandos `/speckit.*`, Claude Code con instalador nativo, Skills (SKILL.md), MCP Python SDK `mcp` 1.27.x, y `uv`/`uvx` de Astral.
- Los comandos de Spec Kit cambiaron de nombre: hoy son `/speckit.constitution → /speckit.specify → /speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.analyze → /speckit.implement`, y el flag de init es `--integration claude` (el viejo `--ai` quedó deprecado).
- El MCP custom se hace con el SDK OFICIAL (`from mcp.server.fastmcp import FastMCP`, `@mcp.tool()`, `mcp.run(transport="stdio")`), registrado con `claude mcp add nombre -- uv run server.py`.

## Key Findings (estado verificado a junio 2026)

**Spec Kit (github/spec-kit).** Instalación con uv: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` (persistente) o uso efímero `uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT>`. La última release es 0.8.18 (29-may-2026), con 0.9.0 en desarrollo. Init en proyecto con Claude: `specify init <nombre> --integration claude` o en directorio actual `specify init . --integration claude`. El flag `--ai` quedó deprecado en favor de `--integration` (changelog #2218). Verificación: `specify check` y `specify version`; upgrade: `specify self upgrade`. Los slash-commands se instalan en `.claude/commands/` y el flujo es: `/speckit.constitution`, `/speckit.specify`, `/speckit.clarify` (opcional), `/speckit.plan`, `/speckit.tasks`, `/speckit.checklist` (opcional), `/speckit.analyze` (opcional), `/speckit.implement`. La constitución vive en `.specify/memory/constitution.md`; los artefactos por feature en `specs/<N>-<feature>/`.

**Claude Code.** Método recomendado por Anthropic (anunciado oct-2025): instalador nativo, sin Node. La vía npm hoy está deprecada — Anthropic se movió enteramente al instalador nativo para macOS, Linux y Windows, y el viejo `npm install -g @anthropic-ai/claude-code` quedó como método legado (reseña de Augment Code, abril 2026). macOS/Linux: `curl -fsSL https://claude.ai/install.sh | bash`; Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`. Alternativa npm (todavía soportada, requiere Node.js 18+): `npm install -g @anthropic-ai/claude-code` (nunca con sudo). El binario nativo queda en `~/.local/bin/claude` y se autoactualiza. Verificación: `claude --version` y `claude doctor`. Autenticación: al correr `claude` por primera vez abre el navegador (OAuth) — sirve Pro/Max/Team/Enterprise; para CI se usa `ANTHROPIC_API_KEY`. Primer arranque en un repo: `/init` genera el `CLAUDE.md`.

**Skills (Agent Skills).** Una Skill es una carpeta con un `SKILL.md` que arranca con frontmatter YAML; los campos requeridos son `name` (máximo 64 caracteres, minúsculas/números/guiones solamente) y `description` (máximo 1024 caracteres, no vacío, sin etiquetas XML, escrito en tercera persona, qué hace y cuándo usarla) — per Claude API Docs, *Skill authoring best practices*: *"name: Maximum 64 characters, lowercase letters/numbers/hyphens only... description: Maximum 1024 characters, non-empty, no XML tags."* Progressive disclosure de 3 niveles: en arranque solo se cargan name+description al system prompt; el cuerpo se lee cuando la tarea matchea; los archivos de referencia (REFERENCE.md, scripts/, references/, assets/) solo cuando se necesitan. Recomendación oficial textual (Claude API Docs, best-practices): *"Keep SKILL.md body under 500 lines for optimal performance. If your content exceeds this, split it into separate files using the progressive disclosure patterns described earlier."* Ubicaciones en Claude Code: personal `~/.claude/skills/`, proyecto `.claude/skills/`, o vía plugins. Los "custom commands" se fusionaron con Skills — per Claude Code Docs: *"Custom commands have been merged into skills. A file at .claude/commands/deploy.md and a skill at .claude/skills/deploy/SKILL.md both create /deploy and work the same way."* Detección en caliente, cita textual de Claude Code Docs: *"Adding, editing, or removing a skill under ~/.claude/skills/... takes effect within the current session without restarting. Creating a top-level skills directory that did not exist when the session started requires restarting Claude Code so the new directory can be watched."* (o `/reload-skills`). Campos opcionales del frontmatter: `allowed-tools`, `disable-model-invocation`.

**MCP (Model Context Protocol).** SDK oficial Python: paquete `mcp` (la 1.27.0 fue *"Released: Apr 2, 2026"* según PyPI y la última es 1.27.1 según Libraries.io; el SDK *"implements the full MCP specification"* en su revisión 2025-11-25, per modelcontextprotocol/python-sdk releases: *"This release brings us up to speed with the latest MCP spec 2025-11-25"*). Requiere Python ≥3.10 y figura en PyPI como *"Development Status :: 4 - Beta"* con *"Requires: Python >=3.10"*. Setup oficial con uv: `uv init <dir>`, `uv venv`, `source .venv/bin/activate`, `uv add "mcp[cli]" httpx`. Import: `from mcp.server.fastmcp import FastMCP`. Tool con decorador `@mcp.tool()` (con paréntesis). Transportes: stdio (local, mismo árbol de proceso) y streamable-http (red). Para Claude Code se usa stdio: `mcp.run(transport="stdio")`. Gotcha crítico verificado: en stdio NUNCA escribir a stdout (`print()` corrompe el JSON-RPC); usar `print(..., file=sys.stderr)` o `logging`. Registro: `claude mcp add my-server -- uv run server.py` (scope local por defecto) o `--scope project` para compartir vía `.mcp.json`. Verificación: `claude mcp list` y, dentro de sesión, `/mcp`.

**uv/uvx (Astral).** Instalación: `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux) o `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows). `uvx` es alias de `uv tool run` (ejecuta herramientas en entornos efímeros). Verificación: `uv --version`. Reiniciar la terminal después de instalar para tomar el PATH.

---

## Details

A continuación, las 4 partes del entregable. Todo el texto destinado a participantes y facilitador va en español rioplatense (voseo).

### PARTE 1 — MATERIAL PREVIO (documento autocontenido para participantes)

#### 1.A — SPEC PARA CLAUDE (para generar el .md de material previo)

> **Spec: "Generá el material previo del taller de SDD + Skills"**
>
> Sos un asistente técnico. Generá un único archivo Markdown autocontenido llamado `material-previo.md`, en español rioplatense (voseo), para MLOps con base en clásico ML/infra, cómodos con terminal, Python, Git y Docker, principiantes en agentes y usuarios básicos de Claude Code. NO expliques redes neuronales ni transformers en profundidad (eso ya se vio en Clase 1); solo enlazá videos de referencia. El documento debe tener estas secciones, en este orden:
> 1. **Qué es SDD y por qué** — explicá que el "vibe coding" no escala (el código generado "parece bien pero no anda", pierde la intención); la spec como única fuente de verdad; SDD como "Infrastructure-as-Code para el código". Máx. 400 palabras.
> 2. **Qué es Spec Kit** — toolkit open-source de GitHub que materializa SDD; CLI `specify`; flujo constitution→specify→plan→tasks→implement. Máx. 250 palabras.
> 3. **Instalación y verificación del entorno** — comandos EXACTOS para: Python ≥3.11, `uv`/`uvx`, Spec Kit, Claude Code, Git, Docker. Incluí un checklist "entorno listo" con comandos de verificación y su salida esperada.
> 4. **Refresher mínimo de Flask + SQLite** — lo justo para no trabarse: un `app.py` con un GET y un POST contra SQLite usando el módulo `sqlite3` de la stdlib; cómo correrlo; cómo pegarle con `curl`.
> 5. **Referencias en video y docs** — links a 3blue1brown (redes neuronales, transformers, atención, LLMs) y a la documentación oficial.
>
> Requisitos de formato: usá bloques de código con el lenguaje indicado; no inventes comandos; cada comando debe ser copy-paste. Cerrá con el checklist marcable `[ ]`.

#### 1.B — CONTENIDO REAL DEL MATERIAL PREVIO (texto ya escrito)

**# Material previo — Taller de Spec-Driven Development + Claude Skills**

**## 1. ¿Qué es SDD y por qué te va a importar?**

Cuando le tirás un prompt suelto a un agente ("hacéme una API de inventario") pasa lo de siempre: el código *parece* correcto, pero no compila, o resuelve otra cosa, o elige un stack que no es el tuyo. A eso se le dice **vibe coding**, y está bien para un prototipo descartable, pero no escala a software serio. El problema no es la capacidad del modelo: es que lo tratamos como buscador cuando en realidad es un programador de a pares muy literal que necesita instrucciones sin ambigüedad.

**Spec-Driven Development (SDD)** da vuelta la jerarquía: en vez de que la spec sirva al código, el código sirve a la spec. La especificación es la **única fuente de verdad** (source of truth) y el código pasa a ser el output que se regenera. Para un MLOps esto es familiar: es **Infrastructure-as-Code, pero para el código**. Igual que no editás un servidor a mano sino que cambiás el Terraform y reaplicás, en SDD no parcheás el código: cambiás la spec y regenerás. Debuggear es arreglar la spec; refactorizar es reescribir para mayor claridad de la spec.

**## 2. ¿Qué es Spec Kit?**

**Spec Kit** es el toolkit open-source de GitHub que materializa SDD para agentes de código (Claude Code, Copilot, Gemini, etc.). Trae una CLI llamada `specify` que bootstrapea tu repo con plantillas y *slash-commands*. El flujo tiene fases con checkpoints: primero una **constitución** (principios no negociables del proyecto), después **specify** (el qué y el porqué), **plan** (el cómo técnico), **tasks** (desglose accionable) e **implement** (construcción). Vos manejás el volante (steering); el agente escribe.

**## 3. Instalación y verificación del entorno**

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

**## 4. Refresher mínimo de Flask + SQLite**

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

**## 5. Referencias (video y docs)**

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

---

### PARTE 2 — GUION MINUTO A MINUTO POR BLOQUE (150 min en vivo)

> Reparto: Bloque 0 (apertura) 10 min · Bloque 1 (Fundamentos SDD) 25 min · Bloque 2 (Setup hands-on) 25 min · Bloque 3 (Práctica guiada flujo completo) 45 min · Bloque 4 (Skill con SDD + MCP) 35 min · Bloque 5 (Reflexión y cierre) 10 min. Total: 150 min.

**BLOQUE 0 — Apertura (0:00–0:10)**
- 0:00–0:03 — Facilitador dice: "Bienvenidos a la Clase 3. En las clases 1 y 2 vimos el puente de ML clásico a LLMs/agentes, vibe coding vs SDD, MCP como USB-C para agentes y Skills como carpetas con procedimientos. Hoy lo construimos end-to-end." Hace: comparte pantalla, muestra agenda.
- 0:03–0:08 — Facilitador hace: pide que todos abran terminal y corran el checklist del material previo (`uv --version`, `claude --version`, `specify check`). Participantes tipean esos comandos.
- 0:08–0:10 — Facilitador resuelve dudas rápidas de entorno; quien tenga rojo, lo emparejamos con troubleshooting (ver apéndice 4.G).

**BLOQUE 1 — Fundamentos de SDD (0:10–0:35)**
- 0:10–0:13 — Dice: recap de "spec gobierna, código es output"; analogía IaC.
- 0:13–0:23 — Hace: presenta la HTML del Bloque 1 (generada con la spec del apéndice 4.A), recorre Spec Kit en detalle: constitution→specify→clarify→plan→tasks→analyze→implement; muestra dónde viven los artefactos (`.specify/memory/constitution.md`, `specs/<N>-<feature>/`).
- 0:23–0:33 — Dice: cómo adaptar el flujo SDD a cada empresa (constitución propia, gates de calidad propios). Participantes: anotan qué reglas pondrían en su constitución.
- 0:33–0:35 — Cierre del bloque y transición al setup.

**BLOQUE 2 — Setup técnico hands-on (0:35–1:00)**
- 0:35–0:38 — Dice: "Ahora cada uno arma su repo." Muestra la HTML del Bloque 2.
- 0:38–0:45 — Hace/Participantes tipean:
```bash
mkdir taller-sdd && cd taller-sdd
git init
claude            # primera vez: autenticar en navegador
# dentro de Claude Code:
/init
```
- 0:45–0:55 — Participantes tipean (instalar Spec Kit en el repo):
```bash
specify init . --integration claude
```
Después, dentro de Claude Code, tipean `/` y confirman que aparecen los `/speckit.*`.
- 0:55–1:00 — Verificación grupal: `ls .specify/ .claude/commands/`. Troubleshooting de los que no ven los comandos (reiniciar Claude Code, carpeta correcta).

**BLOQUE 3 — Práctica guiada: flujo completo (1:00–1:45)**
- 1:00–1:05 — Dice: entrega el `.md` del problema (Parte 4.B). Pide: "Primero ESTIMÁ cuánto tardarías a mano en levantar la DB + Flask + endpoints + tests con curl. Anotá tu número." Participantes: escriben su estimación.
- 1:05–1:08 — Dice: "Ahora se lo damos a Claude Code vía SDD."
- 1:08–1:15 — Participantes tipean la constitución:
```
/speckit.constitution Proyecto local y simple. Solo stdlib + Flask. SQLite con el módulo sqlite3. Sin auth. Tests con curl. Código documentado.
```
- 1:15–1:25 — `/speckit.specify` pegando el contenido del `.md` del problema; luego `/speckit.clarify` para cerrar ambigüedades.
- 1:25–1:32 — `/speckit.plan` (indicando Flask + sqlite3 stdlib) y `/speckit.tasks`.
- 1:32–1:33 — `/speckit.analyze` (gate de consistencia).
- 1:33–1:42 — `/speckit.implement`. Mientras corre, el facilitador explica qué está pasando.
- 1:42–1:45 — Participantes prueban con curl los endpoints y comparan tiempo real vs su estimación a mano. Dice: "¿Quién tardó menos? ¿Qué parte les sorprendió?"

**BLOQUE 4 — Construcción de una Skill con SDD + MCP (1:45–2:20)**
- 1:45–1:48 — Dice: "Ahora levantamos un MCP propio que le pega a los endpoints de la DB, y vía specs creamos una Skill que conecta todo." Muestra el objetivo.
- 1:48–1:58 — Participantes crean el MCP server mínimo (Parte 4.C). Tipean:
```bash
uv init mcp-items && cd mcp-items
uv venv && source .venv/bin/activate
uv add "mcp[cli]" httpx
# pegan server.py (apéndice 4.C)
```
- 1:58–2:03 — Registran el MCP en Claude Code:
```bash
claude mcp add items-api -- uv run server.py
claude mcp list
# dentro de Claude Code: /mcp
```
- 2:03–2:15 — Vía SDD crean la Skill (Parte 4.D): corren `/speckit.specify` con la spec de la Skill, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`. Resultado: `.claude/skills/items-ops/SKILL.md`.
- 2:15–2:20 — Prueban la Skill: le piden a Claude Code "listá los items y agregá uno"; Claude usa la Skill + las tools del MCP. Verifican con curl.

**BLOQUE 5 — Reflexión y extensión (2:20–2:30)**
- 2:20–2:25 — Dice: muestra la HTML del Bloque 5: Skills + MCPs + imaginación = construís cualquier cosa. Da los 2–3 ejemplos de Skills MLOps.
- 2:25–2:30 — Dice: el concepto central — "diseñá tu propio SDD basado en Skills": encodear specify/plan/tasks/implement como Skills a medida del stack del equipo. Cierre y próximos pasos.

---

### PARTE 3 — ESQUEMA DE SLIDES (outline del taller)

1. Portada: "Clase 3 — SDD + Skills, hands-on".
2. Recap Clases 1–2 (1 slide): ML→LLMs→agentes; vibe vs SDD; MCP=conectividad, Skills=procedimiento.
3. Agenda y reparto de bloques (150 min).
4. Bloque 1 — Qué es SDD (spec = fuente de verdad; IaC para el código).
5. Bloque 1 — Spec Kit en detalle (constitution→specify→clarify→plan→tasks→analyze→implement).
6. Bloque 1 — Dónde viven los artefactos (.specify/, specs/).
7. Bloque 1 — Adaptar SDD a tu empresa (constitución + gates propios).
8. Bloque 2 — Setup: instalar Claude Code, crear repo, `/init`.
9. Bloque 2 — Instalar Spec Kit en el repo (`specify init . --integration claude`).
10. Bloque 3 — El problema (DB + Flask + GET/POST + curl); estimá a mano.
11. Bloque 3 — El flujo SDD completo en vivo.
12. Bloque 3 — Comparación: SDD vs vibe coding (tiempo, calidad).
13. Bloque 4 — MCP custom mínimo (FastMCP oficial, stdio).
14. Bloque 4 — Registrar el MCP (`claude mcp add`).
15. Bloque 4 — Crear la Skill con SDD (SKILL.md + estructura).
16. Bloque 5 — Skills + MCPs + imaginación.
17. Bloque 5 — Ejemplos de Skills MLOps.
18. Bloque 5 — "Diseñá tu propio SDD basado en Skills".
19. Cierre / Q&A / próximos pasos.

---

### PARTE 4 — APÉNDICE TÉCNICO (specs, comandos y código verificados)

#### 4.A — SPECS PARA CLAUDE CODE (presentaciones HTML)

**Spec Bloque 1 (HTML — Fundamentos de SDD):**
> Generá una presentación HTML autocontenida (un solo archivo `bloque1.html`, sin dependencias externas, que abra en Chrome), en español rioplatense, con navegación por teclado (flechas) entre slides. Tema oscuro, tipografía grande, apta para compartir pantalla. Contenido: (1) Qué es SDD y por qué (spec como fuente de verdad, vibe coding no escala, analogía IaC para el código); (2) Spec Kit en detalle: explicá cada comando del flujo `/speckit.constitution`, `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.analyze`, `/speckit.checklist`, `/speckit.implement`, qué artefacto produce cada uno y dónde vive (`.specify/memory/constitution.md`, `specs/<N>-<feature>/spec.md|plan.md|tasks.md`); (3) Cómo adaptar el flujo SDD a cada empresa (constitución propia, gates de calidad, convenciones de stack). Incluí diagramas con HTML/CSS (sin imágenes externas). Pie de cada slide con el número y el total.

**Spec Bloque 2 (HTML — Setup técnico hands-on):**
> Generá `bloque2.html` autocontenida (Chrome, navegación por flechas, tema oscuro), en español rioplatense, mostrando paso a paso: (1) instalar Claude Code con el instalador nativo (`curl -fsSL https://claude.ai/install.sh | bash`) y alternativa npm (`npm install -g @anthropic-ai/claude-code`, Node 18+, aclarando que npm es legado), verificar con `claude --version`/`claude doctor`, autenticar; (2) crear el repo (`mkdir`, `git init`, `claude`, `/init`); (3) instalar Spec Kit en el repo (`specify init . --integration claude`) y confirmar los `/speckit.*`. Cada slide con un bloque de código copy-paste resaltado y la "salida esperada". Última slide: checklist de verificación.

**Spec Bloque 5 (HTML — Reflexión y extensión):**
> Generá `bloque5.html` autocontenida (Chrome, navegación por flechas, tema oscuro), en español rioplatense, que argumente: (1) Skills + MCPs + imaginación = podés construir casi cualquier integración; MCP aporta conectividad (las tools), Skills aportan el procedimiento (cómo usarlas bien); (2) 2–3 ejemplos de Skills útiles para MLOps; (3) el concepto central "diseñá tu propio SDD basado en Skills": cómo encodear el flujo specify/plan/tasks/implement como Skills a medida del stack del equipo (cada fase es un SKILL.md con su procedimiento, sus referencias y sus scripts). Cerrá con un llamado a la acción.

#### 4.B — EL `.md` DEL PROBLEMA (Bloque 3, sin mencionar a Claude)

**# Problema: API local de inventario de modelos**

**## Contexto**
Necesitás un servicio local mínimo para registrar artefactos de modelos en un inventario. Todo corre en tu máquina, sin nube, sin auth.

**## Objetivo**
Levantar una base de datos local y un servidor Flask con endpoints GET y POST, y probarlos con `curl`.

**## Stack obligatorio**
- Python 3.11+, Flask, módulo `sqlite3` de la stdlib (sin ORM).
- Un solo archivo `app.py`. Base `inventory.db` creada automáticamente.

**## Modelo de datos**
Tabla `models`:
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `name` TEXT NOT NULL
- `framework` TEXT NOT NULL (ej. "pytorch", "sklearn")
- `accuracy` REAL
- `created_at` TEXT (timestamp ISO)

**## Endpoints**
1. `GET /models` → lista todos los modelos (JSON array).
2. `GET /models/<id>` → un modelo por id (404 si no existe).
3. `POST /models` → crea un modelo. Body JSON: `{"name","framework","accuracy"}`. Setea `created_at` en el server. Responde 201 con `{"id": <nuevo_id>}`.
4. `GET /health` → `{"status":"ok"}`.

**## Datos de ejemplo (seed)**
Al iniciar, si la tabla está vacía, insertar:
- `{"name":"resnet50","framework":"pytorch","accuracy":0.76}`
- `{"name":"xgb-churn","framework":"sklearn","accuracy":0.88}`

**## Criterios de aceptación**
- `GET /health` responde `{"status":"ok"}`.
- `GET /models` devuelve al menos los 2 seeds.
- `POST /models` con body válido crea y devuelve un id; un segundo `GET /models` lo incluye.
- `GET /models/<id>` inexistente devuelve 404.
- `POST /models` sin campos requeridos devuelve 400.
- El server corre en `http://127.0.0.1:5000`.

**## Tu tarea (antes de automatizar)**
Estimá cuánto tardarías en hacer TODO esto a mano (DB + server + 4 endpoints + seed + pruebas curl). Anotá el número en minutos. Después lo comparás.

**## Pruebas con curl (definición de hecho)**
```bash
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/models
curl -X POST http://127.0.0.1:5000/models -H "Content-Type: application/json" \
  -d '{"name":"bert-base","framework":"pytorch","accuracy":0.91}'
curl http://127.0.0.1:5000/models/1
```

#### 4.C — CÓDIGO DEL MCP SERVER MÍNIMO (SDK oficial, verificado)

Verificado contra el SDK oficial `mcp` (1.27.x, la 1.27.0 lanzada 2-abr-2026, Python ≥3.10) y la guía oficial modelcontextprotocol.io/docs/develop/build-server.

Setup:
```bash
uv init mcp-items && cd mcp-items
uv venv && source .venv/bin/activate
uv add "mcp[cli]" httpx
```

`server.py`:
```python
import logging
import sys

import httpx
from mcp.server.fastmcp import FastMCP

# IMPORTANTE (stdio): nunca escribir a stdout, corrompe el JSON-RPC.
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

mcp = FastMCP("items-api")
API_BASE = "http://127.0.0.1:5000"

@mcp.tool()
async def list_models() -> str:
    """Lista todos los modelos del inventario local."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/models", timeout=30.0)
        r.raise_for_status()
        return str(r.json())

@mcp.tool()
async def get_model(model_id: int) -> str:
    """Devuelve un modelo por id."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/models/{model_id}", timeout=30.0)
        if r.status_code == 404:
            return f"No existe el modelo {model_id}."
        r.raise_for_status()
        return str(r.json())

@mcp.tool()
async def add_model(name: str, framework: str, accuracy: float) -> str:
    """Crea un modelo nuevo en el inventario."""
    payload = {"name": name, "framework": framework, "accuracy": accuracy}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_BASE}/models", json=payload, timeout=30.0)
        r.raise_for_status()
        return str(r.json())

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Registro en Claude Code:
```bash
claude mcp add items-api -- uv run server.py
claude mcp list                 # debe aparecer items-api
# dentro de una sesión de Claude Code:
/mcp                            # muestra estado y cantidad de tools
```
Para compartir con el equipo (genera `.mcp.json` commiteable): agregá `--scope project`.

#### 4.D — LA SKILL CONSTRUIDA CON SDD (spec, pasos, artefacto final)

**Spec de la Skill (autosuficiente para que Claude genere todas las specs):**
> Quiero una Skill de Claude Code llamada `items-ops` que opere el inventario de modelos a través de las tools del MCP `items-api`. Generá vía SDD (specify/plan/tasks/implement) la Skill completa. La Skill debe: (1) explicar cuándo usarse (cuando el usuario pida listar, consultar o agregar modelos al inventario); (2) instruir a Claude a usar SIEMPRE los nombres calificados de las tools del MCP (`items-api:list_models`, `items-api:get_model`, `items-api:add_model`); (3) validar que `accuracy` esté entre 0 y 1 antes de un alta; (4) ante un alta, confirmar el id devuelto leyendo el modelo. El SKILL.md debe tener frontmatter YAML con `name: items-ops` y un `description` en tercera persona (máx 1024 caracteres) que diga qué hace y cuándo usarse. Cuerpo por debajo de 500 líneas. Ubicación: `.claude/skills/items-ops/SKILL.md`.

**Pasos (lo que hacen los participantes):**
1. `/speckit.specify` pegando la spec de arriba.
2. `/speckit.plan` (Claude Code, MCP `items-api`, sin dependencias extra).
3. `/speckit.tasks` y luego `/speckit.implement`.
4. Reiniciar Claude Code o correr `/reload-skills` si la carpeta de skills es nueva.

**Artefacto final esperado — estructura y `SKILL.md`:**
```
.claude/skills/items-ops/
└── SKILL.md
```
```markdown
---
name: items-ops
description: Opera el inventario de modelos (listar, consultar y dar de alta) a través del MCP items-api. Usar cuando el usuario pida ver, buscar o agregar modelos al inventario local.
---

# items-ops

## Cuándo usar
Usá esta skill cuando el usuario quiera listar modelos, consultar un modelo por id, o dar de alta un modelo en el inventario.

## Reglas
- Usá siempre los nombres calificados de las tools del MCP:
  - `items-api:list_models`
  - `items-api:get_model`
  - `items-api:add_model`
- Antes de un alta, validá que `accuracy` esté entre 0 y 1. Si no, pedí corrección.
- Después de un alta, confirmá el `id` devuelto llamando a `items-api:get_model`.

## Procedimiento
1. Identificá la intención (listar / consultar / alta).
2. Para alta: validá campos (`name`, `framework`, `accuracy`).
3. Ejecutá la tool correspondiente.
4. Mostrá el resultado de forma legible.
```

> Nota de buenas prácticas (docs oficiales de Skills): el uso de los nombres calificados `servidor:tool` es la recomendación explícita para evitar errores "tool not found" cuando hay varios MCP conectados.

#### 4.E — 2–3 EJEMPLOS DE SKILLS ÚTILES PARA MLOPS

1. **`run-training`** — captura el procedimiento reproducible de levantar un entrenamiento: comandos de entorno, variables, script de lanzamiento; queda commiteada como skill de proyecto y todos siguen la misma receta. (Esto refleja el patrón oficial `run-skill-generator` de Claude Code, que captura los comandos de install/env/launch que funcionaron y los commitea como skill por proyecto.)
2. **`data-drift-check`** — instruye a Claude a correr el chequeo de drift entre dataset de referencia y producción usando el script `scripts/drift.py` bundleado, e interpretar el reporte (script determinístico = confiabilidad, sin gastar contexto).
3. **`model-card`** — genera la model card de un artefacto siguiendo el template y las convenciones del equipo (referencia en `references/model-card-template.md`), tomando métricas del inventario vía el MCP.

#### 4.F — "DISEÑÁ TU PROPIO SDD BASADO EN SKILLS"

La idea de cierre: el flujo SDD (specify→plan→tasks→implement) no es sagrado ni fijo. Como una Skill es solo una carpeta con un SKILL.md que enseña un procedimiento con progressive disclosure, podés **encodear cada fase de tu SDD como una Skill a medida de tu stack**. Por ejemplo: una skill `mlops-specify` que sepa que tus specs siempre incluyen sección de datos, métricas objetivo y restricciones de latencia; una `mlops-plan` que imponga tu stack (Kubeflow, MLflow, tal registry); una `mlops-tasks` que genere tareas con tus convenciones de CI; una `mlops-implement` que conozca tus repos y patrones. MCP aporta la **conectividad** (tools hacia tus sistemas) y las Skills aportan el **procedimiento** (cómo se hace acá). Combinando ambos, tu equipo deja de usar un SDD genérico y pasa a tener su propio SDD, versionado en el repo y compartible vía plugins. Como dice la doc de Skills: *"MCP can provide tools and resources, while Skills package the playbook for using them well."*

#### 4.G — TROUBLESHOOTING DE ERRORES COMUNES DE SETUP

- **Python viejo / no encontrado:** verificá `python3 --version`. Si es <3.11, instalá uno nuevo (con `uv python install 3.12` podés gestionarlo). Spec Kit y el SDK de MCP requieren Python ≥3.10.
- **`uvx`/`uv` "command not found":** reabrí la terminal después de instalar (el instalador modifica tu perfil de shell). Si persiste, agregá `~/.local/bin` al PATH.
- **Claude Code "command not found":** tu shell no tomó el PATH; abrí una terminal nueva o `source ~/.zshrc`/`~/.bashrc`. El binario nativo queda en `~/.local/bin/claude`.
- **Node viejo para la instalación npm de Claude Code:** la vía npm (legada) requiere Node.js 18+; verificá `node -v`. Mejor usá el instalador nativo, que no depende de Node. Nunca instales con `sudo npm` (rompe permisos; el fix correcto es `nvm` o `npm config set prefix ~/.npm-global`).
- **Registro del MCP falla / 0 tools:** corré el server a mano para ver errores en stderr; revisá que no haya `print()` a stdout (corrompe el JSON-RPC). Los servers stdio descubren tools al inicio de sesión: si lo agregaste a mitad de sesión, abrí una sesión nueva. Verificá con `claude mcp list` y `/mcp`.
- **Spec Kit init: no aparecen los `/speckit.*`:** abriste la carpeta equivocada en Claude Code o no reiniciaste; confirmá con `ls .claude/commands/` y reiniciá Claude Code. Recordá usar `--integration claude` (no el viejo `--ai`).
- **Flask/SQLite gotchas:** "no such table" significa que no inicializaste la DB (corré `init_db()` antes del primer query); si el POST falla, verificá `-H "Content-Type: application/json"` en el curl; el server de desarrollo de Flask corre en el puerto 5000 — si está ocupado, cambialo.

## Recommendations
1. **Antes del taller:** mandá el material previo (Parte 1) con 3–4 días de anticipación y pediles que peguen el output del checklist en un canal. Quien no complete el checklist no debería empezar el Bloque 2 en vivo (pierde tiempo de todos).
2. **Día del taller:** generá las HTML de los Bloques 1, 2 y 5 con las specs (Parte 4.A) la noche anterior y revisalas, porque la generación puede variar.
3. **Pinneá versiones:** instalá Spec Kit pinneando a una release (`@v0.8.18`) para que todos vean los mismos comandos, ya que el proyecto se mueve rápido. Igual con el MCP SDK si querés reproducibilidad total (`uv add "mcp[cli]==1.27.1"`).
4. **Umbral de decisión:** si más del 20% del grupo tiene el entorno roto al minuto 8, corré el Bloque 2 como "setup asistido" extendido y recortá 10 min del Bloque 3 (estimación + 1 sola pasada de SDD).

## Caveats
- Spec Kit evoluciona rápido (0.8.18 estable a 29-may-2026, 0.9.0 en desarrollo): verificá `specify check` el día del taller y confirmá los nombres de comandos con `/` dentro de Claude Code.
- El SDK oficial `mcp` figura como "Development Status :: 4 - Beta" en PyPI; el código del 4.C usa solo lo estable (FastMCP + stdio). La numeración exacta de la última patch (1.27.0 vs 1.27.1) puede variar entre PyPI y Libraries.io según el día — pinneá la que verifiques.
- La instalación npm de Claude Code está deprecada pero todavía funciona; priorizá el instalador nativo en clase para evitar problemas de Node/PATH.
- Para Windows nativo, varios comandos difieren; recomendá WSL2 para uniformar.
- Los IDs/fechas de los videos de 3blue1brown se citan donde se confirmaron (capítulo 6 = `eMlx5fFNoYc`, 7-abr-2024); verificá los demás títulos en el canal oficial antes de publicar, ya que la serie a veces renumera capítulos.