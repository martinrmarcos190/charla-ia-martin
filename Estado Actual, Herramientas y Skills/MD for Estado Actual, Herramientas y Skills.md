# Clase 2 — Estado actual, herramientas y Skills
**Curso Applied AI · Parte 2 · 90 minutos · presencial**
**Audiencia:** Devs MLOps old-school (Docker, IaC, CI/CD, pipelines, ML clásico) que ya usan Claude Code a nivel básico.
**Pre-requisito:** Clase 1 (fundamentos: LLMs, embeddings, transformers, agent loop).

---

## TL;DR para el instructor (leer antes de entrar al aula)

- **El mensaje central de la clase es uno solo:** *la diferencia no está en la herramienta, está en el proceso.* El vibe coding es como hacer deploys a mano por SSH; SDD es Infrastructure-as-Code aplicado a tu código. MCP es el USB-C de los agentes. Skills es el equivalente de tener "playbooks" o roles de Ansible cargados en el agente.
- **Tres demos en vivo, todas en Claude Code:** (1) vibe coding rápido → "ahora pedile al agente que te escriba la spec de lo que acabamos de hacer", (2) `claude mcp add` con el filesystem server oficial, (3) crear un Skill propio en `~/.claude/skills/release-notes/SKILL.md`.
- **Cierre:** se anuncia el workshop de la semana que viene (SDD hands-on con Spec Kit + construir un Skill propio con SDD + diseñar tu propio flujo SDD para tu equipo).

---

## 1) Cronograma minuto a minuto (suma 90)

| Bloque | Min | Tiempo absoluto | Tema | Modo |
|---|---|---|---|---|
| 0 | 0–3 | 00:00–00:03 | Bienvenida + recap clase 1 + objetivos de hoy | Speech |
| 2.1 | 3–18 | 00:03–00:18 | El mapa actual: quién es quién en LLMs (15 min) | Speech + slide-tabla |
| 2.2 | 18–38 | 00:18–00:38 | Vibe coding vs SDD + demo en Claude Code (20 min) | Demo en vivo |
| Break | 38–43 | 00:38–00:43 | Pausa cortita / Q&A | — |
| 2.3 | 43–63 | 00:43–01:03 | MCPs y Tools: cómo los agentes se conectan al mundo (20 min) | Demo en vivo |
| 2.4 | 63–80 | 01:03–01:20 | Claude Skills: extendiendo capacidades (17 min) | Demo en vivo |
| 2.5 | 80–90 | 01:20–01:30 | Cierre, síntesis y puente al workshop (10 min) | Speech |

---

## 2) Guion hablado, bloque por bloque (voseo rioplatense)

### Bloque 0 (00:00–00:03) — Bienvenida y framing

> "Bueno, bienvenidos a la segunda clase. La semana pasada vimos los fundamentos: qué es un LLM, qué son los embeddings, cómo funciona un transformer, y el agent loop. Hoy bajamos a tierra. **Hoy hablamos del estado actual del mercado, de las herramientas que están cambiando cómo trabajamos, y de los skills nuevos que tenés que tener vos como MLOps si querés seguir siendo relevante en 2026.**
>
> Vamos a ver cuatro cosas: el mapa de LLMs hoy, vibe coding vs Spec-Driven Development, MCPs y tools, y Claude Skills. Y la clase que viene es 100% workshop: vas a hacer SDD con las manos en el teclado. **Lo que les pido es una cosa: no se queden con que esto son herramientas nuevas. El cambio real es de proceso, no de herramienta. Lo vamos a probar en vivo.**"

---

### Bloque 2.1 (00:03–00:18) — El mapa actual: quién es quién en LLMs (15 min)

**Minuto 3–6 — Por qué nos importa el mapa**

> "Como MLOps, ustedes ya saben que elegir un modelo es elegir un proveedor, una API, una pricing tier, una zona de data residency y un riesgo de deprecación. Es la misma lógica que cuando elegís entre RDS, Aurora o Postgres self-hosted. Hoy en LLMs pasa lo mismo. **El error más común que veo en equipos MLOps es tratar a los LLMs como si fueran un commodity intercambiable. No lo son.** Cada familia tiene un sweet spot, un tokenizer distinto, una latencia distinta y un comportamiento agentico distinto.
>
> Y la otra cosa: esto se mueve rapidísimo. Lo que les muestro hoy, 2 de junio de 2026, en tres meses cambia. Por eso lo que importa es la **forma de pensar la integración**, no memorizar nombres de modelos."

**Minuto 6–12 — Tour de proveedores (apoyándose en la tabla del slide 2.1.B)**

> "Vamos de a uno, rápido. **Anthropic** — Claude. El flagship actual es **Claude Opus 4.8**, anunciado el 28 de mayo de 2026. La que ustedes van a usar el 90% del tiempo es **Sonnet 4.6** (febrero 2026): el daily driver, $3/$15 por millón de tokens, 1M de contexto. **Haiku 4.5** (octubre 2025) es el tier barato y rápido para clasificación, routing, batch. Anthropic domina hoy SWE-bench Verified con Opus 4.8 al 88.6% — si tu workload principal es código, este es el camino más corto.
>
> **OpenAI** — GPT. El flagship es **GPT-5.5** (23 de abril de 2026 release, 24 de abril en API). Tiene variantes Thinking, Pro e Instant. Es más caro que Sonnet ($5/$30 por millón) pero gana en breadth multimodal y en tareas científicas. GPT-5.4 sigue disponible como el caballito de batalla profesional anterior.
>
> **Google** — Gemini. La línea actual es **Gemini 3.5 Flash** (la última generación, performance cerca de Pro al costo de Flash) y **Gemini 3.1 Pro Preview** para reasoning pesado. Si ya están en GCP, la integración con Vertex AI les ahorra horas. Vale la pena.
>
> **Meta** — Llama. Acá hay novedad: Meta estuvo casi un año sin sacar modelo flagship después de que Llama 4 (abril 2025) decepcionara. En abril de 2026, **Meta Superintelligence Labs lanzó Muse Spark** como reemplazo de la línea Llama. Si necesitan open-weights serios, hoy la opción más sólida sigue siendo **Llama 3.3 70B** o **Llama 4 Scout/Maverick** según el caso, pero presten atención a Muse Spark.
>
> **DeepSeek** — la sorpresa china. **DeepSeek V3.2** y la nueva **V4** (marzo 2026) ofrecen calidad cercana a GPT-4o a una décima parte del costo. MIT-licensed, open-weights, MoE. Para batch jobs grandes esto les puede ahorrar zarpadamente.
>
> **Alibaba / Qwen** — **Qwen 3.7 Max** (20 de mayo de 2026, anunciado en el Alibaba Cloud Summit) con 1M de contexto, optimizado para agentes long-horizon, $2.50/$7.50 por millón. El #1 chino en benchmarks. Closed-weights. Para versiones open ya hay Qwen 3.6.
>
> **Otros que vale tener en el radar:** xAI Grok, Mistral, MiniMax M2.5, GLM-5 de Zhipu, Kimi K2.6 de Moonshot. Hoy 9 de los top 15 en SWE-bench Verified son chinos."

**Minuto 12–16 — Benchmarks: qué mirar y qué no**

> "Cuando alguien les diga 'este modelo es el mejor', pregúntenle: ¿en qué benchmark? El estándar de facto para coding agéntico es **SWE-bench Verified** — son 500 issues reales de GitHub validados por humanos. Al 28 de mayo de 2026, según BenchLM.ai, el ranking es: **Claude Mythos Preview 93.9%, Claude Opus 4.8 88.6%, Claude Opus 4.7 (Adaptive) 87.6%**. Sonnet 4.6 está en 79.6%, Opus 4.6 en 80.8%.
>
> Cuidado: OpenAI dejó de reportar Verified a principios de 2026 y recomienda usar **SWE-bench Pro** (versión harder, contamination-resistant de Scale AI). Por qué importa: los mismos modelos que sacan 80% en Verified bajan a 40-45% en Pro. **Los benchmarks dan dirección, no precisión.**
>
> La forma de pensarlo es la misma que ustedes usan con un modelo de ML clásico: el benchmark es la métrica offline. La métrica online es: ¿cuántos tickets de tu backlog real resuelve sin intervención? Ese es el único número que importa."

**Minuto 16–18 — Cierre del bloque**

> "Tres reglas prácticas: **Uno**, default a Sonnet 4.6 (o equivalente Gemini Flash, GPT-5.4 mini) para el 80% del laburo. **Dos**, reservá el modelo flagship para los problemas donde el costo extra está justificado. **Tres**, tené un plan B open-weights (Qwen, DeepSeek, Llama) en pipeline para los casos de data residency o costo extremo. Es exactamente la misma estrategia de multi-cloud que ya conocés."

---

### Bloque 2.2 (00:18–00:38) — Vibe coding vs SDD (20 min)

**Minuto 18–22 — Vibe coding: qué es y por qué no escala**

> "El término **'vibe coding'** lo acuñó Andrej Karpathy el 2 de febrero de 2025. Lo definió así, literal: *'There's a new kind of coding I call vibe coding, where you fully give in to the vibes, embrace exponentials, and forget that the code even exists.'* Hablás con el LLM, aceptás todo lo que te tira, copiás-pegás los errores de vuelta, y seguís. Collins Dictionary lo eligió Palabra del Año 2025 el 6 de noviembre de 2025; Alex Beecroft, Managing Director de Collins, dijo que *'la selección de "vibe coding" como Palabra del Año captura perfectamente cómo el lenguaje evoluciona junto a la tecnología.'*
>
> ¿A qué se parece esto en nuestro mundo? **Vibe coding es como hacer deploys a mano por SSH a producción.** Funciona para el prototipo del viernes a la noche, no funciona para tu pipeline de CI. ¿Por qué? Porque no es reproducible, no es auditable, no es revisable, y cuando el modelo se olvida del contexto te quedaste con código que nadie entiende ni vos.
>
> Y los números lo confirman. El informe *'State of AI vs Human Code Generation'* de CodeRabbit (Business Wire, 17 de diciembre de 2025), que analizó 470 PRs de GitHub (320 co-autoreados con IA vs 150 humanos), encontró que *'los PRs autoreados con IA contienen 1.4× más issues críticos y 1.7× más issues mayores en promedio que los PRs escritos por humanos'*. Y Veracode, en su update de octubre de 2025 titulado *'GPT-5 Pulls Ahead on Secure Code While Rivals Stall'*, confirmó que solamente GPT-5 Mini de OpenAI mejoró de manera significativa la seguridad del código generado (72% de pass rate, el más alto registrado); Anthropic, Google, Qwen y xAI *'no mostraron mejoras significativas en seguridad'*. El reporte previo de julio 2025 de Veracode había detectado que **el 45% del código generado por IA introducía vulnerabilidades del OWASP Top 10**, y que los modelos mejoraban en funcionalidad pero *'no mejor en escribir código seguro'*."

**Minuto 22–26 — SDD: la analogía MLOps que tiene que quedar grabada**

> "**Spec-Driven Development es Infrastructure-as-Code para tu código.** Repito porque importa: SDD es a vibe coding lo que Terraform es a 'clickear en la consola de AWS'. La spec es el HCL. El plan es el `terraform plan`. La implementación es el `terraform apply`. Y como en IaC, **lo que gobierna es la spec, no el código generado.**
>
> Lo dice GitHub en su blog del 2 de septiembre de 2025, cuando lanzaron Spec Kit: *'We're moving from "code is the source of truth" to "intent is the source of truth." With AI the specification becomes the source of truth and determines what gets built. This isn't because documentation became more important. It's because AI makes specifications executable.'*
>
> Esa última frase es la que tiene que quedarles: **la spec se volvió ejecutable**. Eso cambia todo. Una spec antes era un Word que nadie leía. Hoy es un artefacto que el agente lee, plan-ea, divide en tareas e implementa. **Es el equivalente a cuando pasamos de scripts bash sueltos a Terraform: el ciclo de revisión, plan, apply, drift detection ahora existe para el código de aplicación también.**"

**Minuto 26–36 — DEMO EN VIVO 1: vibe coding → "ahora escribime la spec"**

> "Vamos a probarlo. Abro Claude Code. Le voy a pedir vibe coding puro y duro: 'Hacé un endpoint Flask que reciba un POST con un JSON, lo valide, lo guarde en SQLite y devuelva un ID.'"

*[Demo en vivo. El instructor escribe el prompt, ve a Claude Code generar todo a las apuradas. 4–5 minutos.]*

> "Listo. Funciona. ¿Pero qué tenés? Tenés un archivo que vos no leíste, dependencias que el agente eligió, un esquema de BD que el agente decidió, validación que el agente decidió, manejo de errores que el agente decidió. **Si mañana querés reproducir esto en otro lenguaje o con otra base, no podés. Y eso es exactamente la deuda que vibe coding genera a escala.**
>
> Ahora viene la parte interesante. Le pido a Claude Code: *'Ahora generame la spec de lo que acabás de hacer: requirements funcionales, edge cases, dependencias y supuestos. Formato Markdown.'*"

*[El agente genera un spec.md decente en ~30 segundos.]*

> "Mirá lo que pasó. **El mismo agente que acaba de "vibe-codear" me acaba de dar el artefacto que necesitábamos al principio.** Y esto es la intuición clave de SDD: si la spec puede generarse al final, también puede dirigir el desarrollo desde el principio. Y si dirige desde el principio, **es reproducible, revisable y versionable.** Esa spec.md la puedo meter en un repo, hacerle PR review, y la semana que viene re-implementarla en Go o en Rust si quiero. Eso es el equivalente a tener tu infra en HCL versus haberla clickeado a mano."

**Minuto 36–38 — Cierre del bloque y bridge a Spec Kit**

> "GitHub publicó **Spec Kit** en septiembre 2025 como toolkit open-source de SDD. Tiene 92.4k stars y 8k+ forks al 5 de mayo de 2026 (star-history.com, corroborado por MarkTechPost), y soporta más de 30 agentes — Claude Code, Copilot, Gemini CLI, Cursor, Codex, Windsurf, etc. El flujo canónico es: **constitution → specify → clarify → plan → tasks → analyze → implement**, todo como slash commands. La semana que viene lo usamos en el workshop con las manos en el teclado. **Para hoy, lo único que necesitan llevarse es la intuición: la spec gobierna, el código es output.**"

---

### Break (00:38–00:43) — 5 min

---

### Bloque 2.3 (00:43–01:03) — MCPs y Tools (20 min)

**Minuto 43–47 — El problema M×N que MCP resuelve**

> "Antes de MCP, conectar un agente a una herramienta externa era el clásico problema M×N. Si tenés 3 modelos y 10 herramientas (Slack, Postgres, GitHub, Jira, etc.), tenés 30 integraciones custom para mantener. Cada una con su auth, su schema, su error handling. **Esto es exactamente el mismo problema que resuelve un service mesh: en vez de N² conexiones, una abstracción común.**
>
> **Model Context Protocol es ese estándar.** Lo lanzó Anthropic el 25 de noviembre de 2024. Es un protocolo JSON-RPC 2.0 sobre transportes intercambiables (stdio o Streamable HTTP), inspirado en el Language Server Protocol que usa VS Code. La frase oficial: *'MCP is the USB-C of AI.'* Un servidor MCP se escribe una vez y cualquier host MCP-compatible (Claude, ChatGPT, Cursor, VS Code, Zed, Replit) lo puede usar."

**Minuto 47–51 — Estado del protocolo en junio 2026**

> "Datos verificados al 2 de junio de 2026:
> - **Versión estable del spec: 2025-11-25**. Esa es la que están corriendo todos los SDKs en producción.
> - **Release Candidate: 2026-07-28**, lockeado el 21 de mayo de 2026, final programado para el 28 de julio. Cambio grande: **core stateless**, extensions framework, MCP Apps (UI server-rendered), Tasks extension, OAuth 2.1 más estricto.
> - **Governance:** el 9 de diciembre de 2025 Anthropic donó MCP a la **Agentic AI Foundation**, un directed fund del Linux Foundation, co-fundado con Block y OpenAI, con apoyo de Google, Microsoft, AWS, Cloudflare y Bloomberg.
> - **Adopción:** OpenAI lo adoptó oficialmente el 26 de marzo de 2025 (anuncio de Sam Altman). Hoy lo soportan Claude Desktop, Claude Code, ChatGPT, Cursor, VS Code, Zed, Replit.
> - **Ecosistema:** más de **10.000 servidores MCP públicos activos**, según el anuncio AAIF/Linux Foundation de Anthropic del 9 de diciembre de 2025; el MCP Registry API contaba 9.652 server records al 24 de mayo de 2026 (registry.modelcontextprotocol.io).
>
> **Para ustedes como MLOps esto importa por una sola razón: dejó de ser un protocolo de un solo vendor. Es un estándar de industria con governance formal.** Es seguro apostar infra a esto."

**Minuto 51–54 — Cómo funcionan tools en MCP**

> "Un servidor MCP expone tres primitivas:
> - **Tools** — funciones que el modelo puede invocar (query a DB, mandar email, crear issue en GitHub). El modelo decide cuándo llamarlas. Las describe con name, description y JSON Schema de inputs.
> - **Resources** — data que el modelo puede *leer* (archivos, registros de DB, configs). Identificadas por URI.
> - **Prompts** — templates reutilizables que el host puede ofrecer al usuario como slash commands.
>
> El handshake va así: el cliente arranca, llama `initialize`, el servidor responde con sus capabilities, el cliente lista las tools con `tools/list`, el modelo decide qué invocar con `tools/call`. **Para los que vienen de gRPC, es básicamente lo mismo: contract-first, capability discovery, request/response tipado.**"

**Minuto 54–62 — DEMO EN VIVO 2: agregar un MCP server a Claude Code**

> "Vamos a agregar el filesystem server oficial de Anthropic a Claude Code. Comando único:"

```bash
claude mcp add filesystem -s user -- npx -y @modelcontextprotocol/server-filesystem ~/Documents ~/Desktop
```

> "Lo que hago acá: `claude mcp add` agrega un server, `filesystem` es el nombre, `-s user` lo hace disponible en todos mis proyectos, `--` separa el comando que arranca el server, y los dos paths son los directorios que le doy acceso. Lo verifico con `claude mcp list` y dentro de la sesión con `/mcp`."

*[Demo: muestra `claude mcp list`, abre Claude Code, hace `/mcp`, ve el server conectado con sus tools (read_file, write_file, list_directory, etc.). Le pide al agente: 'Listame los .md de ~/Documents y resumime el más nuevo'. El agente invoca las tools, muestra los logs.]*

> "Mirá lo que está pasando bajo el capó: el modelo NO conoce mi filesystem. Lo descubre por el protocolo. Si mañana cambio el server por uno que apunta a S3, **el modelo no cambia y mi prompt no cambia**. Esa es la abstracción.
>
> Lo mismo se puede hacer con servers HTTP remotos:"

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport http stripe https://mcp.stripe.com
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

> "Estos son servers remotos oficiales, con OAuth 2.1. La autenticación la maneja Claude Code via `/mcp` cuando hacés el primer uso."

**Minuto 62–63 — Por qué esto cambia las reglas del juego**

> "Antes: cada equipo escribía su propio adapter para conectar el LLM a su backend. Hoy: escribís un MCP server una vez (Python con `fastmcp`, TypeScript con `@modelcontextprotocol/sdk`, etc.), y lo usás en cualquier host. **Es la misma lógica de cuando pasamos de drivers JDBC custom a una capa estándar. El costo marginal de integrar una herramienta nueva colapsa.**"

---

### Bloque 2.4 (01:03–01:20) — Claude Skills (17 min)

**Minuto 63–67 — Qué son Skills y por qué nacieron**

> "Anthropic anunció **Claude Skills** el **16 de octubre de 2025**. La gente que se la pasa probando todo, como Simon Willison, los describió como '*maybe a bigger deal than MCP*'. Vamos a ver por qué.
>
> Un Skill es una **carpeta** con un archivo `SKILL.md` adentro. El SKILL.md tiene YAML frontmatter (mínimo: `name` y `description`) y debajo, instrucciones en Markdown. Eso es todo. Es texto plano versionable.
>
> El truco está en cómo se carga. Al arrancar la sesión, Claude escanea todos los skills disponibles y lee SOLO el frontmatter de cada uno (~30-50 tokens por skill). Cuando vos le pedís algo, Claude evalúa si alguno matchea con la descripción y, si sí, **carga el SKILL.md completo en contexto**. Si el skill tiene archivos auxiliares (scripts, references, assets), los carga *solo si los necesita*. **Esto se llama 'progressive disclosure' y es la idea fuerte: cero overhead de contexto hasta que el skill se necesita de verdad.**"

**Minuto 67–70 — Skills vs MCP: la distinción que tienen que entender**

> "Esta confusión la veo mucho. Memorícenla así:
> - **MCP te da conectividad.** Es el 'cómo' técnico — cómo hablás con Stripe, con Postgres, con GitHub.
> - **Skills te dan procedimiento.** Es el 'cómo' organizacional — cómo *tu equipo* escribe un release note, cómo *tu empresa* genera un informe financiero, cómo aplicar tu style guide.
>
> En MLOps lo veo así: **MCP es como tu Terraform provider — te da las primitivas para hablar con un cloud. Skill es como tu módulo de Terraform — encapsula la convención de tu equipo de cómo se levanta un EKS cluster en tu org.**
>
> Y se combinan: un skill puede invocar tools de un MCP. La combinación más potente es 'MCP para conectar + Skill para enseñar cómo usar esa conexión correctamente'."

**Minuto 70–72 — Estructura formal de un Skill**

> "El layout estándar, sacado de github.com/anthropics/skills:
>
> ```
> my-skill/
> ├── SKILL.md          # Required: YAML frontmatter + instructions
> ├── references/       # Optional: docs cargados on-demand
> ├── scripts/          # Optional: scripts ejecutables
> ├── assets/           # Optional: templates, logos, fonts
> └── evals/            # Recommended: evaluation tests
> ```
>
> En Claude Code los Skills viven en `~/.claude/skills/<nombre>/` (personal) o `.claude/skills/<nombre>/` (proyecto). La doc oficial dice, literal: *'Claude Code watches skill directories for file changes. Adding, editing, or removing a skill under ~/.claude/skills/ takes effect within the current session without restarting.'* **Hot reload incluido.**"

**Minuto 72–78 — DEMO EN VIVO 3: crear un Skill en Claude Code**

> "Vamos a crear un Skill llamado `release-notes` que enseñe a Claude a generar release notes con el formato de nuestra empresa imaginaria."

```bash
mkdir -p ~/.claude/skills/release-notes
```

Y escribimos `~/.claude/skills/release-notes/SKILL.md`:

```markdown
---
name: release-notes
description: Genera release notes con el formato estándar de DataCorp. Usar siempre que el usuario pida release notes, changelog, notas de versión, o pida resumir cambios entre tags de git para una release.
---

# Release Notes — DataCorp Standard

## Iron Law
SIEMPRE seguir esta estructura. NO inventar secciones nuevas.

## Estructura obligatoria
1. **Header:** `## vX.Y.Z — YYYY-MM-DD`
2. **Highlights:** 3 bullets máximo, una línea cada uno.
3. **Breaking Changes:** lista o `Ninguno`.
4. **New Features:** bullets con [JIRA-XXXX] al final.
5. **Bug Fixes:** bullets con [JIRA-XXXX] al final.
6. **Internal:** cambios sin impacto en usuarios.

## Procedimiento
1. Correr `git log <prev-tag>..HEAD --oneline` para listar commits.
2. Agrupar por convención de commits (feat:, fix:, chore:, etc.).
3. Aplicar el formato de arriba.
4. NO incluir merges de PRs sin ticket de JIRA.

## Ejemplos
- ✅ `- Soporte para autenticación SAML en el dashboard [DCP-1234]`
- ❌ `- Added some auth stuff`
```

> "Listo. Recargo la sesión, escribo: *'Generame las release notes desde el tag v2.3.0 hasta HEAD.'* Claude ve la descripción del skill, matchea, carga el SKILL.md completo, sigue el procedimiento al pie de la letra."

*[Demo en vivo: Claude Code carga el skill automáticamente — en el panel se ve `release-notes` activado — y genera output siguiendo la estructura.]*

> "Tres cosas que quiero que noten:
> 1. **No usé prompt engineering en mi mensaje.** Toda la inteligencia está en el skill, versionada en disco.
> 2. **El skill es portable.** Lo puedo commitear al repo en `.claude/skills/` y todo el equipo lo hereda. Si nuestra convención cambia, hago un PR al SKILL.md.
> 3. **Skills es un open standard.** Anthropic publicó el spec en agentskills.io el 18 de diciembre de 2025. El mismo skill, en principio, anda en Claude Code, Codex CLI, Cursor, Gemini CLI."

**Minuto 78–80 — Cómo encajan los Skills en el flujo MLOps**

> "Piensen los Skills como los **playbooks** o los **roles de Ansible** que ya manejan. Cada skill encapsula una capacidad procedimental que tu organización quiere consistencia. Versionado en git, code-review-able, hot-reloadable. Es la pieza que faltaba para que los agentes dejen de ser un juguete y pasen a ser una capa más de tu stack de DevEx."

---

### Bloque 2.5 (01:20–01:30) — Cierre y puente al workshop (10 min)

**Minuto 80–84 — Síntesis de la clase**

> "Resumen rápido de lo que vimos hoy:
>
> **1) El mapa de LLMs en mid-2026:** Claude lidera coding agéntico (Opus 4.8 al 88.6% en SWE-bench Verified), GPT-5.5 lidera multimodal/breadth, Gemini 3.5 Flash es el value play en Google Cloud, los chinos (Qwen 3.7 Max, DeepSeek V4) son competitivos a fracción del costo. Default a Sonnet 4.6, reservá Opus para los problemas duros.
>
> **2) Vibe coding vs SDD:** vibe coding es deploy a mano por SSH, SDD es Terraform. La spec es el contrato ejecutable. *'Specifications don't serve code — code serves specifications.'* Spec Kit de GitHub es la herramienta canónica.
>
> **3) MCP:** el USB-C de los agentes. Spec estable 2025-11-25, RC 2026-07-28. Governance en Linux Foundation desde diciembre 2025. Más de 10.000 servers públicos. Te elimina el M×N integration problem.
>
> **4) Skills:** carpetas con SKILL.md que enseñan procedimientos a Claude con progressive disclosure. Versionables, portables, open standard."

**Minuto 84–88 — La idea fuerza**

> "Si tienen que llevarse UNA sola cosa de hoy, es esta:
>
> **La diferencia no está en la herramienta, está en el proceso.**
>
> Cualquiera puede instalar Claude Code. Lo que separa al equipo que va a escalar del equipo que va a chocar contra el muro de la deuda técnica es: **¿tu spec es la fuente de verdad, o lo es tu chat history con el agente?**
>
> Vibe coding está bien para el viernes a la noche. SDD es lo que te permite producción. MCP te da las primitivas. Skills te da la convención. **Las cuatro piezas juntas son la versión 2026 de lo que para ustedes hace 10 años fue pasar de scripts bash a CI/CD declarativo.**"

**Minuto 88–90 — Bridge al workshop**

> "La semana que viene es 100% hands-on. Tres cosas vamos a hacer:
>
> **1)** Instalar Spec Kit y correr el flujo completo `constitution → specify → clarify → plan → tasks → analyze → implement` en un proyecto real.
> **2)** Construir un Skill propio usando SDD — sí, vamos a aplicar SDD a la construcción del Skill, así sienten en carne propia el doble bucle.
> **3)** Diseñar **un flujo SDD custom** adaptado a la realidad de su empresa: presets, extensions, validaciones, gates. Porque Spec Kit es la base; vos sobre eso construís el SDD de tu org.
>
> Trayanse Claude Code instalado y actualizado (versión 2.1+), una API key de Anthropic, y un repo de un proyecto chico real al que se animen a meterle la motosierra. **La diferencia no está en la herramienta. Lo probamos en vivo, la semana que viene.**"

---

## 3) Esquema de slides (slide por slide)

### Slide 0 — Título
- Clase 2 · Estado actual, herramientas y Skills
- Curso Applied AI · 90 min · Parte 2
- [tu nombre] · 2026

### Slide 1 — Agenda
- 2.1 El mapa actual de LLMs (15 min)
- 2.2 Vibe coding vs SDD (20 min)
- *Break (5 min)*
- 2.3 MCPs y Tools (20 min)
- 2.4 Claude Skills (17 min)
- 2.5 Cierre y puente al workshop (10 min)

### Slide 2 — Recap clase 1
- LLM = predictor de tokens
- Embeddings = representación densa
- Transformer = attention + capas
- Agent loop = LLM + tools + memoria
- Hoy: estado del arte y herramientas

### Slide 2.1.A — Por qué un mapa
- Elegir LLM = elegir vendor + pricing + latencia + data residency + roadmap
- Mismo problema que elegir DB managed vs self-hosted
- Cambia rápido: este slide tiene fecha de vencimiento

### Slide 2.1.B — Tabla comparativa (slide-tabla principal)

| Proveedor | Flagship (jun 2026) | Sweet spot | Costo $/M tok (in/out) | Open? |
|---|---|---|---|---|
| Anthropic | Claude Opus 4.8 (may 2026) | Coding agéntico, long-horizon | Opus 4.8: premium · Sonnet 4.6: $3/$15 | No |
| OpenAI | GPT-5.5 (abr 2026) | Multimodal, breadth, Codex | $5/$30 | No |
| Google | Gemini 3.5 Flash + 3.1 Pro | Multimodal, GCP integration, costo | Flash: muy bajo | No |
| Meta | Muse Spark (abr 2026) · Llama 4 | Open-weights, self-host | Gratis (infra propia) | Sí |
| DeepSeek | V3.2 / V4 (mar 2026) | Reasoning, costo extremo bajo | $0.28/$0.42 | Sí (MIT) |
| Alibaba/Qwen | Qwen 3.7 Max (may 2026) | Agentes long-horizon, 1M ctx | $2.50/$7.50 | Max: no · 3.6: Apache 2.0 |

### Slide 2.1.C — Benchmarks: qué mirar
- **SWE-bench Verified** = 500 issues reales de GitHub, validados por humanos
- Top al 28-may-2026 (fuente: BenchLM.ai):
  - Claude Mythos Preview: 93.9%
  - Claude Opus 4.8: 88.6%
  - Claude Opus 4.7 Adaptive: 87.6%
  - Sonnet 4.6: 79.6% · Opus 4.6: 80.8%
- ⚠️ OpenAI dejó de reportar Verified en 2026 — recomienda **SWE-bench Pro** (harder, contamination-resistant)
- Mismos modelos: -35 puntos al pasar de Verified a Pro
- Benchmark = dirección, no precisión

### Slide 2.1.D — Heurísticas de elección (regla de 3)
- Default a Sonnet 4.6 / Gemini Flash / GPT-5.4 mini para 80% del trabajo
- Reservá flagship (Opus 4.8 / GPT-5.5 Pro) para los problemas donde el costo extra está justificado
- Tené un plan B open-weights (Qwen 3.6, DeepSeek V4, Llama) para data residency y cost extremo

### Slide 2.2.A — Vibe coding
- Término acuñado por Andrej Karpathy, 2 de febrero de 2025
- *"Fully give in to the vibes, embrace exponentials, and forget that the code even exists"*
- Collins Word of the Year, anunciada 6-nov-2025
- **= deploy a mano por SSH**
- OK para prototipo del viernes. NO para producción.

### Slide 2.2.B — Por qué vibe coding no escala
- CodeRabbit (17-dic-2025, 470 PRs analizados): código IA-coautoreado tiene **1.4× más issues críticos y 1.7× más issues mayores** que código humano
- Veracode (oct 2025): solo GPT-5 Mini mejoró seguridad (72% pass rate); Anthropic, Google, Qwen, xAI no mostraron mejoras significativas
- Veracode (jul 2025): **45% del código generado por IA introduce vulnerabilidades del OWASP Top 10**
- Falta: reproducibilidad, revisión, versión, rollback
- Es el equivalente a tener tu infra en clicks de consola

### Slide 2.2.C — Spec-Driven Development
- **SDD = Infrastructure-as-Code para tu código**
- spec.md = HCL · plan = `terraform plan` · implement = `terraform apply`
- Lo que gobierna es la **spec**, no el código
- GitHub blog (2-sep-2025): *"Specifications don't serve code — code serves specifications."*
- *"AI makes specifications executable"*

### Slide 2.2.D — Spec Kit en una slide
- Toolkit open-source de GitHub para SDD (sep 2025)
- Repo: github/spec-kit · **92.4k stars · 8k+ forks** (5-may-2026, star-history.com)
- Soporta 30+ agentes (Claude Code, Copilot, Gemini, Cursor, Codex, Windsurf, Kiro, etc.)
- Flujo canónico (slash commands):
  - `/speckit.constitution` → principios no-negociables
  - `/speckit.specify` → qué construir (requirements)
  - `/speckit.clarify` → resolver ambigüedades
  - `/speckit.plan` → plan técnico (tech stack)
  - `/speckit.tasks` → lista de tareas ejecutable
  - `/speckit.analyze` → consistencia entre artefactos
  - `/speckit.implement` → ejecutar las tareas

### Slide 2.2.E — DEMO 1
- Live demo: vibe coding rápido en Claude Code → "ahora generame la spec"
- Take-away: la misma spec que el agente generó al final, **puede dirigir el desarrollo desde el principio**

### Slide 2.3.A — El problema M×N
- 3 modelos × 10 tools = 30 integraciones custom
- Cada una con auth, schema, error handling propios
- Insostenible

### Slide 2.3.B — MCP en una slide
- **Model Context Protocol** — Anthropic, 25-nov-2024
- JSON-RPC 2.0 sobre stdio o Streamable HTTP
- *"The USB-C of AI"*
- Inspirado en LSP de VS Code: write once, plug anywhere
- Adopción: Anthropic, OpenAI (mar 2025, Sam Altman), Cursor, VS Code, Zed, Replit
- **>10.000 servers públicos activos** (Anthropic / Linux Foundation, 9-dic-2025; 9.652 server records en el MCP Registry al 24-may-2026)

### Slide 2.3.C — Estado al 2 de junio de 2026
- Spec **estable: 2025-11-25**
- **RC: 2026-07-28** (locked 21-may-2026, final 28-jul-2026)
  - Core stateless
  - Extensions framework
  - MCP Apps (UI server-rendered)
  - Tasks extension
  - OAuth 2.1 hardening
- **Governance:** donado a **Agentic AI Foundation** (Linux Foundation) el **9-dic-2025**
  - Co-founders: Anthropic, Block, OpenAI
  - Supporters: Google, Microsoft, AWS, Cloudflare, Bloomberg

### Slide 2.3.D — Las 3 primitivas
- **Tools** = funciones invocables por el modelo (DB query, API call, side-effect)
- **Resources** = data leíble por el modelo (archivos, registros, configs, URI)
- **Prompts** = templates / slash commands

### Slide 2.3.E — DEMO 2: `claude mcp add`
```bash
# Filesystem oficial (local, stdio)
claude mcp add filesystem -s user -- \
  npx -y @modelcontextprotocol/server-filesystem ~/Documents ~/Desktop

# Servers HTTP remotos (oficiales)
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport http stripe https://mcp.stripe.com
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```
- Listar: `claude mcp list` / dentro de sesión `/mcp`
- Scope: `-s user` (global) · `-s project` (`.mcp.json` versionado) · default = local

### Slide 2.3.F — Por qué cambia las reglas
- Costo marginal de integrar una tool nueva → colapsa
- El mismo MCP server anda en cualquier host compatible
- = pasar de drivers JDBC custom a una capa estándar

### Slide 2.4.A — Claude Skills en una slide
- Anunciado **16-oct-2025** por Anthropic
- Una carpeta con un `SKILL.md` adentro
- YAML frontmatter (`name`, `description`) + instrucciones Markdown
- **Progressive disclosure:** solo se carga la descripción (~30-50 tokens); el body se carga si matchea; los archivos auxiliares se cargan solo si se usan
- *"Maybe a bigger deal than MCP"* — Simon Willison

### Slide 2.4.B — Skills vs MCP (la slide que vale oro)

| | MCP | Skills |
|---|---|---|
| **Da...** | Conectividad (cómo técnico) | Procedimiento (cómo organizacional) |
| **Análogo MLOps** | Terraform provider | Módulo de Terraform / playbook Ansible |
| **Ejemplo** | "Cómo hablo con Stripe" | "Cómo *mi equipo* hace un refund" |
| **Formato** | JSON-RPC server | Carpeta con SKILL.md |
| **Combinable** | ✅ Skill puede invocar tools MCP | ✅ |

### Slide 2.4.C — Estructura de un Skill
```
my-skill/
├── SKILL.md          # Required: frontmatter + instructions
├── references/       # Optional: docs cargados on-demand
├── scripts/          # Optional: scripts ejecutables
├── assets/           # Optional: templates, logos
└── evals/            # Recommended: tests
```
- Personal: `~/.claude/skills/<nombre>/`
- Proyecto: `.claude/skills/<nombre>/`
- Hot-reload sin reiniciar la sesión

### Slide 2.4.D — DEMO 3: SKILL.md mínimo
```yaml
---
name: release-notes
description: Genera release notes con formato DataCorp.
  Usar siempre que se pidan release notes, changelog,
  notas de versión, o resumir cambios entre tags.
---

# Release Notes — DataCorp Standard
## Iron Law
...
```
- Descripción "pushy": Anthropic recomienda explícitamente describir cuándo disparar el skill, porque la tendencia es a "under-triggering"

### Slide 2.4.E — Skills es open standard
- Spec publicado en **agentskills.io** el 18-dic-2025
- Soporte: Claude.ai, Claude Code, Claude Agent SDK, Claude API
- Adoptado/portable a: OpenAI Codex CLI, Cursor, Gemini CLI, GitHub Copilot (open standard)

### Slide 2.5.A — Las 4 piezas juntas
- **Mapa de LLMs** → elegí el motor con criterio
- **SDD** → la spec gobierna, el código es output
- **MCP** → conectividad estándar a todo
- **Skills** → procedimientos versionables del equipo

### Slide 2.5.B — La idea fuerza
- **La diferencia no está en la herramienta, está en el proceso.**
- ¿Tu spec es la fuente de verdad, o lo es tu chat history con el agente?
- Vibe coding = viernes a la noche. SDD = producción.
- Lo probamos en vivo la semana que viene.

### Slide 2.5.C — Workshop semana próxima
- Hands-on, 100% teclado.
- **1)** Spec Kit flow completo en un proyecto real
- **2)** Construir un Skill aplicando SDD
- **3)** Diseñar un flujo SDD custom para tu org
- Traer: Claude Code 2.1+, API key Anthropic, un repo chico real

---

## 4) Apéndice de ejemplos prácticos (ejecutables y verificados al 2 de junio de 2026)

### Apéndice A — Spec Kit: flujo completo

**A.1. Instalación one-time (sin instalar el CLI persistente):**

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init my-project --integration claude
```

Prerequisitos: Python 3.11+ y [uv](https://docs.astral.sh/uv/) instalados.

**A.2. Instalación persistente (recomendado para uso recurrente):**

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify init my-project --integration claude
```

Flags útiles:
- `--integration claude` → Claude Code (también: `copilot`, `gemini`, `cursor`, `codex`, `windsurf`, `kiro`, `forge`, etc.)
- `--here` o `.` → inicializar en directorio actual
- `--force` → mergear sobre directorio no vacío
- `--no-git` → saltear init de git
- `--script ps` (Windows PowerShell) | `--script sh` (POSIX)
- `--integration-options="--skills"` → instalar como Agent Skills en vez de slash commands (para integraciones que lo soporten)

**A.3. Estructura generada:**

```
my-project/
├── .specify/
│   ├── memory/
│   │   └── constitution.md            # tras /speckit.constitution
│   ├── scripts/
│   │   └── bash/                       # (o powershell/)
│   │       ├── check-prerequisites.sh
│   │       ├── common.sh
│   │       ├── create-new-feature.sh
│   │       ├── setup-plan.sh
│   │       └── setup-tasks.sh
│   └── templates/
│       ├── plan-template.md
│       ├── spec-template.md
│       └── tasks-template.md
├── .claude/                            # commands/skills para Claude Code
│   └── commands/                       # o skills/ si se usó --skills mode
└── specs/                              # se llena con cada feature
    └── 001-create-taskify/             # creado por /speckit.specify
        ├── spec.md
        ├── plan.md                     # tras /speckit.plan
        ├── data-model.md
        ├── research.md
        ├── quickstart.md
        ├── contracts/
        │   ├── api-spec.json
        │   └── signalr-spec.md
        └── tasks.md                    # tras /speckit.tasks
```

**A.4. Flujo canónico de slash commands (dentro de Claude Code, en orden):**

```
/speckit.constitution
/speckit.specify   <descripción en prosa de lo que querés>
/speckit.clarify
/speckit.plan      <stack técnico: .NET Aspire + Postgres + Blazor>
/speckit.tasks
/speckit.analyze
/speckit.implement
```

Comandos opcionales útiles:
- `/speckit.checklist` — genera quality checklists ("unit tests for English")
- `/speckit.taskstoissues` — convierte el tasks.md en issues de GitHub

**A.5. Ejemplo corto de una spec inicial (lo que va dentro de `/speckit.specify`):**

```text
Build Taskify — una plataforma de productividad para equipos chicos.
Permite crear proyectos, agregar miembros, asignar tareas, comentar
y mover tareas entre columnas estilo Kanban.

En esta primera fase ("Create Taskify"):
- 5 usuarios predefinidos: 1 product manager + 4 engineers
- 3 proyectos de muestra
- Columnas Kanban estándar: To Do, In Progress, In Review, Done
- Drag & drop entre columnas
- Comentarios por tarea
- No incluir auth real en esta fase (usuarios hard-coded)
```

**A.6. SDD custom por empresa — preset:**

Spec Kit permite presets que sobreescriben templates y agregan gates. Para tu org podés:

```bash
specify preset add <preset-name>
# o crear el tuyo propio editando .specify/templates/overrides/
```

Ejemplo de uso: un preset `compliance` que mete validación de PII y traceability regulatoria como gates obligatorios en cada `/speckit.analyze`.

```bash
specify init my-project --integration claude --preset compliance
```

---

### Apéndice B — MCP con Claude Code

**B.1. Verificar la versión:**

```bash
claude --version    # 2.1+ al 2 de junio de 2026
```

**B.2. Agregar el filesystem server (oficial, stdio, local):**

```bash
claude mcp add filesystem -s user -- \
  npx -y @modelcontextprotocol/server-filesystem ~/Documents ~/Desktop
```

Verificar:

```bash
claude mcp list
# Dentro de Claude Code:
# /mcp
```

**B.3. Servers HTTP remotos oficiales (con OAuth 2.1):**

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport http stripe https://mcp.stripe.com
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

**B.4. GitHub MCP server (stdio, con env var):**

```bash
claude mcp add github -s user \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here -- \
  npx -y @modelcontextprotocol/server-github
```

**B.5. Versión versionada por proyecto (`.mcp.json` en la raíz, commiteable):**

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "${DATABASE_URL}"]
    },
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PAT}"
      }
    }
  }
}
```

Sintaxis `${VAR}` y `${VAR:-default}` soportadas en `command`, `args`, `env`, `url`, `headers`.

**B.6. Escribir tu propio MCP server (Python, en 10 líneas con `fastmcp`):**

```python
# server.py
from fastmcp import FastMCP

mcp = FastMCP(name="Inventory")

@mcp.tool
def get_stock(sku: str) -> int:
    """Returns current stock for a given SKU."""
    # ...query a tu DB real...
    return 42

if __name__ == "__main__":
    mcp.run()
```

Instalarlo en Claude Code:

```bash
fastmcp install claude-code server.py --with sqlalchemy --with psycopg2
```

---

### Apéndice C — Claude Skill mínimo

**C.1. Template oficial (de `anthropics/skills`):**

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here that Claude will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

**C.2. Skill funcional completo — `release-notes`:**

Ubicación: `~/.claude/skills/release-notes/SKILL.md`

```markdown
---
name: release-notes
description: Genera release notes con el formato estándar de DataCorp.
  Usar siempre que el usuario pida release notes, changelog, notas de versión,
  o pida resumir cambios entre tags de git para una release. Disparar
  incluso si el usuario no usa la palabra "release notes" literalmente
  pero pide un resumen de cambios versión-a-versión.
---

# Release Notes — DataCorp Standard

## Iron Law
SIEMPRE seguir la estructura de abajo. NO inventar secciones nuevas.
NO incluir merges de PRs que no tengan ticket de JIRA asociado.

## Estructura obligatoria

## vX.Y.Z — YYYY-MM-DD

**Highlights** (3 bullets máximo, una línea cada uno)
- ...

**Breaking Changes**
- ...  (o el literal `Ninguno`)

**New Features**
- Descripción [JIRA-XXXX]

**Bug Fixes**
- Descripción [JIRA-XXXX]

**Internal**
- Cambios sin impacto en usuarios finales

## Procedimiento

1. Correr `git log <prev-tag>..HEAD --oneline` para listar commits.
2. Agrupar por convención de commits:
   - `feat:` → New Features
   - `fix:` → Bug Fixes
   - `chore:`, `refactor:`, `test:` → Internal
   - Cualquier cosa marcada con `BREAKING CHANGE:` → Breaking Changes
3. Extraer ticket de JIRA del título del commit o de la rama.
4. Si un commit no tiene ticket → preguntar al usuario, no inventar.
5. Aplicar el formato de arriba.

## Ejemplos

- ✅ `- Soporte para autenticación SAML en el dashboard [DCP-1234]`
- ❌ `- Added some auth stuff`
- ❌ `- Refactored some files (Merge pull request #4321)`
```

**C.3. Invocación:**

Dentro de Claude Code, simplemente:

```
Generame las release notes desde el tag v2.3.0 hasta HEAD.
```

Claude detecta el match con la `description`, carga el SKILL.md completo y sigue el procedimiento al pie de la letra. **No hace falta nombrar el skill explícitamente.**

**C.4. Skill con scripts auxiliares (progressive disclosure):**

Cuando el skill crece, separá:

```
~/.claude/skills/release-notes/
├── SKILL.md
├── scripts/
│   └── group_commits.py        # script Python invocable por Claude
├── references/
│   ├── jira-mappings.md         # tablas de proyectos JIRA
│   └── breaking-change-policy.md
└── assets/
    └── release-note-template.md
```

Desde `SKILL.md` referenciás los archivos cuando los necesitás:

```markdown
Para casos complejos (más de 50 commits), correr `scripts/group_commits.py`
en vez de procesar manualmente. Para mapeo de prefijos de commits a
proyectos de JIRA, consultar `references/jira-mappings.md`.
```

Claude carga esos archivos SOLO cuando los necesita.

**C.5. Skill versionado por proyecto (compartido por el equipo):**

```
mi-repo/
├── .claude/
│   └── skills/
│       └── release-notes/
│           └── SKILL.md
└── ... (tu código)
```

Commiteás `.claude/skills/` al repo y todo el equipo lo hereda automáticamente. Cualquier cambio a la convención es un PR al SKILL.md, con su code review.

---

## 5) Notas finales del instructor (fuentes primarias y caveats date-sensitive)

### Fuentes primarias verificadas (con fecha de consulta: 2 de junio de 2026)

**LLMs y modelos:**
- Anthropic — Models overview: https://platform.claude.com/docs/en/about-claude/models/overview (Claude Opus 4.8 al 28-may-2026)
- OpenAI — Introducing GPT-5.5: https://openai.com/index/introducing-gpt-5-5/ (23-abr-2026)
- OpenAI — GPT-5.5 Instant: https://openai.com/index/gpt-5-5-instant/ (5-may-2026)
- Google DeepMind — Gemini 3.5: https://deepmind.google/models/gemini/
- Meta / Llama: https://www.llama.com/ (Llama 4 sigue como referencia open-weights principal hasta Muse Spark, abril 2026)
- DeepSeek API changelog: https://api-docs.deepseek.com/updates
- Qwen 3.7 Max — confirmado por Alibaba Cloud Summit, 20-may-2026

**Benchmarks:**
- SWE-bench Verified leaderboard (BenchLM.ai, 28-may-2026): https://benchlm.ai/benchmarks/sweVerified
- SWE-bench oficial: https://www.swebench.com
- LLM Stats SWE-Bench Verified: https://llm-stats.com/benchmarks/swe-bench-verified
- CodeRabbit — *State of AI vs Human Code Generation* report (Business Wire, 17-dic-2025; 470 PRs, 320 IA-coautoreados vs 150 humanos)
- Veracode — *GPT-5 Pulls Ahead on Secure Code While Rivals Stall* (oct-2025) y *2025 GenAI Code Security Report* (jul-2025)

**Vibe coding y SDD:**
- Andrej Karpathy original tweet, 2-feb-2025: https://x.com/karpathy/status/1886192184808149383
- Collins Dictionary blog — Word of the Year 2025 (6-nov-2025): https://www.collinsdictionary.com/woty
- Simon Willison — "Not all AI-assisted programming is vibe coding": https://simonwillison.net/2025/Mar/19/vibe-coding/
- GitHub Blog — Spec-driven development announcement (2-sep-2025): https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- GitHub Spec Kit repo: https://github.com/github/spec-kit (92.4k stars / 8k+ forks al 5-may-2026, vía star-history.com y MarkTechPost)
- Spec Kit docs: https://github.github.com/spec-kit/ (last updated 27-may-2026)
- Microsoft Dev blog: https://developer.microsoft.com/blog/spec-driven-development-spec-kit

**MCP:**
- MCP spec 2025-11-25 (stable): https://modelcontextprotocol.io/specification/2025-11-25
- MCP blog — 2026-07-28 RC: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
- MCP donado a la Agentic AI Foundation (9-dic-2025): https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
- MCP Registry (>10.000 servers; 9.652 records al 24-may-2026): https://registry.modelcontextprotocol.io
- Sam Altman / OpenAI adoptando MCP (26-mar-2025): TechCrunch coverage
- Anthropic original MCP announcement (25-nov-2024): https://www.anthropic.com

**Claude Skills:**
- Anthropic engineering blog — "Equipping agents for the real world with Agent Skills" (16-oct-2025): https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Claude API docs — Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Claude Code docs — Skills: https://code.claude.com/docs/en/skills
- anthropics/skills repo: https://github.com/anthropics/skills
- Simon Willison — "Claude Skills are awesome, maybe a bigger deal than MCP" (16-oct-2025): https://simonwillison.net/2025/Oct/16/claude-skills/
- Skills open standard: https://agentskills.io (publicado 18-dic-2025)

**Claude Code:**
- Docs: https://code.claude.com/docs/en/
- MCP en Claude Code: https://code.claude.com/docs/en/mcp
- Anthropic claude-code repo: https://github.com/anthropics/claude-code

### Caveats date-sensitive (advertir al alumno)

1. **El RC del MCP spec 2026-07-28 todavía no es final al 2 de junio de 2026.** Final scheduled 28-jul-2026. No lo presenten como producción.
2. **Los nombres de modelos cambian cada 4-8 semanas.** El "default" Sonnet 4.6 puede ser Sonnet 4.7 o 5.0 cuando den la clase. Revisar antes.
3. **OpenAI no reporta más SWE-bench Verified.** Si alguien les muestra un score de GPT-5.5 en Verified, es estimación de terceros (Tom's Guide, Scale AI), no reportado oficialmente.
4. **Muse Spark de Meta (abril 2026)** es novedoso y al momento de esta clase no tiene tantos casos de uso en producción como Llama. Mencionar pero no construir sobre él.
5. **Qwen 3.7 Max es closed-weights;** las versiones open siguen en Qwen 3.6 al 2-jun-2026. Si el alumno necesita open-weights chinos, derivar a Qwen 3.6 o DeepSeek.
6. **El comando exacto `--integration claude --integration-options="--skills"` no está verbatim en el README de Spec Kit** — está documentado el patrón genérico para integraciones que soportan skills mode. Probar antes de la clase.
7. **Los stars de Spec Kit (92.4k al 5-may-2026)** se mueven rápido — revisar el día de la clase para tener la cifra fresca.