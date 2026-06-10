# Clase 3 — Workshop SDD + Skills · CONTENIDO DE PRESENTACIÓN

> **PARA CLAUDE CODE — leé esto antes de armar nada.**
>
> Tu tarea es construir una presentación HTML standalone a partir del contenido de abajo. Requisitos (idénticos a la Clase 2, para mantener el estilo del repo):
>
> 1. **Stack:** **reveal.js** (CDN 5.1.0) en un único `index.html` autocontenido, sin build step. CSS embebido.
> 2. **Tema:** dark, técnico, sobrio. **Inter/IBM Plex Sans** para texto; **JetBrains Mono** para código. Acentos en azul/cian. "Dashboard de DevOps", no "pitch de startup". Formato cuadrado 1024×1024.
> 3. **Syntax highlighting:** plugin `highlight.js` de reveal.js para TODOS los bloques de código, respetando el lenguaje del fence (```bash, ```python, ```markdown, ```text).
> 4. **Pasos hands-on EMBEBIDOS como "terminal" falsa:** un `<div class="terminal">` con barra macOS, prompt y líneas comando+output. Animá con **fragments** (`class="fragment"`) para "ejecutar" con espacio/flecha. Efecto de tipeo (`typeit` + `data-text`) en los comandos. El orador NO abre una terminal real: la demo "corre" en el slide.
> 5. **Tablas** comparativas estilizadas y legibles a 3 metros, zebra stripes suaves.
> 6. **Notas del orador:** el bloque `NOTAS:` de cada slide va dentro de `<aside class="notes">` (tecla `S`). Texto corto.
> 7. **Footer/encabezado:** en cada slide, chico y discreto, el número de slide y el bloque (ej. "Bloque 3 · Flujo completo").
> 8. **Idioma:** español rioplatense (voseo). No traducir términos técnicos ni citas en inglés.
> 9. **Datos con fecha** (versiones): dejalos tal cual; el orador sabe que puede revisarlos. Sin disclaimers en el slide.
>
> Cada bloque `---` separa una diapositiva. El `# Título` o `## Título` es el título visible. Generá una slide por bloque, en orden.

---

# SDD + Skills, hands-on
### Curso Applied AI · Clase 3 · Workshop · 150 min

Spec-Driven Development + Claude Skills para MLOps — con las manos en el teclado

NOTAS: Bienvenida corta. "Clase 3, hoy lo construimos end-to-end." El valor está en el teclado de ellos. Confirmá que tienen Claude Code abierto.

---

## Recap clases 1 y 2

- **ML → LLMs → agentes:** el agent loop = LLM + tools + memoria
- **Vibe coding vs SDD:** la spec gobierna, el código es output
- **MCP:** el USB-C de la IA — conectividad
- **Skills:** carpetas con procedimiento del equipo
- **Hoy:** lo construimos end-to-end, en vivo, vos en el teclado

NOTAS: Reconectar, no re-explicar. 1 minuto máximo.

---

## Agenda · reparto de bloques (150 min)

- **B0** Apertura + checklist de entorno · 10 min
- **B1** Fundamentos de SDD + Spec Kit · 25 min
- **B2** Setup hands-on: repo + Spec Kit · 25 min · 🖐️
- **B3** Práctica guiada: flujo SDD completo · 45 min · 🖐️
- **B4** Skill con SDD + MCP propio · 35 min · 🖐️
- **B5** Reflexión, extensión y cierre · 10 min

NOTAS: 20 seg. El grueso (B2–B4, 105 min) es práctica. "Si el entorno de alguno está roto, lo resolvemos ya, no en el minuto 40."

---

## Checklist de entorno (corré esto ahora)

```bash
python3 --version && uv --version
claude --version && claude doctor
specify check
```
- Verde en las tres = listo para el Bloque 2
- ¿Rojo en alguna? Troubleshooting ya, no después

NOTAS: Que todos tipeen. Si >20% tiene algo roto, planificá B2 como "setup asistido" extendido y recortá 10 min de B3.

---

## Spec-Driven Development

- El **vibe coding** no escala: el código *parece* bien, pero no anda o resuelve otra cosa. Se pierde la **intención**.
- SDD da vuelta la jerarquía: la **spec es la única fuente de verdad**; el código es output que se regenera.
- Para MLOps: es **Infrastructure-as-Code, pero para el código**. No parcheás el código: cambiás la spec y regenerás.

NOTAS: La analogía IaC es la que tiene que pegar. "Debuggear = arreglar la spec." Repetir: lo que gobierna es la spec.

---

## Spec Kit, en una slide

- Toolkit **open-source de GitHub** que materializa SDD para agentes de código
- CLI `specify` · bootstrapea el repo con plantillas y slash-commands
- Última release estable **0.8.18** (29-may-2026) · 0.9.0 en desarrollo
- Flujo con fases y checkpoints: constitución → specify → plan → tasks → implement
- **Vos manejás el volante, el agente escribe**

NOTAS: "Le da estructura al SDD: en vez de un prompt suelto, un flujo con gates." Hoy lo corremos entero.

---

## El flujo de comandos /speckit.*

```text
/speckit.constitution   → principios no-negociables
/speckit.specify        → el qué y el porqué
/speckit.clarify        → cierra ambigüedades (opcional)
/speckit.plan           → el cómo técnico
/speckit.tasks          → desglose accionable
/speckit.analyze        → gate de consistencia (opcional)
/speckit.implement      → construye
```
- **Ojo:** hoy llevan prefijo `/speckit.*`; el flag de init es `--integration claude` (el viejo `--ai` quedó deprecado)
- `clarify` y `analyze` son los gates de calidad

NOTAS: Recorré cada comando: qué hace y qué produce. La diferencia con vibe coding son los checkpoints revisables.

---

## Dónde viven los artefactos

```text
.specify/memory/constitution.md     # principios del proyecto
.claude/commands/                   # los slash-commands /speckit.*
specs/001-inventario/
├── spec.md                         # qué construir
├── plan.md                         # cómo (tech stack)
└── tasks.md                        # lista ejecutable
```
- **Todo se commitea.** Versionado, revisable en un PR.

NOTAS: El punto para MLOps: "¿por qué el código hace X?" → la respuesta está en spec.md, no en un chat perdido.

---

## Adaptar el flujo a tu empresa

- **Constitución propia:** tus reglas no-negociables (stack, seguridad, estilo, data residency)
- **Gates de calidad propios:** qué tiene que pasar `analyze` antes de implementar
- **Convenciones de stack:** "acá siempre Flask + sqlite3", "acá siempre Kubeflow + MLflow"
- El flujo **no es sagrado**: es un template que adaptás → más tarde lo encodeamos como Skills
- 📝 ¿Qué 3 reglas pondrías en la constitución de TU proyecto?

NOTAS: Pedí que anoten 3 reglas. Se reconecta en el Bloque 5 ("diseñá tu propio SDD").

---

## Armá tu repo y abrí Claude Code

```bash
mkdir taller-sdd && cd taller-sdd && git init
claude            # primera vez: autenticar en el navegador
# dentro de Claude Code:
/init             # genera CLAUDE.md
```
Instalar Claude Code (si falta): nativo `curl -fsSL https://claude.ai/install.sh | bash` · npm (legado, Node 18+)

NOTAS: Que cada uno corra los comandos. /init genera el CLAUDE.md. Nunca npm con sudo.

---

## Instalá Spec Kit en el repo

```bash
specify init . --integration claude
ls .specify/ .claude/commands/
# dentro de Claude Code: tipeá "/" y confirmá los /speckit.*
```
- ¿No aparecen los comandos? **Reiniciá Claude Code** (descubre comandos al arrancar) y confirmá la carpeta. Usá `--integration claude`, no `--ai`.

NOTAS: Verificación grupal con ls. Troubleshooting de los que no ven los comandos.

---

## Checklist antes de seguir

- ✓ El repo `taller-sdd` existe con `git init`
- ✓ Logueado en Claude Code y corrí `/init` (existe CLAUDE.md)
- ✓ `specify init . --integration claude` corrió OK
- ✓ Veo los `/speckit.*` al tipear `/`
- ✓ Existen `.specify/` y `.claude/commands/`

NOTAS: Pausá. Confirmación a mano alzada. Nadie entra al Bloque 3 con esto en rojo.

---

## El problema: API local de inventario de modelos

- Flask + `sqlite3` (stdlib, sin ORM), un solo `app.py`, base `inventory.db` automática
- Tabla `models`: id, name, framework, accuracy, created_at
- 4 endpoints: `GET /models` · `GET /models/<id>` (404) · `POST /models` (201) · `GET /health`
- Seed de 2 modelos · validaciones (400 sin campos) · pruebas con curl
- **Primero: ¿cuánto tardarías a mano? Anotá tu número.**

NOTAS: Entregá problema-inventario.md. Que ESTIMEN a mano y anoten. No menciones a Claude todavía.

---

## Ahora se lo damos a Claude Code vía SDD

```text
constitution → specify → clarify → plan → tasks → analyze → implement
```
- Cada fase produce un artefacto revisable
- **Vos leés y aprobás entre fase y fase** — no es un botón mágico, es un proceso con checkpoints

NOTAS: Marcá el ritmo: comando por comando juntos. En cada checkpoint abrí el artefacto y leé unas líneas.

---

## Constitución → Spec → Clarify

```text
> /speckit.constitution Proyecto local y simple. Solo stdlib + Flask. SQLite con sqlite3. Sin auth. Tests con curl. Código documentado.
> /speckit.specify <pego problema-inventario.md>
> /speckit.clarify  → responder las preguntas; la spec se actualiza
```
- El `clarify` evita que el agente rellene supuestos por su cuenta. Acá gobernás la intención.

NOTAS: Abrí spec.md y mostrá que es legible. Respondé el clarify en vivo y mostrá cómo se actualiza la spec.

---

## Plan → Tasks → Analyze → Implement

```text
> /speckit.plan Flask + módulo sqlite3 de la stdlib, sin dependencias extra.
> /speckit.tasks
> /speckit.analyze     → consistencia spec ↔ plan ↔ tasks
> /speckit.implement   → app.py + DB + seeds, corriendo en :5000
```
- Mientras corre `implement`, explicá qué hace. Después probá los 4 endpoints con curl.

NOTAS: analyze es el gate de consistencia, antes de escribir código. Narrá mientras implement corre. Probá con curl.

---

## SDD vs vibe coding

| | Vibe coding | SDD |
|---|---|---|
| **Fuente de verdad** | el chat con el agente | la spec, versionada |
| **Reproducible** | no, se pierde la intención | sí, regenerás desde la spec |
| **Revisable** | leés código a ciegas | revisás spec/plan/tasks en un PR |
| **Checkpoints** | ninguno | clarify + analyze (gates) |

- **¿Quién tardó menos que su estimación? ¿Qué parte les sorprendió?**

NOTAS: Comparen tiempo real vs estimación. Llevá a "lo que ganamos no es solo velocidad, es proceso".

---

## Un MCP propio + una Skill, vía SDD

```text
Pedido del usuario  ("listá los modelos y agregá uno")
  └─→ Skill "items-ops"     (el procedimiento)
        └─→ MCP "items-api"  (las tools: list/get/add_model)
              └─→ API Flask  (GET/POST → SQLite)   ✓
```
- **MCP** aporta la conectividad (las tools) · **Skill** aporta el procedimiento (cómo usarlas bien)

NOTAS: La Skill no "habla" con la API: le dice al modelo CÓMO usar las tools que el MCP expone.

---

## MCP server mínimo (FastMCP, stdio)

```python
from mcp.server.fastmcp import FastMCP
import httpx, logging, sys

# stdio: NUNCA print() a stdout (corrompe el JSON-RPC)
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

mcp = FastMCP("items-api")
API_BASE = "http://127.0.0.1:5000"

@mcp.tool()
async def list_models() -> str:
    """Lista todos los modelos del inventario local."""
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{API_BASE}/models", timeout=30.0)
        r.raise_for_status()
        return str(r.json())

if __name__ == "__main__":
    mcp.run(transport="stdio")
```
- SDK oficial `mcp` 1.27.x · Python ≥3.10 · `uv add "mcp[cli]" httpx`

NOTAS: El gotcha crítico: print() a stdout rompe el JSON-RPC. Cada tool se describe con el docstring. Código completo en entregables.

---

## Crear y registrar el MCP

```bash
uv init mcp-items && cd mcp-items
uv venv && source .venv/bin/activate
uv add "mcp[cli]" httpx
# pegar server.py, después:
claude mcp add items-api -- uv run server.py
claude mcp list                 # items-api ✓ connected
# dentro de la sesión: /mcp
```
- Para compartir: `--scope project` (genera `.mcp.json`)

NOTAS: La API Flask del B3 tiene que estar corriendo. Los servers stdio descubren tools al inicio de sesión: si lo agregaste a mitad, abrí sesión nueva.

---

## Generás la Skill con el mismo flujo SDD

```text
> /speckit.specify Quiero una Skill "items-ops" que opere el inventario vía las tools del MCP items-api. Validar accuracy ∈ [0,1] y confirmar el id tras un alta...
> /speckit.plan · /speckit.tasks · /speckit.implement
  → .claude/skills/items-ops/SKILL.md
> /reload-skills   (o reiniciar Claude Code si la carpeta es nueva)
```
- **El doble bucle:** SDD no solo para la app, también para las capacidades del agente

NOTAS: Momento "aha": el mismo flujo SDD que generó la app ahora genera una Skill. Spec completa en entregables. Carpeta nueva → reiniciar.

---

## El SKILL.md resultante

```markdown
---
name: items-ops
description: Opera el inventario de modelos (listar, consultar
  y dar de alta) a través del MCP items-api. Usar cuando el
  usuario pida ver, buscar o agregar modelos al inventario.
---

# items-ops
## Reglas
- Usá siempre los nombres calificados de las tools:
  items-api:list_models · items-api:get_model · items-api:add_model
- Antes de un alta, validá que accuracy ∈ [0, 1].
- Después de un alta, confirmá el id con items-api:get_model.
```
- **Frontmatter:** `name` (≤64) + `description` (≤1024, 3ª persona, qué + cuándo)
- **Progressive disclosure:** solo se carga name+description hasta que la tarea matchea · cuerpo <500 líneas

NOTAS: Las dos reglas de oro del frontmatter. Nombres calificados servidor:tool evitan "tool not found". El description es lo único que Claude lee al arrancar.

---

## La Skill se activa sola y usa el MCP

```text
> Listame los modelos del inventario y agregá uno: bert-base, pytorch, accuracy 0.91.
[skill "items-ops" activada]
[items-api:list_models] → resnet50, xgb-churn
accuracy 0.91 ∈ [0,1] ✓
[items-api:add_model] → {"id": 3}
[items-api:get_model 3] → confirmado: bert-base
```
```bash
curl http://127.0.0.1:5000/models/3
```
- **No nombraste la Skill — se activó sola por su `description`.** Skill (criterio) + MCP (capacidad) + API (ejecución).

NOTAS: El usuario pidió en lenguaje natural, la Skill se activó sola, validó y confirmó. Verificá con curl. Todo el stack junto.

---

## Skills + MCPs + imaginación

- **MCP** te da la **capacidad** (las tools hacia tus sistemas)
- **Skill** te da el **criterio** (cómo se hace acá)
- Combinándolos, construís casi cualquier integración

> *"MCP can provide tools and resources, while Skills package the playbook for using them well."* — Docs de Claude (Agent Skills)

NOTAS: La frase: MCP = capacidad, Skill = criterio. El agente se vuelve una capa más de tu stack de DevEx.

---

## Skills útiles para MLOps

- **🚀 run-training:** captura la receta reproducible de lanzar un entrenamiento (env, vars, script). Commiteada.
- **📉 data-drift-check:** corre un `drift.py` bundleado e interpreta el reporte. Script determinístico = confiable.
- **📋 model-card:** genera la model card con el template del equipo, tomando métricas del inventario vía el MCP.
- **🔁 items-ops:** la que acabás de construir.

Cualquier procedimiento repetible que quieras que el agente haga **siempre igual**.

NOTAS: Mostrá amplitud. run-training refleja el run-skill-generator oficial. Scripts bundleados = confiabilidad sin gastar contexto.

---

## Diseñá tu propio SDD basado en Skills

El flujo specify→plan→tasks→implement **no es fijo**. Encodeá cada fase como una Skill a medida:

- **mlops-specify** → tus specs siempre con sección de datos, métricas objetivo y latencia
- **mlops-plan** → impone tu stack: Kubeflow, MLflow, tu registry
- **mlops-tasks** → genera tareas con tus convenciones de CI
- **mlops-implement** → conoce tus repos y patrones

Tu equipo deja de usar un SDD genérico y pasa a tener **su propio SDD**, versionado y compartible vía plugins.

NOTAS: Cierre conceptual. Conectá con el ejercicio del B1 (las 3 reglas). MCP = conectividad, Skills = procedimiento.

---

## La spec gobierna. El código es output. El procedimiento es versionable.

- Hoy construiste una app, un MCP y una Skill — **todo dirigido por specs**
- El doble bucle: SDD para el producto *y* para las capacidades del agente
- El siguiente paso es tuyo: **encodeá el SDD de tu equipo como Skills**

NOTAS: LA frase de la clase. Dejala respirar. El llamado a la acción es llevarlo a su equipo.

---

## ¿Preguntas?

Gracias por construir en vivo.

Material previo, problema, server.py y SKILL.md → carpeta `entregables/`

NOTAS: Gracias + preguntas. Próximo paso: una Skill para un procedimiento real de su equipo, esta semana.
