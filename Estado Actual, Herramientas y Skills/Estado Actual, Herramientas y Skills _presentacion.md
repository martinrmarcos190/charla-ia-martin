# Clase 2 — Estado actual, herramientas y Skills · CONTENIDO DE PRESENTACIÓN

> **PARA CLAUDE CODE — leé esto antes de armar nada.**
>
> Tu tarea es construir una presentación HTML standalone a partir del contenido de abajo. Requisitos:
>
> 1. **Stack:** usá **reveal.js** (CDN, última versión estable) en un único archivo `index.html` autocontenido, sin build step. Todo (HTML + CSS + JS) en ese archivo o, como mucho, con un `style` embebido.
> 2. **Tema:** dark, técnico, sobrio. Tipografía sans para texto e **Inter/IBM Plex Sans**; monospace para código (**JetBrains Mono** o **Fira Code** vía CDN). Acentos en un color frío (azul/cian). Pensá "dashboard de DevOps", no "pitch de startup".
> 3. **Syntax highlighting:** usá el plugin `highlight.js` de reveal.js para TODOS los bloques de código. Respetá el lenguaje indicado en cada fence (```bash, ```python, ```json, ```yaml, ```markdown, ```text).
> 4. **Las tres demos van EMBEBIDAS, no en notebook.** Para cada demo (DEMO 1, 2 y 3) construí un **componente "terminal" falso**: un `<div class="terminal">` con barra de título (tres puntitos macOS), prompt, y las líneas de comando + output que te doy. Animá la aparición con **fragments de reveal.js** (`class="fragment"`) para poder "ejecutar" paso a paso con la tecla espacio/flecha. Opcional pero deseable: efecto de tipeo (typing) en los comandos vía un pequeño script JS. El objetivo es que el orador NO necesite abrir una terminal real: la demo "corre" dentro del slide.
> 5. **Tablas:** las dos tablas comparativas (mapa de LLMs y Skills-vs-MCP) tienen que renderizar como tablas HTML estilizadas y legibles a 3 metros. Fuente grande, zebra stripes suaves.
> 6. **Code reveal incremental:** donde marco `[[FRAGMENT]]` entre bullets, usá fragments para revelarlos de a uno.
> 7. **Notas del orador:** meté el contenido del bloque `NOTAS:` de cada slide dentro de `<aside class="notes">` de reveal.js (se ven con la tecla `S`, speaker view). Es texto corto, no el guion completo.
> 8. **Footer/encabezado:** mostrá en cada slide, chico y discreto, el número de slide y el bloque (ej. "2.3 · MCPs y Tools").
> 9. **Idioma:** todo en español rioplatense (voseo). No traduzcas los términos técnicos ni las citas en inglés.
> 10. **Datos con fecha:** donde veas ⚠️, dejá el dato tal cual pero el orador sabe que puede estar desactualizado; no agregues disclaimers en el slide.
>
> Cada bloque `---` separa una diapositiva. El `# Título` o `## Título` es el título del slide. El resto es el contenido visible. Generá una slide por bloque, en orden.

---

# Estado actual, herramientas y Skills
### Curso Applied AI · Parte 2 · 90 min

De random forests a agentes — ahora las herramientas

NOTAS: Saludar corto. "Segunda clase, hoy bajamos a tierra." Avanzar rápido.

---

## Agenda

- **2.1** El mapa actual de LLMs · 15 min
- **2.2** Vibe coding vs SDD · 20 min
- *Break · 5 min*
- **2.3** MCPs y Tools · 20 min
- **2.4** Claude Skills · 17 min
- **2.5** Cierre y puente al workshop · 10 min

NOTAS: 20 segundos. Aclarar que la clase que viene es 100% workshop.

---

## Recap clase 1

- **LLM** = predictor de tokens
- **Embeddings** = significado como coordenadas
- **Transformer** = attention + capas
- **Agent loop** = LLM + tools + memoria
- **Hoy:** estado del arte y las herramientas que cambian cómo trabajamos

NOTAS: Solo reconectar, no re-explicar. Disparador: "¿se acuerdan del agent loop?"

---

## 2.1 · ¿Por qué nos importa el mapa?

- Elegir un LLM = elegir **vendor + pricing + latencia + data residency + roadmap**
- Mismo problema que elegir **RDS vs Aurora vs Postgres self-hosted**
- El error más común en MLOps: tratar a los LLMs como **commodity intercambiable**. No lo son.
- Esto se mueve rapidísimo → importa la **forma de pensar la integración**, no memorizar nombres

NOTAS: Énfasis en la frase de "commodity". Avisar que el slide tiene fecha de vencimiento.

---

## 2.1 · El mapa de LLMs (junio 2026)

| Proveedor | Flagship | Sweet spot | Costo $/M (in/out) | Open? |
|---|---|---|---|---|
| **Anthropic** | Claude Opus 4.8 *(may-26)* | Coding agéntico, long-horizon | Sonnet 4.6: $3/$15 | No |
| **OpenAI** | GPT-5.5 *(abr-26)* | Multimodal, breadth, Codex | $5/$30 | No |
| **Google** | Gemini 3.5 Flash / 3.1 Pro | Multimodal, GCP, costo | Flash: muy bajo | No |
| **Meta** | Muse Spark *(abr-26)* / Llama 4 | Open-weights, self-host | Infra propia | Sí |
| **DeepSeek** | V3.2 / V4 *(mar-26)* | Reasoning, costo extremo | $0.28/$0.42 | Sí (MIT) |
| **Alibaba/Qwen** | Qwen 3.7 Max *(may-26)* | Agentes long-horizon, 1M ctx | $2.50/$7.50 | Max: no |

⚠️ En el radar: Grok, Mistral, MiniMax M2.5, GLM-5, Kimi K2.6. **9 de los top 15 en SWE-bench son chinos.**

NOTAS: 1 min por proveedor. Anthropic domina coding; default real = Sonnet 4.6. Revisar versiones el día de la clase.

---

## 2.1 · Benchmarks: qué mirar y qué no

- Cuando te digan "el mejor", preguntá: **¿en qué benchmark?**
- **SWE-bench Verified** = 500 issues reales de GitHub, validados por humanos

[[FRAGMENT]] Top al **28-may-2026** (BenchLM.ai):
- Claude Mythos Preview — **93.9%**
- Claude Opus 4.8 — **88.6%**
- Claude Opus 4.7 Adaptive — **87.6%**
- Sonnet 4.6 — 79.6%

[[FRAGMENT]] ⚠️ OpenAI dejó de reportar Verified → recomienda **SWE-bench Pro** (harder, contamination-resistant)

[[FRAGMENT]] **Mismos modelos: −35 puntos al pasar de Verified a Pro.** El benchmark da dirección, no precisión.

NOTAS: La métrica online real = cuántos tickets del backlog resuelve sin intervención.

---

## 2.1 · Heurística de elección (regla de 3)

1. **Default** a Sonnet 4.6 / Gemini Flash / GPT mini → 80% del laburo
2. **Reservá** el flagship (Opus 4.8 / GPT-5.5 Pro) para los problemas donde el costo extra se justifica
3. **Plan B open-weights** (Qwen 3.6, DeepSeek V4, Llama) para data residency y costo extremo

> Es la misma estrategia **multi-cloud** que ya conocés.

NOTAS: Cerrar el bloque acá. Es la heurística que se llevan a la práctica.

---

## 2.2 · Vibe coding

> *"There's a new kind of coding I call vibe coding, where you fully give in to the vibes, embrace exponentials, and forget that the code even exists."*
> — **Andrej Karpathy**, 2 de febrero de 2025

- Collins Dictionary **Word of the Year 2025** (6-nov-2025)
- **= deploy a mano por SSH a producción**
- OK para el prototipo del viernes. **NO** para tu pipeline de CI.

NOTAS: La analogía del SSH es la que tiene que pegar.

---

## 2.2 · Por qué vibe coding no escala

- **CodeRabbit** (17-dic-2025, 470 PRs analizados): código IA-coautoreado → **1.4× más issues críticos**, **1.7× más mayores** que código humano
- **Veracode** (oct-2025): solo GPT-5 Mini mejoró seguridad (72% pass rate); Anthropic, Google, Qwen, xAI sin mejoras significativas
- **Veracode** (jul-2025): **45%** del código IA introduce vulnerabilidades del OWASP Top 10
- Falta: **reproducibilidad, revisión, versión, rollback**
- Equivale a tener tu infra en **clicks de consola**

NOTAS: Tres datos, fuerte y rápido. No te quedes en los números, llevá a "falta proceso".

---

## 2.2 · Spec-Driven Development

# SDD = Infrastructure-as-Code para tu código

- `spec.md` = **HCL** · plan = **`terraform plan`** · implement = **`terraform apply`**
- Lo que gobierna es la **spec**, no el código generado

> *"We're moving from 'code is the source of truth' to 'intent is the source of truth'. AI makes specifications executable."*
> — **GitHub Blog**, 2 de septiembre de 2025

NOTAS: Repetir "SDD es IaC para tu código". La frase clave: la spec se volvió ejecutable.

---

## 2.2 · Spec Kit en una slide

- Toolkit **open-source de GitHub** para SDD (sep-2025)
- `github/spec-kit` · ⚠️ ~92k stars · 8k+ forks
- Soporta **30+ agentes** (Claude Code, Copilot, Gemini, Cursor, Codex, Windsurf, Kiro…)

**Flujo canónico (slash commands):**

```text
/speckit.constitution   → principios no-negociables
/speckit.specify         → qué construir (requirements)
/speckit.clarify         → resolver ambigüedades
/speckit.plan            → plan técnico (tech stack)
/speckit.tasks           → lista de tareas ejecutable
/speckit.analyze         → consistencia entre artefactos
/speckit.implement       → ejecutar las tareas
```

NOTAS: La semana que viene se usa en vivo. Hoy solo la intuición.

---

## DEMO 1 · Vibe coding → "ahora escribime la spec"

> **[[TERMINAL EMBEBIDA — animar con fragments]]**

```bash
$ claude
> Hacé un endpoint Flask que reciba un POST con JSON,
  lo valide, lo guarde en SQLite y devuelva un ID.
```
```text
✓ Creado app.py (Flask + sqlite3)
✓ Creado schema.sql
✓ Endpoint POST /items listo. Corriendo en :5000
```
```bash
# Funciona... pero vos no leíste nada. No es reproducible.
> Ahora generame la spec de lo que acabás de hacer:
  requirements, edge cases, dependencias y supuestos. Markdown.
```
```markdown
# Spec — POST /items
## Requirements
- Recibe JSON {name: str, qty: int}
- Valida tipos; 400 si falta campo
- Persiste en SQLite (tabla items)
- Devuelve {id} con 201
## Edge cases
- Body vacío / no-JSON → 400
- qty negativo → 422
## Dependencias: Flask 3.x, sqlite3 (stdlib)
```

**El mismo agente que vibe-codeó te da el artefacto que necesitabas al principio.**
Si la spec se genera al final, puede **dirigir desde el principio** → reproducible, revisable, versionable.

NOTAS: Si la spec puede generarse al final, puede dirigir desde el inicio. Esa spec.md se commitea y se re-implementa en Go la semana que viene.

---

## Break · 5 minutos

Volvemos puntual.

NOTAS: Agua, estiramiento, preguntas sueltas.

---

## 2.3 · El problema M×N

- **3 modelos × 10 tools = 30 integraciones custom**
- Cada una con su auth, su schema, su error handling
- Insostenible de mantener

> Mismo problema que resuelve un **service mesh**: en vez de N² conexiones, una abstracción común.

NOTAS: Anclar en service mesh. Ya lo conocen.

---

## 2.3 · MCP en una slide

# Model Context Protocol = el USB-C de la IA

- **Anthropic**, 25 de noviembre de 2024
- **JSON-RPC 2.0** sobre stdio o Streamable HTTP
- Inspirado en el **LSP** de VS Code: *write once, plug anywhere*
- Adopción: Anthropic, **OpenAI** (mar-2025, Altman), Cursor, VS Code, Zed, Replit
- **>10.000 servers públicos activos** (Linux Foundation, 9-dic-2025)

NOTAS: La frase USB-C. Un server se escribe una vez y cualquier host lo usa.

---

## 2.3 · Estado del protocolo (2-jun-2026)

- Spec **estable: `2025-11-25`**
- ⚠️ **RC: `2026-07-28`** (locked 21-may, final 28-jul) — core stateless, MCP Apps, Tasks, OAuth 2.1 hardening
- **Governance:** donado a la **Agentic AI Foundation** (Linux Foundation) el **9-dic-2025**
  - Co-founders: Anthropic · Block · OpenAI
  - Supporters: Google · Microsoft · AWS · Cloudflare · Bloomberg

> Dejó de ser un protocolo de un solo vendor. Es **estándar de industria con governance formal**.

NOTAS: El RC todavía no es final. No presentarlo como producción.

---

## 2.3 · Las 3 primitivas de MCP

- **Tools** → funciones invocables por el modelo (query DB, mandar email, crear issue)
- **Resources** → data leíble por el modelo (archivos, configs, registros · por URI)
- **Prompts** → templates reutilizables / slash commands

**Handshake:** `initialize` → capabilities → `tools/list` → `tools/call`

> Para los de gRPC: contract-first, capability discovery, request/response tipado.

NOTAS: Mapear cada primitiva a algo que ya conocen.

---

## DEMO 2 · Agregar un MCP server a Claude Code

> **[[TERMINAL EMBEBIDA — animar con fragments]]**

```bash
# Filesystem server oficial (local, stdio)
$ claude mcp add filesystem -s user -- \
    npx -y @modelcontextprotocol/server-filesystem ~/Documents ~/Desktop
```
```text
✓ Added stdio MCP server "filesystem" (scope: user)
```
```bash
$ claude mcp list
```
```text
filesystem   ✓ connected   (stdio)
  tools: read_file, write_file, list_directory, search_files, ...
```
```bash
# Dentro de Claude Code:
> Listame los .md de ~/Documents y resumime el más nuevo.
```
```text
[invoca list_directory → read_file]
→ "notas-arquitectura.md" (modificado hoy):
  Resumen: migración del pipeline de ingest a event-driven...
```

**Servers HTTP remotos (OAuth 2.1):**
```bash
claude mcp add --transport http notion  https://mcp.notion.com/mcp
claude mcp add --transport http stripe  https://mcp.stripe.com
claude mcp add --transport http sentry  https://mcp.sentry.dev/mcp
```

**El modelo NO conoce tu filesystem — lo descubre por protocolo.** Si mañana cambiás a S3, el modelo y tu prompt **no cambian**.

NOTAS: Desglosar el comando: add / nombre / -s user / -- / paths. La abstracción es el punto.

---

## 2.3 · Por qué cambia las reglas

- **Antes:** cada equipo escribía su propio adapter LLM → backend
- **Hoy:** escribís el MCP server **una vez** (`fastmcp`, `@modelcontextprotocol/sdk`) y anda en cualquier host
- El **costo marginal** de integrar una tool nueva → **colapsa**

> Mismo salto que de **drivers JDBC custom** a una **capa estándar**.

NOTAS: Cerrar bloque MCP con esta analogía.

---

## 2.4 · Claude Skills

- Anthropic, **16 de octubre de 2025**
- Un Skill = una **carpeta con un `SKILL.md`** adentro
- YAML frontmatter (`name`, `description`) + instrucciones en Markdown

[[FRAGMENT]] **Progressive disclosure:**
- Al arrancar, Claude lee **solo la descripción** (~30-50 tokens por skill)
- Carga el **body** solo si matchea con tu pedido
- Carga los **archivos auxiliares** solo si los necesita

> *"Claude Skills are awesome, maybe a bigger deal than MCP."* — Simon Willison

NOTAS: El truco es la carga perezosa. Cero overhead hasta que se usa.

---

## 2.4 · Skills vs MCP (memorizá esto)

| | **MCP** | **Skills** |
|---|---|---|
| **Da…** | Conectividad *(cómo técnico)* | Procedimiento *(cómo organizacional)* |
| **Análogo** | Terraform **provider** | Módulo de Terraform / **role de Ansible** |
| **Ejemplo** | "Cómo hablo con Stripe" | "Cómo *mi equipo* hace un refund" |
| **Formato** | JSON-RPC server | Carpeta con `SKILL.md` |
| **Combinables** | ✅ Un Skill puede invocar tools MCP | ✅ |

NOTAS: Esta es la slide que vale oro. MCP = conectividad. Skill = procedimiento.

---

## 2.4 · Estructura de un Skill

```text
my-skill/
├── SKILL.md          # Required: frontmatter + instructions
├── references/       # Optional: docs cargados on-demand
├── scripts/          # Optional: scripts ejecutables
├── assets/           # Optional: templates, logos
└── evals/            # Recommended: tests
```

- Personal: `~/.claude/skills/<nombre>/`
- Proyecto (compartido por el equipo): `.claude/skills/<nombre>/`
- **Hot-reload:** agregás o editás un skill y toma efecto **sin reiniciar la sesión**

NOTAS: En el repo se commitea .claude/skills/ y todo el equipo lo hereda.

---

## DEMO 3 · Crear un Skill en Claude Code

> **[[TERMINAL EMBEBIDA — animar con fragments]]**

```bash
$ mkdir -p ~/.claude/skills/release-notes
$ $EDITOR ~/.claude/skills/release-notes/SKILL.md
```
```markdown
---
name: release-notes
description: Genera release notes con el formato estándar de DataCorp.
  Usar siempre que se pidan release notes, changelog, notas de versión,
  o resumir cambios entre tags de git.
---

# Release Notes — DataCorp Standard
## Iron Law
SIEMPRE seguir la estructura. NO inventar secciones. NO incluir PRs sin ticket JIRA.
## Estructura: Header → Highlights → Breaking → Features → Fixes → Internal
## Procedimiento: git log <prev-tag>..HEAD --oneline → agrupar por feat/fix/chore → [JIRA-XXXX]
```
```bash
# Recargo la sesión y pido (sin nombrar el skill):
> Generame las release notes desde el tag v2.3.0 hasta HEAD.
```
```text
[skill "release-notes" activado automáticamente]
## v2.4.0 — 2026-06-02
**Highlights**
- Autenticación SAML en el dashboard
**New Features**
- Soporte SAML en login [DCP-1234]
**Bug Fixes**
- Fix timeout en export CSV [DCP-1240]
```

1. **Sin prompt engineering** — la inteligencia está versionada en disco
2. **Portable** — lo commiteo y el equipo lo hereda
3. **Open standard** — agentskills.io (18-dic-2025)

NOTAS: El skill se activa solo por la descripción. No hay que nombrarlo.

---

## 2.4 · Skills es un open standard

- Spec publicado en **agentskills.io** (18-dic-2025)
- Soporte nativo: Claude.ai · Claude Code · Agent SDK · Claude API
- Portable a: OpenAI Codex CLI · Cursor · Gemini CLI

> Pensalos como tus **playbooks / roles de Ansible**: capacidad procedimental versionada, *code-reviewable*, *hot-reloadable*. La pieza que faltaba para que el agente sea **una capa más del stack de DevEx**.

NOTAS: Cierre del bloque Skills.

---

## 2.5 · Las 4 piezas juntas

- **Mapa de LLMs** → elegí el motor con criterio
- **SDD** → la spec gobierna, el código es output
- **MCP** → conectividad estándar a todo
- **Skills** → procedimientos versionables del equipo

NOTAS: Recap de una línea cada uno.

---

## 2.5 · La idea fuerza

# La diferencia no está en la herramienta, está en el proceso.

- ¿Tu **spec** es la fuente de verdad, o lo es tu **chat history** con el agente?
- Vibe coding = viernes a la noche. **SDD = producción.**
- Las 4 piezas juntas = la versión 2026 de pasar de **scripts bash a CI/CD declarativo**

NOTAS: Esta es LA frase de la clase. Dejala respirar.

---

## 2.5 · La semana que viene: Workshop

**100% hands-on, con las manos en el teclado:**

1. **Spec Kit** — flujo completo `constitution → … → implement` en un proyecto real
2. **Construir un Skill** aplicando SDD (el doble bucle)
3. **Diseñar un flujo SDD custom** para la realidad de tu empresa

**Traé:** Claude Code 2.1+ actualizado · API key Anthropic · un repo chico real

> La diferencia no está en la herramienta. **Lo probamos en vivo.**

NOTAS: Cerrar con energía. Gracias + preguntas.

---

# ¿Preguntas?

Gracias.
