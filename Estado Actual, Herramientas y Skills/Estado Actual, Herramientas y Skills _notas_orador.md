# Clase 2 — Notas al orador (guion diapositiva por diapositiva)

> **Uso:** estas son tus *cue cards*. Una mirada rápida por slide mientras hablás. No es para leer palabra por palabra — son los puntos que no te podés olvidar, los datos con fecha, y las señales de cuándo avanzar.
> **Duración total:** 90 min. **Registro:** voseo, directo, analogías DevOps/MLOps.
> **Leyenda:** ⏱ = tiempo objetivo · ▶ = cuándo avanzar · 🎯 = la frase que tiene que quedar · ⚠️ = dato sensible a fecha (revisar el día de la clase).

---

## Slide 0 — Título ⏱ 0:00–0:01
- Saludá, presentate corto. No te extiendas acá.
- "Segunda clase. Hoy bajamos a tierra."
- ▶ Avanzá apenas terminás de saludar.

## Slide 1 — Agenda ⏱ 0:01–0:02
- Recorré los 4 bloques en 20 segundos.
- Aclará: "la clase que viene es 100% workshop, con las manos en el teclado".
- ▶ Avanzá.

## Slide 2 — Recap clase 1 ⏱ 0:02–0:03
- Disparador rápido: "¿se acuerdan del agent loop? LLM + tools + memoria".
- No re-expliques. Es solo para reconectar.
- 🎯 "Hoy: estado del arte y herramientas que cambian cómo trabajamos."
- ▶ Avanzá al bloque 2.1.

---

# BLOQUE 2.1 — El mapa de LLMs ⏱ 0:03–0:18 (15 min)

## Slide 2.1.A — Por qué un mapa ⏱ 0:03–0:06
- Elegir LLM = elegir vendor + pricing + latencia + data residency + roadmap.
- Analogía: igual que elegir RDS vs Aurora vs Postgres self-hosted.
- 🎯 "El error más común en equipos MLOps es tratar a los LLMs como commodity intercambiable. No lo son."
- Avisá: "esto se mueve rapidísimo; importa la forma de pensar, no memorizar nombres".
- ▶ Avanzá a la tabla.

## Slide 2.1.B — Tabla comparativa ⏱ 0:06–0:12
- Recorré proveedor por proveedor, rápido (1 min c/u):
  - **Anthropic:** Opus 4.8 (28-may-2026) flagship; Sonnet 4.6 daily driver ($3/$15, 1M ctx); Haiku 4.5 barato/rápido. Domina coding.
  - **OpenAI:** GPT-5.5 (abr-2026), más caro ($5/$30), gana en multimodal/breadth.
  - **Google:** Gemini 3.5 Flash (value play) + 3.1 Pro (reasoning). Si están en GCP, Vertex te ahorra horas.
  - **Meta:** Llama estancada post-Llama 4; Muse Spark (abr-2026) es lo nuevo. Open-weights sólido sigue siendo Llama 4 Scout/Maverick.
  - **DeepSeek:** V3.2/V4, calidad cercana a GPT-4o a 1/10 del costo, MIT, open-weights.
  - **Qwen:** 3.7 Max (20-may-2026), 1M ctx, agentes long-horizon, #1 chino.
- Mencioná al pasar: Grok, Mistral, MiniMax, GLM-5, Kimi. "9 de los top 15 en SWE-bench son chinos."
- ⚠️ Revisá nombres/versiones el día de la clase — cambian cada 4-8 semanas.
- ▶ Avanzá a benchmarks.

## Slide 2.1.C — Benchmarks ⏱ 0:12–0:16
- Pregunta clave a enseñarles: "¿el mejor *en qué benchmark*?"
- SWE-bench Verified = 500 issues reales de GitHub validados por humanos.
- Top (28-may-2026, BenchLM.ai): Mythos Preview 93.9% · Opus 4.8 88.6% · Opus 4.7 Adaptive 87.6% · Sonnet 4.6 79.6%.
- ⚠️ OpenAI dejó de reportar Verified → recomienda SWE-bench Pro (harder).
- 🎯 "Mismos modelos bajan ~35 puntos de Verified a Pro. El benchmark da dirección, no precisión."
- Cierre del punto: "la métrica online real = ¿cuántos tickets de tu backlog resuelve sin intervención?"
- ▶ Avanzá a heurísticas.

## Slide 2.1.D — Heurísticas (regla de 3) ⏱ 0:16–0:18
- 1) Default a Sonnet 4.6 / Gemini Flash / GPT mini para el 80%.
- 2) Reservá flagship para los problemas duros.
- 3) Tené plan B open-weights (Qwen, DeepSeek, Llama) para data residency / costo.
- 🎯 "Es la misma estrategia multi-cloud que ya conocés."
- ▶ Avanzá al bloque 2.2.

---

# BLOQUE 2.2 — Vibe coding vs SDD ⏱ 0:18–0:38 (20 min)

## Slide 2.2.A — Vibe coding ⏱ 0:18–0:21
- Término de Karpathy, 2-feb-2025. Cita: "forget that the code even exists".
- Collins Word of the Year 2025 (6-nov-2025).
- 🎯 "Vibe coding = deploy a mano por SSH a producción."
- OK para prototipo del viernes, NO para CI.
- ▶ Avanzá a "por qué no escala".

## Slide 2.2.B — Por qué no escala ⏱ 0:21–0:22
- CodeRabbit (17-dic-2025, 470 PRs): código IA-coautoreado = 1.4× más issues críticos, 1.7× más mayores.
- Veracode (oct-2025): solo GPT-5 Mini mejoró seguridad (72%); el resto no.
- Veracode (jul-2025): 45% del código IA mete vulnerabilidades del OWASP Top 10.
- 🎯 "Falta reproducibilidad, revisión, versión, rollback. Es infra clickeada a mano."
- ▶ Avanzá a SDD.

## Slide 2.2.C — SDD ⏱ 0:22–0:25
- 🎯 "SDD es Infrastructure-as-Code para tu código." (repetila)
- spec.md = HCL · plan = `terraform plan` · implement = `terraform apply`.
- Lo que gobierna es la SPEC, no el código.
- Cita GitHub (2-sep-2025): "AI makes specifications executable".
- Énfasis: "la spec dejó de ser un Word que nadie lee — ahora es ejecutable".
- ▶ Avanzá a Spec Kit.

## Slide 2.2.D — Spec Kit ⏱ 0:25–0:26
- Toolkit open-source de GitHub (sep-2025). ⚠️ ~92k stars (revisá el día).
- Soporta 30+ agentes.
- Flujo: constitution → specify → clarify → plan → tasks → analyze → implement.
- "La semana que viene lo usamos en vivo. Hoy solo la intuición."
- ▶ Avanzá a la DEMO 1.

## Slide 2.2.E — DEMO 1 (vibe → spec) ⏱ 0:26–0:38
- **Demo embebida en el slide** (terminal animada). Si preferís, hacela en vivo en Claude Code.
- Paso 1: pedí vibe coding puro — endpoint Flask POST → valida → SQLite → ID.
- Paso 2: "Funciona, pero no leíste nada. No es reproducible."
- Paso 3: pedile al agente "ahora generame la spec de lo que hiciste".
- 🎯 "El mismo agente que vibe-codeó te da el artefacto que necesitabas al principio. Si la spec puede generarse al final, puede dirigir desde el principio → reproducible, revisable, versionable."
- Cierre: "esa spec.md la commiteo y la re-implemento en Go la semana que viene si quiero".
- ▶ BREAK.

---

## BREAK ⏱ 0:38–0:43 (5 min)
- Estírense, agua, preguntas sueltas.
- Volvé puntual.

---

# BLOQUE 2.3 — MCPs y Tools ⏱ 0:43–1:03 (20 min)

## Slide 2.3.A — El problema M×N ⏱ 0:43–0:47
- 3 modelos × 10 tools = 30 integraciones custom, cada una con auth/schema/errores.
- 🎯 "Mismo problema que resuelve un service mesh: en vez de N² conexiones, una abstracción común."
- ▶ Avanzá a MCP.

## Slide 2.3.B — MCP en una slide ⏱ 0:47–0:49
- Anthropic, 25-nov-2024. JSON-RPC 2.0 sobre stdio o Streamable HTTP.
- 🎯 "MCP es el USB-C de la IA." Inspirado en LSP de VS Code: write once, plug anywhere.
- >10.000 servers públicos (Linux Foundation, 9-dic-2025).
- ▶ Avanzá a estado.

## Slide 2.3.C — Estado al 2-jun-2026 ⏱ 0:49–0:51
- Spec estable: **2025-11-25**.
- RC: **2026-07-28** (locked 21-may, final 28-jul). ⚠️ NO es producción todavía.
- Governance: donado a la Agentic AI Foundation (Linux Foundation) el 9-dic-2025. Co-founders Anthropic/Block/OpenAI.
- Adopción: OpenAI lo adoptó 26-mar-2025 (Altman).
- 🎯 "Dejó de ser protocolo de un vendor. Es estándar de industria con governance formal. Es seguro apostar infra."
- ▶ Avanzá a primitivas.

## Slide 2.3.D — Las 3 primitivas ⏱ 0:51–0:54
- Tools = funciones invocables (el modelo decide cuándo).
- Resources = data leíble (URI).
- Prompts = templates / slash commands.
- Handshake: initialize → capabilities → tools/list → tools/call.
- 🎯 "Para los de gRPC: contract-first, capability discovery, request/response tipado."
- ▶ Avanzá a la DEMO 2.

## Slide 2.3.E — DEMO 2 (`claude mcp add`) ⏱ 0:54–1:02
- **Demo embebida** (terminal animada) o en vivo.
- Comando: `claude mcp add filesystem -s user -- npx -y @modelcontextprotocol/server-filesystem ~/Documents ~/Desktop`.
- Desglosá: `add` / nombre / `-s user` global / `--` separa / paths con acceso.
- Verificá: `claude mcp list` y dentro `/mcp`.
- Pedile: "listame los .md de ~/Documents y resumime el más nuevo". Mostrá que invoca las tools.
- 🎯 "El modelo NO conoce mi filesystem, lo descubre por protocolo. Si mañana cambio a S3, el modelo y mi prompt no cambian."
- Mostrá los remotos HTTP (Notion/Stripe/Sentry) con OAuth.
- ▶ Avanzá al cierre del bloque.

## Slide 2.3.F — Por qué cambia las reglas ⏱ 1:02–1:03
- Antes: cada equipo su adapter. Hoy: escribís el server una vez, anda en cualquier host.
- 🎯 "Mismo salto que de drivers JDBC custom a una capa estándar. El costo de integrar una tool nueva colapsa."
- ▶ Avanzá al bloque 2.4.

---

# BLOQUE 2.4 — Claude Skills ⏱ 1:03–1:20 (17 min)

## Slide 2.4.A — Qué son los Skills ⏱ 1:03–1:07
- Anthropic, 16-oct-2025. Willison: "maybe a bigger deal than MCP".
- Un Skill = una carpeta con un SKILL.md (YAML frontmatter: name + description; abajo Markdown).
- 🎯 "Progressive disclosure: al arrancar solo lee la descripción (~30-50 tokens); carga el body solo si matchea; los auxiliares solo si los necesita. Cero overhead hasta que se usa."
- ▶ Avanzá a Skills vs MCP.

## Slide 2.4.B — Skills vs MCP ⏱ 1:07–1:10
- 🎯 La distinción que tienen que memorizar:
  - MCP = conectividad (cómo técnico: hablar con Stripe/Postgres/GitHub).
  - Skills = procedimiento (cómo organizacional: cómo TU equipo hace X).
- Analogía: MCP = Terraform provider · Skill = módulo de Terraform / role de Ansible.
- Se combinan: un Skill puede invocar tools de un MCP.
- ▶ Avanzá a estructura.

## Slide 2.4.C — Estructura ⏱ 1:10–1:12
- Layout: SKILL.md (req) + references/ + scripts/ + assets/ + evals/.
- En Claude Code: `~/.claude/skills/<n>/` (personal) o `.claude/skills/<n>/` (proyecto).
- 🎯 "Hot reload: agregás/editás un skill y toma efecto sin reiniciar la sesión."
- ▶ Avanzá a la DEMO 3.

## Slide 2.4.D — DEMO 3 (crear un Skill) ⏱ 1:12–1:18
- **Demo embebida** o en vivo.
- `mkdir -p ~/.claude/skills/release-notes` + escribir SKILL.md (release notes formato DataCorp).
- Recargá, pedí: "generame las release notes desde el tag v2.3.0 hasta HEAD".
- Mostrá que carga el skill solo y sigue el procedimiento.
- 🎯 Tres cosas: (1) no usé prompt engineering, la inteligencia está versionada en disco; (2) es portable, lo commiteo y el equipo lo hereda; (3) es open standard (agentskills.io, 18-dic-2025).
- ▶ Avanzá al encaje MLOps.

## Slide 2.4.E — Skills es open standard ⏱ 1:18–1:20
- Spec en agentskills.io (18-dic-2025). Soporte: Claude.ai, Claude Code, Agent SDK, API.
- Portable a Codex CLI, Cursor, Gemini CLI.
- 🎯 "Pensalos como tus playbooks/roles de Ansible: capacidad procedimental versionada, code-reviewable, hot-reloadable. Es la pieza que faltaba para que el agente sea una capa más del stack."
- ▶ Avanzá al cierre.

---

# BLOQUE 2.5 — Cierre y puente ⏱ 1:20–1:30 (10 min)

## Slide 2.5.A — Las 4 piezas juntas ⏱ 1:20–1:24
- Recap rápido: Mapa de LLMs / SDD / MCP / Skills, una línea cada uno.
- Mapa: Claude lidera coding, GPT multimodal, Gemini value en GCP, chinos competitivos barato.
- SDD: la spec gobierna. MCP: conectividad estándar. Skills: procedimiento versionable.
- ▶ Avanzá a la idea fuerza.

## Slide 2.5.B — La idea fuerza ⏱ 1:24–1:28
- 🎯 "La diferencia no está en la herramienta, está en el proceso."
- Pregunta para que se lleven: "¿tu spec es la fuente de verdad, o lo es tu chat history con el agente?"
- "Vibe coding = viernes a la noche. SDD = producción."
- "Las 4 piezas = la versión 2026 de pasar de scripts bash a CI/CD declarativo."
- ▶ Avanzá al workshop.

## Slide 2.5.C — Workshop semana próxima ⏱ 1:28–1:30
- 100% hands-on. Tres cosas:
  - 1) Spec Kit flow completo en proyecto real.
  - 2) Construir un Skill aplicando SDD (doble bucle).
  - 3) Diseñar un flujo SDD custom para tu org.
- Traer: Claude Code 2.1+ actualizado, API key Anthropic, un repo chico real.
- 🎯 Cierre: "La diferencia no está en la herramienta. Lo probamos en vivo, la semana que viene."
- Gracias + preguntas.

---

## Checklist pre-clase (revisar el día) ⚠️
- [ ] Versiones/nombres de modelos en slide 2.1.B y benchmarks 2.1.C.
- [ ] Stars de Spec Kit (slide 2.2.D).
- [ ] Estado del RC de MCP 2026-07-28 (¿ya salió final?).
- [ ] `claude --version` en tu máquina (demo MCP/Skills).
- [ ] Probar las 3 demos una vez antes de entrar (aunque vayan embebidas en el HTML).
