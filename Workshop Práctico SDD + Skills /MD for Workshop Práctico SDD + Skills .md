# Taller práctico (Clase 3): Spec-Driven Development + Claude Skills — 150 min · edición DUAL-TRACK (Claude Code/Spec Kit + Kiro)

## TL;DR
- Materiales completos y verificados contra documentación oficial de mediados de 2026, en **dos caminos**: **Camino A** = Claude Code + Spec Kit; **Camino B** = Kiro (AWS). El grupo puede venir mixto y el taller funciona igual con cualquiera.
- **La idea de fondo (anti lock-in):** SDD, MCP y Skills resultaron ser **estándares abiertos**. El `.md` del problema, el servidor MCP en Python y el `SKILL.md` son **idénticos** en las dos herramientas; solo cambia *dónde se registran*, no *qué son*.
- **Camino A:** Spec Kit v0.8.18 (29-may-2026), comandos `/speckit.constitution → specify → clarify → plan → tasks → analyze → implement`, init con `specify init . --integration claude` (el viejo `--ai` quedó deprecado). Claude Code con instalador nativo. MCP con `claude mcp add`. Skills en `.claude/skills/`.
- **Camino B:** Kiro trae **SDD nativo** (no instalás Spec Kit): un *Feature Spec* genera `requirements.md → design.md → tasks.md` en `.kiro/specs/`. MCP vía `.kiro/settings/mcp.json`. Skills (mismo estándar abierto, mismo `SKILL.md`) en `.kiro/skills/`. Constitución ≈ *Steering files* en `.kiro/steering/`.

## Key Findings (estado verificado a junio 2026)

**Spec Kit (github/spec-kit) — Camino A.** Instalación con uv: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` (persistente) o uso efímero `uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT>`. La última release es 0.8.18 (29-may-2026). Init: `specify init <nombre> --integration claude` o en el directorio actual `specify init . --integration claude`. El flag `--ai` quedó deprecado en favor de `--integration` (changelog #2218). Verificación: `specify check`, `specify version`; upgrade: `specify self upgrade`. Los slash-commands se instalan en `.claude/commands/`; la constitución vive en `.specify/memory/constitution.md` y los artefactos por feature en `specs/<N>-<feature>/`.

**Claude Code — Camino A.** Método recomendado por Anthropic (anunciado oct-2025): instalador nativo, sin Node. macOS/Linux: `curl -fsSL https://claude.ai/install.sh | bash`; Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`. Alternativa npm (legada, Node 18+): `npm install -g @anthropic-ai/claude-code` (nunca con sudo). El binario nativo queda en `~/.local/bin/claude` y se autoactualiza. Verificación: `claude --version`, `claude doctor`. Autenticación OAuth en el navegador al primer arranque (Pro/Max/Team/Enterprise). En un repo: `/init` genera `CLAUDE.md`.

**Kiro (AWS) — Camino B.** IDE agéntico construido sobre Code OSS (la base open-source de VS Code), por lo que las extensiones y keybindings de VS Code se mantienen (SoftwareSeni review, may-2026). Lanzado públicamente a mediados de 2025 y relanzado internacionalmente el 7-may-2026 como reemplazo de Amazon Q Developer. Login con Google, GitHub, Builder ID o AWS SSO; **no requiere cuenta de AWS**. Descarga: kiro.dev/downloads. **SDD nativo** (kiro.dev/docs/specs, may-2026): un *Feature Spec* sigue tres fases — Requirements (user stories + criterios de aceptación en notación EARS, en `requirements.md`) → Design (`design.md`) → Tasks (`tasks.md`), guardados en `.kiro/specs/<feature>/`. Variantes de workflow: **Requirements-First**, **Design-First** y **Quick Plan** (genera las tres fases de una sin gates de aprobación); además hay **Bugfix Specs**. También se puede hacer "vibe" y luego decir *"Generate spec"*. Inversión spec-first explícita: la spec es la fuente de verdad y el código es un build artifact (digitalapplied guide, abr-2026).

**Skills (estándar abierto Agent Skills) — ambos caminos.** Una Skill es una carpeta con un `SKILL.md` que arranca con frontmatter YAML; campos requeridos `name` (≤64 chars, minúsculas/números/guiones) y `description` (≤1024 chars, tercera persona, qué hace y cuándo usarse). Progressive disclosure de 3 niveles (al inicio solo name+description; el cuerpo al matchear; los archivos de `references/`, `scripts/`, `assets/` recién cuando se necesitan). Cuerpo recomendado <500 líneas. **Camino A:** ubicaciones `~/.claude/skills/` (personal) o `.claude/skills/` (proyecto); detección en caliente o `/reload-skills`; los "custom commands" se fusionaron con Skills. **Camino B:** Kiro adoptó el mismo estándar abierto (kiro.dev/docs/skills, feb-2026): mismo `SKILL.md`, misma estructura de carpeta (`SKILL.md`, `scripts/`, `references/`, `assets/`), progressive disclosure idéntica; ubicaciones `~/.kiro/skills/` (usuario) o `.kiro/skills/` (workspace, las de workspace ganan ante colisión de nombres). **Cuidado:** Kiro solo reconoce la Skill si está en su subcarpeta `.kiro/skills/<nombre>/SKILL.md`, no suelta bajo `skills/` (dev.to aws-builders, feb-2026). Kiro además tiene **Powers** (un superset que empaqueta MCP servers + steering + hooks; frontmatter `POWER.md` con name/displayName/description/keywords/mcpServers) y **Steering files** (contexto propio de Kiro, en `.kiro/steering/`, con modos de inclusión always/auto/fileMatch/manual) — el equivalente más cercano a la constitución.

**MCP (Model Context Protocol) — ambos caminos.** SDK oficial Python: paquete `mcp` (1.27.0 lanzada 2-abr-2026, requiere Python ≥3.10; "Development Status :: 4 - Beta"). Setup con uv: `uv init <dir>`, `uv venv`, `source .venv/bin/activate`, `uv add "mcp[cli]" httpx`. Import: `from mcp.server.fastmcp import FastMCP`; tool con `@mcp.tool()`; transporte stdio: `mcp.run(transport="stdio")`. **Gotcha crítico:** en stdio NUNCA escribir a stdout (`print()` corrompe el JSON-RPC); usar `sys.stderr` o `logging`. **Camino A — registro:** `claude mcp add items-api -- uv run server.py` (scope local; `--scope project` genera `.mcp.json`); verificación `claude mcp list` y `/mcp`. **Camino B — registro:** editar `.kiro/settings/mcp.json` (workspace) o `~/.kiro/settings/mcp.json` (usuario) con la estructura `{"mcpServers": {"items-api": {"command": "uv", "args": [...], "disabled": false}}}` (kiro.dev/docs/mcp/configuration, ene-2026; kiro.dev/docs/cli/mcp, mar-2026).

**uv/uvx (Astral) — ambos caminos.** Instalación: `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux) o `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows). `uvx` = `uv tool run`. Verificación: `uv --version`. Reiniciá la terminal después de instalar. En Camino B, uv se usa para correr el servidor MCP del Bloque 4 (no hace falta `claude` ni Spec Kit).

---

## TABLA MAESTRA DE EQUIVALENCIAS (Camino A ↔ Camino B)

| Pieza del taller | Camino A · Claude Code + Spec Kit | Camino B · Kiro |
|---|---|---|
| **Flujo SDD** | Instalás Spec Kit; `/speckit.constitution → specify → clarify → plan → tasks → analyze → implement` | SDD **nativo**: creás un *Feature Spec* (Requirements-First / Design-First / Quick Plan); genera `requirements.md → design.md → tasks.md` en `.kiro/specs/` |
| **Reglas / constitución** | `.specify/memory/constitution.md` | **Steering files** en `.kiro/steering/` (always / auto / fileMatch / manual) |
| **`.md` del problema (Bloque 3)** | Idéntico — se lo pegás a `/speckit.specify` | **Idéntico** — se lo pegás al crear el Feature Spec |
| **Servidor MCP (Bloque 4)** | **Mismo código Python** (SDK oficial `mcp`, stdio) | **Mismo código Python**, sin cambios |
| **Registrar el MCP** | `claude mcp add items-api -- uv run server.py` | Editar `.kiro/settings/mcp.json` con `{"mcpServers": {...}}` |
| **La Skill (Bloque 4)** | Mismo `SKILL.md`; `.claude/skills/items-ops/` | **Mismo `SKILL.md`**; `.kiro/skills/items-ops/` |
| **Verificar MCP** | `claude mcp list`, `/mcp` | Panel MCP de Kiro / `/mcp` en chat |
| **Bloques 1, 2, 5 (teoría/HTML)** | Conceptuales — sirven igual | Conceptuales — sirven igual |

> **La única diferencia de fondo:** en Camino A el flujo SDD lo *agregás* (Spec Kit); en Camino B *ya viene de fábrica*. Todo lo demás es portable. Eso refuerza el cierre del taller: *"diseñá tu propio SDD basado en Skills"* aplica igual en las dos herramientas.

---

## Details

A continuación, las 4 partes del entregable, ya en dual-track. Texto para participantes y facilitador en español rioplatense (voseo).

### PARTE 1 — MATERIAL PREVIO (documento autocontenido para participantes)

> El material previo ya está entregado como **PDF dual-track** (portada, dos caminos color-coded, refresher Flask+SQLite, tabla de equivalencias y links a docs oficiales). Lo que sigue es el spec que lo genera y el contenido fuente, por si querés regenerarlo o editarlo.

#### 1.A — SPEC PARA CLAUDE (para generar/regenerar el .md de material previo)

> **Spec: "Generá el material previo del taller de SDD + Skills (dual-track)"**
>
> Generá un único Markdown autocontenido `material-previo.md`, en español rioplatense (voseo), para una audiencia técnica general cómoda con terminal, Python, Git y Docker, principiante en agentes. El taller se puede hacer con **Claude Code + Spec Kit (Camino A)** o con **Kiro (Camino B)**: marcá con etiquetas de color qué pasos son comunes y cuáles de cada camino. No expliques redes neuronales/transformers (solo enlazá videos). Secciones, en orden:
> 1. **Cómo usar el documento** — grupo mixto, dos caminos, etiquetas A/B/Ambos.
> 2. **Qué es SDD y por qué** — vibe coding no escala; spec como fuente de verdad; IaC para el código (sin referencias a una industria puntual). Máx. 400 palabras.
> 3. **Las dos herramientas** — Spec Kit (agrega SDD a Claude Code) vs Kiro (SDD nativo); recuadro "SDD/MCP/Skills son estándares abiertos".
> 4. **Instalación y verificación** — base común (Python ≥3.11, uv, Git, Docker); Camino A (Claude Code nativo + Spec Kit); Camino B (Kiro, sin Spec Kit). Comandos EXACTOS + checklist por camino.
> 5. **Refresher Flask + SQLite** — `app.py` con GET y POST contra SQLite stdlib; correr con `uv run --with flask app.py`; probar con `curl`.
> 6. **Tabla "cómo se mapea el curso en cada herramienta"**.
> 7. **Referencias** — 3blue1brown + docs oficiales de ambos caminos.
> Requisitos: bloques de código con lenguaje, comandos copy-paste, cerrar con checklist `[ ]`. No inventes comandos.

#### 1.B — CONTENIDO FUENTE (puntos que cambian respecto a la versión single-track)

Casi todo el material previo single-track se mantiene. Los **agregados dual-track** son:

**Instalación — Camino B (Kiro):**
```text
1) Descargá Kiro desde kiro.dev/downloads (macOS / Linux / Windows; es fork de VS Code).
2) Abrílo y logueate con Google, GitHub, Builder ID o AWS SSO (no hace falta cuenta AWS).
3) En Kiro NO instalás Spec Kit ni Claude Code: el flujo SDD viene incluido.
   De la base común solo necesitás uv (para el MCP del Bloque 4), Python, Git y Docker.
4) Verificación: abrí una carpeta vacía (File → Open Folder) y confirmá que aparece
   el panel "Specs" en la barra lateral y que podés abrir el chat.
```

**Checklist "entorno listo" (Camino B):**
- [ ] Kiro instalado y con sesión iniciada
- [ ] Abrí una carpeta y veo el panel **Specs**
- [ ] `uv --version`, `python3 --version` ≥ 3.11, `git`/`docker` responden (base común)

El resto (SDD/por qué, refresher Flask+SQLite, referencias 3b1b) es idéntico al single-track.

---

### PARTE 2 — GUION MINUTO A MINUTO POR BLOQUE (150 min en vivo, dual-track)

> Reparto: B0 (apertura) 10 · B1 (Fundamentos SDD) 25 · B2 (Setup) 25 · B3 (Práctica guiada) 45 · B4 (Skill + MCP) 35 · B5 (Reflexión) 10. Total 150 min. Donde hay divergencia, se indica **[A]** / **[B]**.

**BLOQUE 0 — Apertura (0:00–0:10)**
- 0:00–0:03 — Dice: "Bienvenidos a la Clase 3. Hoy construimos SDD end-to-end. El grupo viene mixto: algunos con Claude Code + Spec Kit, otros con Kiro. La buena noticia: SDD, MCP y Skills son estándares abiertos, así que el 90% es igual." Comparte agenda y la tabla maestra de equivalencias.
- 0:03–0:08 — Hace: pide correr el checklist. **[A]** `uv --version`, `claude --version`, `specify check`. **[B]** `uv --version` + confirmar panel Specs en Kiro.
- 0:08–0:10 — Resuelve rojos rápidos; deriva al troubleshooting (4.G).

**BLOQUE 1 — Fundamentos de SDD (0:10–0:35)**
- 0:10–0:13 — Dice: "spec gobierna, código es output"; analogía IaC.
- 0:13–0:23 — Hace: presenta la HTML del Bloque 1 (spec 4.A). Recorre el flujo SDD en abstracto y después lo aterriza en cada herramienta: **[A]** `/speckit.*` y artefactos en `.specify/`+`specs/`; **[B]** Feature Spec de Kiro y artefactos `requirements.md`/`design.md`/`tasks.md` en `.kiro/specs/`. Punto clave: **el mismo concepto, dos implementaciones**.
- 0:23–0:33 — Dice: adaptar SDD a la empresa. **[A]** constitución en `.specify/memory/constitution.md`. **[B]** Steering files en `.kiro/steering/`. Participantes: anotan qué reglas pondrían.
- 0:33–0:35 — Transición al setup.

**BLOQUE 2 — Setup técnico hands-on (0:35–1:00)**
- 0:35–0:38 — Dice: "Cada uno arma su entorno según su camino." Muestra HTML del Bloque 2.
- 0:38–0:50 — Hace/Participantes tipean:
  - **[A]**
    ```bash
    mkdir taller-sdd && cd taller-sdd
    git init
    claude              # primera vez: autenticar en navegador
    # dentro de Claude Code:
    /init
    specify init . --integration claude
    ```
    Luego, en Claude Code, tipear `/` y confirmar que aparecen los `/speckit.*`.
  - **[B]**
    ```text
    En Kiro: File → New Folder "taller-sdd" → Open Folder.
    (Opcional) abrir terminal integrada y: git init
    No se instala Spec Kit. El panel "Specs" ya está listo.
    ```
- 0:50–1:00 — Verificación grupal. **[A]** `ls .specify/ .claude/commands/`. **[B]** confirmar el botón "+" bajo Specs y que el chat responde. Troubleshooting de los que no ven comandos/panel.

**BLOQUE 3 — Práctica guiada: flujo completo (1:00–1:45)**
- 1:00–1:05 — Dice: entrega el `.md` del problema (4.B). "Primero ESTIMÁ cuánto tardarías a mano (DB + Flask + 4 endpoints + seed + curl). Anotá el número."
- 1:05–1:08 — Dice: "Ahora lo automatizamos vía SDD, cada uno en su herramienta."
- 1:08–1:42 — Participantes ejecutan el flujo:
  - **[A]**
    ```text
    /speckit.constitution  (reglas: solo stdlib + Flask, sqlite3, sin auth, tests con curl)
    /speckit.specify       (pegar el contenido del .md del problema)
    /speckit.clarify       (cerrar ambigüedades)
    /speckit.plan          (Flask + sqlite3 stdlib)
    /speckit.tasks
    /speckit.analyze       (gate de consistencia)
    /speckit.implement
    ```
  - **[B]**
    ```text
    (Opcional) crear un Steering file en .kiro/steering/ con las mismas reglas.
    Panel Specs → "+" → Feature → pegar el .md del problema →
       elegir Requirements-First (o Quick Plan si el grupo va ajustado de tiempo) →
       revisar requirements.md → aprobar → revisar design.md → aprobar →
       revisar tasks.md → "Run all Tasks" (o tarea por tarea, recomendado).
    ```
  Mientras corre, el facilitador narra qué está pasando en cada fase.
- 1:42–1:45 — Prueban con curl los endpoints y comparan tiempo real vs estimación. "¿Quién tardó menos? ¿Qué les sorprendió?"

**BLOQUE 4 — Construcción de una Skill con SDD + MCP (1:45–2:20)**
- 1:45–1:48 — Dice: "Levantamos un MCP propio que le pega a los endpoints, y vía specs creamos una Skill que conecta todo." (El servidor Flask del Bloque 3 debe estar corriendo.)
- 1:48–1:58 — Participantes crean el MCP server (4.C). Tipean (idéntico en ambos caminos):
  ```bash
  uv init mcp-items && cd mcp-items
  uv venv && source .venv/bin/activate
  uv add "mcp[cli]" httpx
  # pegan server.py (apéndice 4.C)
  ```
- 1:58–2:03 — Registran el MCP:
  - **[A]**
    ```bash
    claude mcp add items-api -- uv --directory "$(pwd)" run server.py
    claude mcp list          # debe aparecer items-api
    # dentro de Claude Code: /mcp
    ```
  - **[B]** — crear/editar `.kiro/settings/mcp.json` en el workspace:
    ```json
    {
      "mcpServers": {
        "items-api": {
          "command": "uv",
          "args": ["--directory", "/ruta/absoluta/a/mcp-items", "run", "server.py"],
          "disabled": false
        }
      }
    }
    ```
    Kiro recarga el MCP al guardar; confirmar en el panel de MCP que `items-api` está conectado y expone las tools.
- 2:03–2:15 — Vía SDD crean la Skill (4.D). **[A]** `/speckit.specify` con la spec de la Skill → `plan` → `tasks` → `implement`; resultado en `.claude/skills/items-ops/SKILL.md`. **[B]** Feature Spec de Kiro con la misma spec; resultado en `.kiro/skills/items-ops/SKILL.md` (recordá la subcarpeta con el nombre).
- 2:15–2:20 — Prueban: "listá los modelos y agregá uno". El agente usa la Skill + las tools del MCP. Verifican con curl.

**BLOQUE 5 — Reflexión y extensión (2:20–2:30)**
- 2:20–2:25 — Dice: HTML del Bloque 5: Skills + MCPs + imaginación = construís cualquier cosa. MCP = conectividad (tools), Skills = procedimiento (cómo se hace acá). Da los 2–3 ejemplos.
- 2:25–2:30 — Dice: el concepto central — "diseñá tu propio SDD basado en Skills". **[A]** Skills + constitución. **[B]** Skills + Steering + **Powers** (que empaquetan MCP + steering + hooks). Cierre y próximos pasos.

---

### PARTE 3 — ESQUEMA DE SLIDES (outline del taller, dual-track)

1. Portada: "Clase 3 — SDD + Skills, hands-on (dual-track)".
2. Recap Clases 1–2.
3. Agenda + **tabla maestra de equivalencias A ↔ B**.
4. Bloque 1 — Qué es SDD (spec = fuente de verdad; IaC).
5. Bloque 1 — El flujo SDD en abstracto.
6. Bloque 1 — **Dos implementaciones:** Spec Kit (`/speckit.*`, `.specify/`) | Kiro (Feature Spec, `.kiro/specs/`).
7. Bloque 1 — Adaptar a tu empresa: constitución | Steering files.
8. Bloque 2 — Setup **[A]**: Claude Code + repo + `/init` + `specify init`.
9. Bloque 2 — Setup **[B]**: instalar Kiro + abrir carpeta + panel Specs.
10. Bloque 3 — El problema (DB + Flask + GET/POST + curl); estimá a mano.
11. Bloque 3 — El flujo SDD en vivo (lado a lado A | B).
12. Bloque 3 — SDD vs vibe coding (tiempo, calidad).
13. Bloque 4 — MCP custom mínimo (FastMCP oficial, stdio) — **mismo código**.
14. Bloque 4 — Registrar el MCP: `claude mcp add` | `.kiro/settings/mcp.json`.
15. Bloque 4 — Crear la Skill con SDD — **mismo `SKILL.md`**, distinta carpeta.
16. Bloque 5 — Skills + MCPs + imaginación.
17. Bloque 5 — Ejemplos de Skills para el día a día.
18. Bloque 5 — "Diseñá tu propio SDD basado en Skills" (A: constitución+Skills · B: Steering+Skills+Powers).
19. Cierre / Q&A.

---

### PARTE 4 — APÉNDICE TÉCNICO (specs, comandos y código verificados, dual-track)

#### 4.A — SPECS PARA LAS PRESENTACIONES HTML

> Las tres specs HTML (Bloques 1, 2 y 5) deben mostrar **ambos caminos**. Agregar a cada una: "Mostrá el concepto en abstracto y luego, lado a lado, cómo se hace en Claude Code + Spec Kit y en Kiro, usando la tabla maestra de equivalencias."

**Spec Bloque 1 (HTML — Fundamentos de SDD):** presentación HTML autocontenida (un archivo, abre en Chrome, navegación por flechas, tema oscuro, tipografía grande), español rioplatense. Contenido: (1) Qué es SDD y por qué; (2) el flujo SDD en abstracto y luego **dos implementaciones lado a lado**: Spec Kit (`/speckit.constitution/specify/clarify/plan/tasks/analyze/implement`, artefactos en `.specify/memory/constitution.md` y `specs/<N>-<feature>/`) vs Kiro (Feature Spec Requirements-First/Design-First/Quick Plan, artefactos `requirements.md`/`design.md`/`tasks.md` en `.kiro/specs/`); (3) adaptar SDD a cada empresa: constitución (A) vs Steering files (B). Diagramas con HTML/CSS, sin imágenes externas.

**Spec Bloque 2 (HTML — Setup hands-on):** dos tracks claramente separados por color. **[A]** instalar Claude Code (instalador nativo `curl -fsSL https://claude.ai/install.sh | bash`; npm legado), `claude --version`/`doctor`, autenticar, crear repo, `/init`, `specify init . --integration claude`, confirmar `/speckit.*`. **[B]** descargar Kiro (kiro.dev/downloads), login, abrir carpeta, panel Specs listo (sin Spec Kit). Cada slide con bloque copy-paste y "salida esperada". Última slide: checklist por camino.

**Spec Bloque 5 (HTML — Reflexión y extensión):** (1) Skills + MCPs + imaginación; MCP = conectividad, Skills = procedimiento; (2) 2–3 ejemplos de Skills útiles; (3) "diseñá tu propio SDD basado en Skills": encodear specify/plan/tasks/implement como Skills a medida del stack — en A con Skills+constitución, en B con Skills+Steering+**Powers**. Cierre con llamado a la acción.

#### 4.B — EL `.md` DEL PROBLEMA (Bloque 3, sin mencionar ninguna herramienta)

> **Es tool-agnostic a propósito:** el mismo archivo se le pega a `/speckit.specify` (A) o al crear el Feature Spec (B).

**# Problema: API local de inventario de modelos**

**## Contexto.** Necesitás un servicio local mínimo para registrar artefactos de modelos en un inventario. Todo corre en tu máquina, sin nube, sin auth.

**## Objetivo.** Levantar una base de datos local y un servidor Flask con endpoints GET y POST, y probarlos con `curl`.

**## Stack obligatorio.** Python 3.11+, Flask, módulo `sqlite3` de la stdlib (sin ORM). Un solo archivo `app.py`. Base `inventory.db` creada automáticamente.

**## Modelo de datos.** Tabla `models`: `id` INTEGER PK AUTOINCREMENT; `name` TEXT NOT NULL; `framework` TEXT NOT NULL; `accuracy` REAL; `created_at` TEXT (timestamp ISO).

**## Endpoints.** `GET /models` (lista JSON); `GET /models/<id>` (404 si no existe); `POST /models` (body `{"name","framework","accuracy"}`, setea `created_at` en el server, responde 201 con `{"id"}`); `GET /health` (`{"status":"ok"}`).

**## Seed.** Si la tabla está vacía al iniciar, insertar: `{"name":"resnet50","framework":"pytorch","accuracy":0.76}` y `{"name":"xgb-churn","framework":"sklearn","accuracy":0.88}`.

**## Criterios de aceptación.** `/health` → ok; `GET /models` ≥ 2 seeds; `POST` válido crea y un segundo `GET` lo incluye; `GET /models/<id>` inexistente → 404; `POST` sin campos requeridos → 400; server en `http://127.0.0.1:5000`.

**## Tu tarea (antes de automatizar).** Estimá cuánto tardarías a mano (DB + server + 4 endpoints + seed + pruebas curl). Anotá el número en minutos.

**## Pruebas con curl (definición de hecho).**
```bash
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/models
curl -X POST http://127.0.0.1:5000/models -H "Content-Type: application/json" \
  -d '{"name":"bert-base","framework":"pytorch","accuracy":0.91}'
curl http://127.0.0.1:5000/models/1
```

#### 4.C — CÓDIGO DEL MCP SERVER MÍNIMO (SDK oficial, idéntico en ambos caminos)

Verificado contra el SDK oficial `mcp` (1.27.x, Python ≥3.10) y modelcontextprotocol.io/docs/develop/build-server.

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

**Registro — Camino A (Claude Code):**
```bash
claude mcp add items-api -- uv --directory "$(pwd)" run server.py
claude mcp list                 # debe aparecer items-api
/mcp                            # dentro de la sesión
```
Para compartir con el equipo: agregá `--scope project` (genera `.mcp.json` commiteable).

**Registro — Camino B (Kiro):** crear `.kiro/settings/mcp.json` (workspace) o `~/.kiro/settings/mcp.json` (usuario):
```json
{
  "mcpServers": {
    "items-api": {
      "command": "uv",
      "args": ["--directory", "/ruta/absoluta/a/mcp-items", "run", "server.py"],
      "disabled": false
    }
  }
}
```
Kiro recarga al guardar; verificá en el panel MCP que `items-api` aparece conectado con sus 3 tools. (Usar ruta absoluta en `--directory` evita el problema de working-directory.)

#### 4.D — LA SKILL CONSTRUIDA CON SDD (spec, pasos, artefacto final, ambos caminos)

**Spec de la Skill (autosuficiente para generar todas las specs):**
> Quiero una Skill llamada `items-ops` que opere el inventario de modelos a través de las tools del MCP `items-api`. Generá vía SDD la Skill completa. Debe: (1) explicar cuándo usarse (listar, consultar o agregar modelos); (2) instruir a usar SIEMPRE los nombres calificados de las tools (`items-api:list_models`, `items-api:get_model`, `items-api:add_model`); (3) validar `accuracy` entre 0 y 1 antes de un alta; (4) tras un alta, confirmar el id leyendo el modelo. El `SKILL.md` debe tener frontmatter YAML con `name: items-ops` y un `description` en tercera persona (≤1024 chars) con qué hace y cuándo usarse. Cuerpo <500 líneas.
>
> Ubicación del artefacto: **[A]** `.claude/skills/items-ops/SKILL.md` · **[B]** `.kiro/skills/items-ops/SKILL.md` (respetá la subcarpeta con el nombre).

**Pasos:** **[A]** `/speckit.specify` (pegar la spec) → `plan` → `tasks` → `implement`; reiniciar Claude Code o `/reload-skills` si la carpeta es nueva. **[B]** Feature Spec de Kiro con la misma spec → requirements → design → tasks → implement; la Skill queda en `.kiro/skills/`.

**Artefacto final esperado — `SKILL.md` (idéntico en ambos caminos):**
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

> Buenas prácticas (ambos): usar nombres calificados `servidor:tool` evita errores "tool not found" cuando hay varios MCP conectados. En Kiro, además, podés empaquetar este MCP + la Skill + un Steering en un **Power** para distribuirlo al equipo.

#### 4.E — 2–3 EJEMPLOS DE SKILLS ÚTILES PARA EL DÍA A DÍA

1. **`run-training`** — captura el procedimiento reproducible de levantar un entrenamiento (entorno, variables, script de lanzamiento) y queda commiteada como skill de proyecto para que todos sigan la misma receta.
2. **`data-drift-check`** — corre el chequeo de drift entre dataset de referencia y producción usando un script `scripts/drift.py` bundleado, e interpreta el reporte (script determinístico = confiabilidad, sin gastar contexto).
3. **`model-card`** — genera la model card de un artefacto siguiendo el template del equipo (`references/model-card-template.md`), tomando métricas del inventario vía el MCP.

> En Kiro estas mismas tres funcionan igual (mismo `SKILL.md` en `.kiro/skills/`); si una necesita conectividad además del procedimiento, conviene empaquetarla como **Power**.

#### 4.F — "DISEÑÁ TU PROPIO SDD BASADO EN SKILLS"

El flujo SDD (specify→plan→tasks→implement) no es fijo. Como una Skill es solo una carpeta con un `SKILL.md` que enseña un procedimiento con progressive disclosure, podés **encodear cada fase de tu SDD como una Skill a medida de tu stack**: una `specify` que sepa que tus specs incluyen sección de datos, métricas objetivo y restricciones de latencia; una `plan` que imponga tu stack (Kubeflow, MLflow, tal registry); una `tasks` con tus convenciones de CI; una `implement` que conozca tus repos y patrones. MCP aporta la **conectividad** (tools hacia tus sistemas) y las Skills aportan el **procedimiento** (cómo se hace acá).

- **Camino A:** Skills (`.claude/skills/`) + constitución (`.specify/memory/`), versionado en el repo y compartible vía plugins.
- **Camino B:** Skills (`.kiro/skills/`) + **Steering files** (`.kiro/steering/`) + **Powers** (empaquetan MCP + steering + hooks en una unidad instalable desde la UI). Kiro te da, de fábrica, las tres piezas para armar tu propio SDD de equipo.

La conclusión es la misma en las dos: dejás de usar un SDD genérico y pasás a tener el tuyo, a medida del stack y portable.

#### 4.G — TROUBLESHOOTING (ambos caminos)

**Comunes:**
- **Python viejo/no encontrado:** `python3 --version`; si <3.11, `uv python install 3.12`. Spec Kit y el SDK MCP requieren ≥3.10.
- **`uv`/`uvx` "command not found":** reabrí la terminal; si persiste, agregá `~/.local/bin` al PATH.
- **MCP 0 tools / no conecta:** corré el server a mano para ver errores en stderr; nunca `print()` a stdout (corrompe el JSON-RPC); usá **ruta absoluta** en el working directory; el server stdio descubre tools al inicio de sesión.
- **Flask/SQLite:** "no such table" → no inicializaste la DB; POST falla → falta `-H "Content-Type: application/json"`; puerto 5000 ocupado → cambialo.

**Camino A (Claude Code + Spec Kit):**
- **Claude Code "command not found":** abrí terminal nueva o `source ~/.zshrc`; el binario nativo está en `~/.local/bin/claude`.
- **Node viejo (instalación npm legada):** requiere Node 18+; mejor usá el instalador nativo; nunca `sudo npm`.
- **No aparecen los `/speckit.*`:** carpeta equivocada o no reiniciaste; `ls .claude/commands/`, reiniciá Claude Code; usá `--integration claude` (no el viejo `--ai`).
- **MCP no aparece tras `claude mcp add`:** `claude mcp list` y abrí sesión nueva (descubre tools al inicio).

**Camino B (Kiro):**
- **No veo el panel Specs:** confirmá que abriste una carpeta (no un archivo suelto); reabrí la carpeta con File → Open Folder.
- **La Skill no se reconoce:** debe estar en `.kiro/skills/<nombre>/SKILL.md` (subcarpeta con el nombre), no suelta bajo `skills/`; revisá el frontmatter (`name`, `description`).
- **El MCP no conecta desde `mcp.json`:** validá el JSON (comas, llaves); usá ruta absoluta en `--directory`; verificá que el server Flask del Bloque 3 esté corriendo; mirá los logs del panel MCP; si usás variables de entorno, referencialas como `${VAR}` y no hardcodees secretos.
- **El Feature Spec no avanza:** en Requirements-First hay gates de aprobación entre fases; si querés saltarlos para la demo, usá **Quick Plan**.

## Recommendations
1. **Antes del taller:** mandá el PDF de material previo con 3–4 días de anticipación y pediles que peguen el output del checklist (el de su camino) en un canal.
2. **Día del taller:** mostrá la **tabla maestra de equivalencias** en pantalla todo el tiempo; ayuda a que A y B no se pierdan.
3. **Pinneá versiones [A]:** instalá Spec Kit con `@v0.8.18` y, si querés reproducibilidad total, `uv add "mcp[cli]==1.27.1"`.
4. **Para el grupo Kiro [B]:** si vas ajustado de tiempo en el Bloque 3, usá **Quick Plan** (sin gates) para que lleguen al `tasks.md` rápido; reservá los gates para quien quiera ver el detalle.
5. **Umbral de decisión:** si >20% tiene el entorno roto al minuto 8, corré el Bloque 2 como "setup asistido" extendido y recortá 10 min del Bloque 3.

## Caveats
- Spec Kit (0.8.18 estable a 29-may-2026) y Kiro se mueven rápido. Verificá el día del taller: **[A]** `specify check` y los `/speckit.*` con `/`; **[B]** el nombre exacto de las variantes de workflow (Requirements-First / Design-First / Quick Plan) y la ubicación del panel, que pueden cambiar entre releases. La estructura de carpetas y formatos (`SKILL.md`, `mcp.json`, `.kiro/specs/`) está confirmada contra docs de mediados de 2026.
- El SDK oficial `mcp` figura como "Beta" en PyPI; el código de 4.C usa solo lo estable (FastMCP + stdio). La patch exacta (1.27.0 vs 1.27.1) puede variar según el día — pinneá la que verifiques.
- En Kiro, "Powers" y "Skills" coexisten: Powers es un superset (MCP + steering + hooks). Para el taller alcanza con Skills; mencioná Powers solo en el Bloque 5.
- Para Windows nativo varios comandos difieren; recomendá WSL2 (Camino A) o el build nativo de Kiro (Camino B) para uniformar.
- Verificá los títulos/IDs de los videos de 3blue1brown en el canal oficial antes de publicar (la serie a veces renumera capítulos); el de atención es `eMlx5fFNoYc` (7-abr-2024).
