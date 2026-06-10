# Clase 3 — Notas al orador (guion diapositiva por diapositiva)

> **Uso:** estas son tus *cue cards*. Una mirada rápida por slide mientras hablás. No es para leer palabra por palabra — son los puntos que no te podés olvidar, los datos con fecha, y las señales de cuándo avanzar.
> **Duración total:** 150 min (workshop hands-on). **Registro:** voseo, directo, analogías DevOps/MLOps.
> **Leyenda:** ⏱ = tiempo objetivo · ▶ = cuándo avanzar · 🖐️ = todos al teclado · 🎯 = la frase que tiene que quedar · ⚠️ = dato sensible a fecha (revisar el día).

---

## Slide 0 — Portada ⏱ 0:00–0:02
- Bienvenida corta. "Clase 3, y hoy lo construimos end-to-end."
- El valor está en el teclado de ellos, no en tus slides.
- Confirmá que todos tienen terminal y Claude Code a mano.
- ▶ Avanzá enseguida.

## Slide 1 — Recap clases 1 y 2 ⏱ 0:02–0:04
- 4 piezas: agent loop · vibe vs SDD · MCP (conectividad) · Skills (procedimiento).
- No re-expliques. Disparador: "¿se acuerdan del agent loop?"
- 🎯 "Hoy bajamos las 4 piezas a un proyecto real. La estrella es SDD conectando todo."

## Slide 2 — Agenda ⏱ 0:04–0:05
- Recorré los 6 bloques en 30 seg.
- 🎯 B2, B3 y B4 (105 min) son 100% manos al teclado.
- "Si a alguien le falla el entorno, lo arreglamos AHORA, no en el minuto 40."

## Slide 3 — Checklist de entorno 🖐️ ⏱ 0:05–0:10
- Que todos corran: `python3 --version` · `uv --version` · `claude doctor` · `specify check`.
- Detectá rojos rápido; pulgar arriba con los tres en verde.
- 🎯 Umbral: si >20% roto → B2 como "setup asistido" extendido y recortá 10 min de B3.

---

# BLOQUE 1 — Fundamentos de SDD ⏱ 0:10–0:35 (25 min)

## Slide 4 — Qué es SDD ⏱ 0:10–0:14
- Vibe coding: el código parece bien pero no anda. Se pierde la intención.
- SDD: la spec es la única fuente de verdad; el código se regenera.
- 🎯 "En SDD no parcheás el código: cambiás la spec y regenerás." Analogía IaC.

## Slide 5 — Qué es Spec Kit ⏱ 0:14–0:17
- Toolkit open-source de GitHub. CLI `specify`. Flujo con fases y checkpoints.
- "Vos manejás el volante, el agente escribe."
- ⚠️ Estable 0.8.18 (29-may-2026). Verificá `specify check` el día; pinneá `@v0.8.18` si querés.

## Slide 6 — Flujo /speckit.* ⏱ 0:17–0:22
- Comando por comando: constitution / specify / clarify(opc) / plan / tasks / analyze(opc) / implement.
- 🎯 clarify y analyze son los gates de calidad — lo que el vibe coding no tiene.
- ⚠️ Nombres con prefijo `/speckit.*`; init con `--integration claude` (no `--ai`).

## Slide 7 — Dónde viven los artefactos ⏱ 0:22–0:26
- constitution en `.specify/memory/`; comandos en `.claude/commands/`; por feature `specs/<N>-.../spec|plan|tasks.md`.
- 🎯 "¿Por qué el código hace X?" → la respuesta está en spec.md, no en un chat perdido. Todo se commitea.

## Slide 8 — Adaptar SDD ⏱ 0:26–0:35
- Constitución propia, gates propios, convenciones de stack. El flujo es un template.
- 🖐️ Ejercicio: que anoten 3 reglas de la constitución de SU proyecto. Guardalo para el B5.
- Sembrá: "más tarde encodeamos esto como Skills a medida del equipo."

---

# BLOQUE 2 — Setup hands-on ⏱ 0:35–1:00 (25 min)

## Slide 9 — Armá el repo 🖐️ ⏱ 0:35–0:45
- `mkdir taller-sdd && cd && git init` · `claude` (autenticar) · `/init` (genera CLAUDE.md).
- Si falta Claude Code: nativo `curl ... install.sh | bash`. npm legado (Node 18+). Nunca `sudo npm`.

## Slide 10 — Instalá Spec Kit 🖐️ ⏱ 0:45–0:55
- `specify init . --integration claude` · `ls .specify/ .claude/commands/`.
- En Claude Code, `/` y confirmar los `/speckit.*`.
- 🎯 ¿No aparecen? Reiniciá Claude Code (descubre comandos al arrancar) + confirmá carpeta. Usá `--integration claude`.

## Slide 11 — Checklist de setup ⏱ 0:55–1:00
- Confirmación a mano alzada de los 5 ítems.
- 🎯 Nadie entra al B3 con esto en rojo. Último checkpoint antes de la práctica grande.

---

# BLOQUE 3 — Flujo SDD completo ⏱ 1:00–1:45 (45 min)

## Slide 12 — El problema + estimación ⏱ 1:00–1:05
- Entregá `problema-inventario.md`. NO menciones a Claude todavía.
- 🎯 "Primero ESTIMÁ cuánto tardarías a mano. Anotá el número en minutos." Al final se compara.

## Slide 13 — El flujo en vivo ⏱ 1:05–1:08
- "Ahora se lo damos a Claude Code, pero vía SDD, no vibe coding."
- Ritmo: comando por comando, todos juntos. En cada checkpoint abrí el artefacto y leé.
- 🎯 "No es un botón mágico. Es un proceso con checkpoints donde vos leés y aprobás."

## Slide 14 — constitution + specify + clarify 🖐️ ⏱ 1:08–1:25
- `/speckit.constitution` (local, stdlib+Flask, sqlite3, sin auth, curl, documentado).
- `/speckit.specify` pegando el problema. Abrí spec.md y mostrá que es legible.
- `/speckit.clarify` → respondé en vivo; mostrá cómo se actualiza la spec.
- 🎯 El clarify es donde gobernás la intención: evita que el agente rellene supuestos.

## Slide 15 — plan + tasks + analyze + implement 🖐️ ⏱ 1:25–1:42
- `/speckit.plan` (Flask + sqlite3 stdlib) · `/speckit.tasks`.
- `/speckit.analyze` → gate de consistencia ANTES de escribir código.
- `/speckit.implement` → mientras corre, narrá. Después curl a los 4 endpoints.

## Slide 16 — Comparación ⏱ 1:42–1:45
- "¿Quién tardó menos que su estimación?" "¿Qué parte les sorprendió?"
- 🎯 "Lo que ganaste no es solo tiempo: es reproducible y revisable. La spec se commitea y se regenera."

---

# BLOQUE 4 — Skill con SDD + MCP ⏱ 1:45–2:20 (35 min)

## Slide 17 — Objetivo ⏱ 1:45–1:48
- Pedido → Skill → MCP → API Flask. La Skill no "habla" con la API: le dice al modelo CÓMO usar las tools.
- 🎯 "MCP te da la capacidad. Skill te da el criterio de cómo usarla."

## Slide 18 — Código del MCP ⏱ 1:48–1:52
- SDK oficial `mcp` (1.27.x, Python ≥3.10). Cada tool se describe con el docstring.
- 🎯 GOTCHA: en stdio NUNCA print() a stdout → corrompe el JSON-RPC. logging a stderr. Código en entregables.

## Slide 19 — Crear y registrar el MCP 🖐️ ⏱ 1:52–2:03
- `uv init mcp-items` · `uv venv && source` · `uv add "mcp[cli]" httpx` · pegar server.py.
- `claude mcp add items-api -- uv run server.py` · `claude mcp list` · `/mcp`.
- 🎯 La API Flask del B3 tiene que estar CORRIENDO. Servers stdio descubren tools al inicio de sesión: si agregaste a mitad, abrí sesión nueva.

## Slide 20 — La Skill vía SDD 🖐️ ⏱ 2:03–2:12
- `/speckit.specify` con la spec de la Skill (entregables) · plan · tasks · implement → `.claude/skills/items-ops/SKILL.md`.
- Carpeta nueva → reiniciar Claude Code (no alcanza `/reload-skills` para directorios nuevos).
- 🎯 El doble bucle: SDD para la app Y para las capacidades del agente.

## Slide 21 — El SKILL.md ⏱ 2:12–2:15
- `name` (≤64, minúsc/guiones) + `description` (≤1024, 3ª persona, qué+cuándo).
- Nombres calificados `servidor:tool` evitan "tool not found". Progressive disclosure, cuerpo <500 líneas.
- 🎯 El description es lo único que Claude lee al arrancar — si está mal, la Skill no se activa.

## Slide 22 — Prueba end-to-end 🖐️ ⏱ 2:15–2:20
- "Listame los modelos y agregá uno: bert-base, pytorch, 0.91." Se activa sola, valida, confirma el id.
- Verificá por afuera con `curl .../models/3`.
- 🎯 "No nombraste la Skill — se activó sola por su description." Skill+MCP+API juntos.

---

# BLOQUE 5 — Reflexión y cierre ⏱ 2:20–2:30 (10 min)

## Slide 23 — Skills + MCPs + imaginación ⏱ 2:20–2:23
- 🎯 MCP = capacidad, Skill = criterio. Con eso, casi cualquier integración.
- Cita: "MCP can provide tools and resources, while Skills package the playbook for using them well."

## Slide 24 — Ejemplos MLOps ⏱ 2:23–2:25
- run-training (receta reproducible) · data-drift-check (script bundleado) · model-card (template + métricas del MCP).
- Patrón: cualquier procedimiento repetible que el agente haga siempre igual.

## Slide 25 — Diseñá tu propio SDD ⏱ 2:25–2:28
- Reconectá con las 3 reglas del B1. Cada fase = una Skill: mlops-specify/plan/tasks/implement.
- 🎯 "Tu equipo deja de usar un SDD genérico y pasa a tener su propio SDD, versionado y compartible."

## Slide 26 — Idea fuerza ⏱ 2:28–2:30
- 🎯 "La spec gobierna. El código es output. El procedimiento es versionable." Dejala respirar.
- Recap de lo que hicieron con las manos: app + MCP + Skill, todo por spec.
- Llamado a la acción: una Skill para un procedimiento real, esta semana.

## Slide 27 — Preguntas ⏱ 2:30
- Gracias + preguntas. Recordá dónde quedan los entregables (`entregables/`).
- Próximo paso concreto: una Skill para su equipo esta semana.
