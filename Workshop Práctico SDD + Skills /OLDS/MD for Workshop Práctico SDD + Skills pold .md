# Workshop: Spec-Driven Development y Claude Skills para MLOps "vieja escuela"

**Duración**: 2 hs en vivo + 30 min de lectura previa. **Audiencia**: MLOps fuertes en infra y ML clásico, principiantes con agentes, usan Claude Code básico.

**Mantra del programa**: *"La diferencia no está en la herramienta, está en el proceso."*

> Aclaración técnica: todo lo de este documento está verificado contra documentación oficial primaria a mediados de 2026 (Spec Kit v0.8.18 — 29 de mayo de 2026, Flask 3.1.3 — 19 de febrero de 2026, paquete npm `@anthropic-ai/claude-code` v2.1.x, `mcp-server-sqlite-npx` v0.8.0 — 25 de octubre de 2025). Donde una herramienta cambió de comando, lo señalo explícitamente para que no uses sintaxis vieja.

---

## PARTE 1 — MATERIAL PREVIO (lectura ~30 min, autocontenido)

### 1. ¿Por qué SDD? El vibe coding no escala

Llamamos *vibe coding* al flujo en el que vos le pedís cosas al LLM en lenguaje natural, agarrás lo que devuelve, lo pegás, lo retocás, y seguís. Funciona genial para un script de 50 líneas. Empieza a explotar apenas tenés un equipo, una base de código que crece y compliance que cumplir.

Hay tres datos duros, fechados, que conviene tener en la cabeza:

- **METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity" (arXiv:2507.09089, 10 de julio de 2025)**: RCT con 16 devs open-source experimentados (promedio de 5 años en sus propios repos), 246 tareas reales. Los devs usaron principalmente **Cursor Pro con Claude 3.5/3.7 Sonnet** (las tools frontier de ese momento). Antes de empezar estimaron que la IA los aceleraría 24%; después estimaron 20% de aceleración. **La medición real mostró que les llevó 19% más de tiempo** terminar con IA habilitada (intervalo de confianza al 95%: +2% a +39%). La gente cree que va más rápido, los datos en codebases maduras dicen lo contrario.
- **Veracode 2025 GenAI Code Security Report (anunciado el 30 de julio de 2025, actualizado en octubre de 2025)**: más de 100 LLMs, 80+ tareas de codificación. **45% del código generado por IA contiene vulnerabilidades de seguridad** (incluyendo OWASP Top 10). **Java fue el peor, con exactamente 72% de tasa de fallo de seguridad**; Cross-Site Scripting falló el 86% de las veces y Log Injection el 88%. Python, C# y JavaScript: 38–45% de fallo. Conclusión central de Veracode: *los modelos más nuevos y grandes no producen código más seguro*. Es un problema estructural, no de escala.
- **DORA State of AI-assisted Software Development 2025 (Google Cloud, encuesta conducida del 13 de junio al 21 de julio de 2025 con casi 5.000 profesionales)**: 90% de los devs usa IA a diario, 65% se apoya "fuertemente" en ella, 80%+ reporta ganancias de productividad. Pero el resultado central, citando el reporte verbatim: *"AI's primary role in software development is that of an amplifier. It magnifies the strengths of high-performing organizations and the dysfunctions of struggling ones."* Equipos con plataforma interna sólida, workflows claros y feedback loops rápidos sacan provecho; equipos con sistemas tightly-coupled y procesos lentos no ven beneficio o ven inestabilidad downstream.

La conclusión operativa es la misma en los tres: **sin un proceso, la IA no te acelera, te genera deuda más rápido**. SDD es una forma concreta de poner ese proceso.

### 2. ¿Qué es Spec-Driven Development?

La analogía que vamos a usar todo el workshop: **SDD es Infrastructure-as-Code para tu código**. La spec gobierna, el código es output.

En vibe coding clásico el código es el artefacto principal y la spec es un mail/Slack/Notion que nadie relee. En SDD se invierte: la **spec** (un markdown estructurado, versionado en Git) es la fuente de verdad. El código se regenera/ajusta hasta cumplir la spec. Si la spec cambia, cambia el código; no al revés.

Esto te resuelve tres problemas concretos del día a día MLOps:
- **Trazabilidad**: por qué tal endpoint se comporta así → mirás el spec, no el código.
- **Onboarding**: un dev nuevo (o un agente nuevo) lee 4 archivos markdown y arranca.
- **Re-implementación**: querés migrar de Flask a FastAPI o de SQLite a Postgres → la spec sobrevive; sólo regenerás el plan y el código.

#### Versionado de specs

La spec vive en `specs/NNN-feature-name/` adentro del repo. Cada feature tiene su rama (`001-feature-name`, `002-...`) y Spec Kit detecta automáticamente la feature activa por la rama Git. Si cambia un requerimiento, vos editás `spec.md`, hacés un nuevo commit, y opcionalmente re-corrés `/speckit.plan` y `/speckit.tasks` para sincronizar plan y tasks con la nueva spec.

#### Specs sobre software existente (brownfield)

¿Y si la app ya existe? Hay dos caminos. **(a)** Le pedís a Claude Code que lea el código actual y te escriba la spec "como si la hubieras hecho antes": después corrés `/speckit.specify` con esa descripción y queda como baseline. **(b)** Para cambios incrementales, abrís una rama nueva (`003-new-endpoint`) y describís sólo el delta en `spec.md`; el plan y los tasks sólo tocan lo nuevo.

#### SDD a medida ("taylor made") por empresa

Spec Kit no es un dogma. Vos podés escribir tu propio `constitution.md` para tu empresa (estándares de testing, librerías permitidas, patrones de logging, exigencias de observabilidad), y tu propia plantilla de spec/plan/tasks. Y como vamos a ver al final, también podés encodear el flujo entero como Skills propias del equipo. El que adopta SDD lo termina adaptando al stack.

### 3. ¿Qué es Spec Kit?

[github.com/github/spec-kit](https://github.com/github/spec-kit), proyecto oficial de GitHub. Es el toolkit de referencia para SDD. Tiene dos piezas:

- **Specify CLI**: una herramienta Python (instalada vía `uv`/`uvx`) que inicializa el scaffolding SDD en tu proyecto.
- **Plantillas + comandos slash** para tu agente de IA. Después de `specify init`, tu agente (en nuestro caso, Claude Code) tiene disponibles los comandos slash `/speckit.*`.

**Ojo, esto cambió**: en versiones viejas de Spec Kit los comandos eran `/specify`, `/plan`, `/tasks` a secas. **Hoy (Spec Kit v0.8.18, lanzada el 29 de mayo de 2026) los comandos están namespaced como `/speckit.*`**. Si seguís un tutorial de 2024 que usa `/specify` a secas, no va a funcionar.

Flujo lean: `/speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement`

Flujo con quality gates (recomendado para producción): `/speckit.constitution → /speckit.specify → /speckit.clarify → /speckit.checklist → /speckit.plan → /speckit.tasks → /speckit.analyze → /speckit.implement`

### 4. Repaso mínimo de MCP y Skills

Esto ya lo vieron en clase 2, pero refresquemos. Son dos cosas distintas y complementarias:

- **MCP (Model Context Protocol)**: la "USB-C de los agentes". Un protocolo abierto que estandariza cómo un agente se conecta a herramientas externas (bases, APIs, sistemas de archivos, etc.). Resuelve el problema MxN (M agentes × N herramientas → M+N adaptadores en vez de M·N). En Claude Code se administra con `claude mcp add`. Hay tres transports: **stdio** (proceso local, lo más usado), **HTTP** (streamable HTTP, el estándar actual para servidores remotos), y **SSE** (legacy, deprecado a favor de HTTP).
- **Claude Skills**: una **carpeta** con un archivo `SKILL.md`. El `SKILL.md` tiene un YAML frontmatter (campos `name` y `description`) y abajo el cuerpo en markdown con instrucciones procedimentales. Anthropic las define oficialmente como *"folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks"*. La gracia es **progressive disclosure**: al arrancar, sólo se cargan el nombre y la descripción de cada Skill (~30 tokens cada una); el contenido completo del `SKILL.md` se lee sólo cuando Claude decide que esa Skill es relevante.

**Regla de oro**: **MCP = conectividad** (cómo Claude habla con sistemas externos). **Skills = procedimiento** (cómo Claude hace una tarea repetible bien). Se usan juntas: una Skill puede orquestar llamadas a un MCP.

#### Ubicación de Skills para Claude Code

- **Personal** (sirve en todos tus proyectos): `~/.claude/skills/<skill-name>/SKILL.md`
- **Proyecto** (vive en el repo, se commitea al equipo): `.claude/skills/<skill-name>/SKILL.md`

Si dos Skills tienen el mismo nombre, la regla de precedencia es: enterprise > personal > project. Para listar las Skills disponibles en una sesión, escribís `/skills`.

#### Frontmatter mínimo viable de un SKILL.md (Anthropic spec)

```markdown
---
name: my-skill-name
description: Qué hace la skill + cuándo usarla, en tercera persona. Hasta 1024 chars.
---

# My Skill

## Instructions
Pasos concretos y enumerados acá.
```

Campos opcionales útiles: `allowed-tools` (restringe qué herramientas puede usar la skill), `disable-model-invocation: true` (sólo el user puede invocarla, no Claude solo), `context: fork` (corre en sub-agente aislado para no contaminar el contexto principal). Validación: `name` máx 64 chars (sólo minúsculas, números, guiones), `description` máx 1024 chars, cuerpo recomendado bajo 500 líneas.

### 5. Instalación y verificación COMPLETA del entorno

Hacé esto **antes del workshop**. Si algo falla, abrí ticket en el canal — vamos a tener 15 min de buffer al inicio pero no más.

#### 5.1 Python 3.11+ y Git 2.30+

```bash
python3 --version    # esperás 3.11 o superior
git --version        # esperás 2.30 o superior
```

#### 5.2 `uv` y `uvx` (Astral)

Instalador oficial (mediados de 2026, serie 0.11.x):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verificación:
```bash
uv --version
uvx --version
```

Si después de instalar `uv` no aparece, abrí una terminal nueva (el script modifica tu shell profile).

#### 5.3 Node.js 18+ (necesario para Claude Code vía npm y para el MCP de SQLite)

```bash
node --version    # mínimo v18.0.0, recomendado v20 LTS o v22 LTS
npm --version
```

Si no tenés Node, instalalo con `nvm`:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nvm install 22
nvm use 22
```

#### 5.4 Claude Code

Dos métodos oficiales:

**Opción A — Native installer** (recomendado por Anthropic desde octubre de 2025; no necesita Node):
```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

**Opción B — npm global** (si ya tenés Node configurado):
```bash
npm install -g @anthropic-ai/claude-code
```

⚠️ **No uses `sudo npm install`**. Si te tira EACCES, configurá `npm config set prefix ~/.npm-global` y agregalo al PATH.

Verificación:
```bash
claude --version
claude doctor    # diagnóstico de entorno
```

Primer login: corré `claude` en cualquier carpeta y va a abrir el navegador para OAuth con tu cuenta Anthropic (necesitás un plan Pro, Max, Team o Enterprise; o una API key seteada como `ANTHROPIC_API_KEY`).

#### 5.5 Spec Kit (Specify CLI)

Hoy (junio 2026) la versión vigente es **v0.8.18** (lanzada el 29 de mayo de 2026).

Dos formas:

**Persistente** (lo que recomendamos para el workshop):
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify --version
```

**One-time vía uvx** (más liviano, no instala nada permanente):
```bash
uvx --from git+https://github.com/github/spec-kit.git specify --help
```

Diagnóstico:
```bash
specify check    # verifica el entorno de Spec Kit
```

#### 5.6 Checklist de "entorno listo"

Marcá los seis:

- [ ] `python3 --version` → 3.11+
- [ ] `git --version` → 2.30+
- [ ] `uv --version` y `uvx --version` responden sin error
- [ ] `node --version` → 18+
- [ ] `claude --version` responde y `claude doctor` no marca rojos
- [ ] `specify --version` responde con v0.8.x

### 6. Repaso mínimo de Flask + SQLite

Flask **3.1.3** (PyPI, 19 de febrero de 2026). Patrón mínimo de GET y POST contra `sqlite3` (sólo para que no te frenes en el workshop):

```python
# app.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "items.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/items", methods=["GET"])
def list_items():
    conn = get_db()
    rows = conn.execute("SELECT id, name, qty FROM items").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/items", methods=["POST"])
def create_item():
    payload = request.get_json()
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO items (name, qty) VALUES (?, ?)",
        (payload["name"], payload["qty"]),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

Inicialización de la base:
```python
# init_db.py
import sqlite3
conn = sqlite3.connect("items.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        qty INTEGER NOT NULL DEFAULT 0
    )
""")
conn.commit()
conn.close()
```

Ojo: este código es **referencia** de lo que vamos a generar con SDD, no lo que vas a tipear. En el workshop el LLM lo genera a partir de la spec.

---

## PARTE 2 — GUION DEL FACILITADOR (minuto a minuto, ~120 min)

### Bloque 0 — Bienvenida y check de entorno (0:00 – 0:10, 10 min)

**Facilitador DICE**:
> "Hola, bienvenidos. Antes que nada, los que no completaron el setup previo: abran el canal #setup y peguen el output de `claude --version && specify --version && uv --version && node --version`. Si algo no anda, agarro a alguien del equipo para que les dé una mano en paralelo mientras arrancamos. Recuerden el mantra de toda la cursada: **la diferencia no está en la herramienta, está en el proceso**. Hoy no venimos a aprender un comando, venimos a aprender un flujo."

**Facilitador HACE**: comparte pantalla, muestra terminal limpia con `claude --version` y `specify --version` corriendo OK.

**Participantes TIPEAN**:
```bash
claude --version
specify --version
uv --version
node --version
```

### Bloque 1 — Fundamentos de SDD (0:10 – 0:30, 20 min)

**0:10 – 0:14 — La analogía IaC**

DICE:
> "Ustedes son MLOps. Saben perfectamente qué pasó cuando Terraform y Pulumi le ganaron al click-ops en AWS. Antes: alguien clickeaba en la consola, levantaba el EC2, y eso era la verdad. ¿Documentación? Mail. ¿Reproducir el entorno? Imposible. Después de IaC: el `main.tf` *es* la verdad. La consola es la consecuencia. SDD es exactamente eso, pero para tu código. La spec es el `main.tf`. El código Python es el EC2 corriendo. Si quieren cambiar el código, cambian la spec, no el código."

**0:14 – 0:20 — Por qué la spec pasa a ser ley**

DICE:
> "Tres datos para que esto no sea opinión mía. Uno: el RCT de METR de julio 2025, 16 devs open-source experimentados, 246 tareas con Cursor Pro + Claude 3.5/3.7 Sonnet. La IA los hizo **19% más lentos**, mientras ellos sentían que iban 20% más rápido. Dos: Veracode escaneó código de más de 100 LLMs en agosto 2025; **45% tenía vulnerabilidades de seguridad**, Java con 72% exacto de fallo. Tres: el DORA report 2025, con casi 5.000 profesionales encuestados entre el 13 de junio y el 21 de julio, dice que la IA es un **amplificador**: equipos con buen sistema, mejoran; equipos sin sistema, empeoran. SDD es el sistema."

**0:20 – 0:26 — Versionado, brownfield, SDD taylor-made**

DICE:
> "La spec vive en `specs/NNN-feature-name/spec.md`, una carpeta por feature, una rama Git por feature. Spec Kit detecta la feature por la rama, así que cambiás de feature cambiando de rama, nada raro. ¿Y si la app ya existe? Le pedís a Claude que te lea el código y te escriba la spec retroactiva. ¿Y si querés tu propio sabor de SDD? El `constitution.md` es el lugar — ahí escribís las reglas no negociables de **tu** empresa: stack permitido, testing obligatorio, observabilidad, lo que sea. Esa constitution la lee Claude en cada `/speckit.plan` y `/speckit.implement`."

**0:26 – 0:30 — MCP vs Skills, otra vez**

DICE:
> "Refresco rápido. **MCP = conectividad**. Es el USB-C: Claude habla con SQLite, con Postgres, con la API de tu CRM, con el filesystem, todo por el mismo protocolo. **Skills = procedimiento**. Es la receta: 'cómo se hace un deploy en esta empresa', 'cómo se valida un modelo antes de subirlo a prod'. Hoy vamos a usar ambas. La app habla con Claude vía un MCP de SQLite, y arriba ponemos una Skill que orquesta — la opción más production-like."

### Bloque 2 — Setup técnico hands-on (0:30 – 0:45, 15 min)

**0:30 – 0:35 — Crear el proyecto**

DICE:
> "Vamos. Carpeta vacía, terminal adentro. Vamos a inicializar el proyecto con Spec Kit integrado con Claude Code."

Participantes TIPEAN:
```bash
mkdir mlops-sdd-workshop && cd mlops-sdd-workshop
uvx --from git+https://github.com/github/spec-kit.git specify init . --integration claude
```

DICE durante el output:
> "Mírense las carpetas que crea: `.specify/` con templates y scripts, `.claude/commands/` con los archivos `speckit.*.md` — esos son los slash commands que Claude Code va a tener disponibles. `.specify/memory/constitution.md` es donde van las reglas no negociables."

**0:35 – 0:40 — Abrir Claude Code**

Participantes TIPEAN:
```bash
git init
git add -A && git commit -m "initial spec-kit scaffold"
claude
```

DICE:
> "Una vez adentro de Claude Code, tipeen `/skills` y miren qué tienen. Y `/help` para ver los comandos. Si ven los `/speckit.*`, estamos OK."

**0:40 – 0:45 — Establecer la constitution**

Participantes TIPEAN dentro de Claude Code:
```
/speckit.constitution
El proyecto es una API HTTP simple para gestionar items en una base local.
Stack obligatorio: Python 3.11+, Flask 3.x, sqlite3 de stdlib (sin ORMs).
Principios: (1) Simplicidad antes que cleverness. (2) Toda persistencia es local SQLite, sin servicios externos. (3) Errores devueltos como JSON con códigos HTTP correctos. (4) Cero dependencias más allá de Flask y pytest. (5) Cada endpoint debe tener al menos un test con pytest. (6) Nunca construir SQL por concatenación; siempre placeholders parametrizados.
```

DICE:
> "Esto es importante: Claude va a leer esto **antes de cada plan y cada implement**. Si su empresa tiene un standard de logging, va acá. Si exigen mypy strict, va acá."

### Bloque 3 — Práctica guiada: flujo SDD completo (0:45 – 1:25, 40 min)

**0:45 – 0:55 — /speckit.specify**

DICE:
> "Ahora la spec. Atentos al detalle: la spec describe **qué y por qué**, no cómo. Nada de Flask, nada de SQLite en este paso. Eso va en /plan."

Participantes TIPEAN:
```
/speckit.specify
Construir una API HTTP local que permita gestionar una lista de "items" (ej. inventario simple).
Funcionalidades:
- GET /items: devuelve todos los items existentes como un array JSON. Cada item tiene id, name, qty.
- POST /items: recibe un JSON con {name, qty} y crea un nuevo item. Responde 201 con el id generado.
Criterios de aceptación:
- Si POST recibe payload inválido (falta name o qty no es entero), responde 400 con un JSON de error.
- Si GET no encuentra items, responde 200 con un array vacío.
- Los datos persisten entre reinicios del servidor.
- Debe haber al menos un test automatizado para cada endpoint.
```

DICE durante la corrida:
> "Claude está creando una rama `001-...`, una carpeta `specs/001-.../`, y un `spec.md` estructurado con secciones de scope, user scenarios, requerimientos funcionales, success criteria. Lean ese archivo cuando termine. Esa es su nueva fuente de verdad."

**0:55 – 1:02 — /speckit.clarify (quality gate)**

DICE:
> "El paso opcional pero re útil: dejamos que Claude nos haga preguntas para limpiar ambigüedades. En proyectos reales, este paso te ahorra el 80% de los bugs de 'no era eso lo que quería'."

Participantes TIPEAN:
```
/speckit.clarify
```

DICE:
> "Va a hacer hasta 5 preguntas. Respondan con criterio MLOps: piensen en logs, en errores, en concurrencia mínima. Cada respuesta queda guardada en una sección Clarifications del spec.md, con fecha. Eso después te permite hacer auditoría de por qué tal decisión está como está."

**1:02 – 1:12 — /speckit.plan**

DICE:
> "Ahora sí, el **cómo**. Le decimos a Claude el stack y la arquitectura."

Participantes TIPEAN:
```
/speckit.plan
Usar Flask 3.x con un único archivo app.py.
Persistencia con el módulo sqlite3 de la stdlib, base local en items.db.
Inicialización de schema en un script init_db.py separado.
Tests con pytest, usando el test client de Flask.
Estructura:
- app.py (Flask app + rutas + lógica de DB inline para mantener simple)
- init_db.py (crea la tabla items si no existe)
- tests/test_api.py (tests de GET y POST)
- requirements.txt (sólo flask y pytest)
```

DICE:
> "Esto genera `plan.md`, `data-model.md` y `contracts/` con los esquemas de los endpoints. Tómense un minuto, léanlos."

**1:12 – 1:17 — /speckit.tasks**

Participantes TIPEAN:
```
/speckit.tasks
```

DICE:
> "Esto te genera `tasks.md` con tareas T001, T002, T003... en orden de dependencias. Si miran adentro, cada tarea tiene su criterio de done. Es un Jira board automático sacado de la spec."

**1:17 – 1:25 — /speckit.implement**

Participantes TIPEAN:
```
/speckit.implement
```

DICE durante la corrida (~5–8 min):
> "Claude va tarea por tarea: crea el archivo, escribe el código, corre los tests si están especificados. Mientras corre, abran otro terminal y miren cómo se llenan los archivos. Cuando termine, vamos a correr el server y probarlo."

Al terminar, participantes TIPEAN:
```bash
python init_db.py
python app.py &
curl http://127.0.0.1:5000/items
curl -X POST http://127.0.0.1:5000/items -H "Content-Type: application/json" -d '{"name":"widget","qty":5}'
curl http://127.0.0.1:5000/items
pytest -v
```

DICE:
> "Lo importante no es que esto ande — anda. Lo importante es que esto **es repetible**. Mañana, otro dev mira el spec.md y entiende. La semana que viene, querés un endpoint nuevo: rama nueva, spec.md nuevo, mismo flujo. Eso es SDD."

### Bloque 4 — Skill + MCP de SQLite con SDD (1:25 – 1:55, 30 min)

**1:25 – 1:30 — Plantear la opción C**

DICE:
> "Hasta acá tenemos una app que corre. Ahora queremos que Claude pueda **leer y escribir directo en la base local**, sin que nosotros corramos curl. Hay tres opciones: (A) que Claude escriba código y lo ejecute, (B) usar una herramienta directa de Claude para subprocess, (C) que haya un servidor MCP de SQLite de por medio, con una Skill que orqueste arriba. Vamos por la C. ¿Por qué? Porque es la opción production-like: el MCP encapsula el acceso a datos, podemos auditarlo, podemos cambiar la base mañana y la Skill no se entera."

**1:30 – 1:38 — Instalar el MCP de SQLite**

DICE:
> "Atención que esto cambió, y es importante saber por qué. El servidor oficial de Anthropic `mcp-server-sqlite` (Python) fue archivado el **29 de mayo de 2025** en `modelcontextprotocol/servers-archived`. Para ese entonces ya había sido forkeado más de 5.000 veces. Después, el investigador Sean Park de Trend Micro le reportó privadamente a Anthropic, el 11 de junio de 2025, una vulnerabilidad de SQL injection en ese mismo servidor. Anthropic decidió no parchearla, citando el estado 'out of scope' por estar el repo archivado (issue público #1348). The Register lo publicó el 25 de junio de 2025. Lo que se usa hoy es la implementación de la comunidad **`mcp-server-sqlite-npx`** (Node, license ISC, mantenida por johnnyoshika en GitHub, v0.8.0 del 25 de octubre de 2025), que es el port npm de la misma interfaz original con la misma superficie de 6 tools."

Participantes TIPEAN (macOS/Linux, **desde la raíz del proyecto**):
```bash
claude mcp add --transport stdio --scope project sqlite \
  -- npx -y mcp-server-sqlite-npx "$(pwd)/items.db"
```

Windows (cmd / PowerShell native, **no WSL**):
```cmd
claude mcp add --transport stdio --scope project sqlite -- cmd /c npx -y mcp-server-sqlite-npx "%CD%\items.db"
```

Verificación:
```bash
claude mcp list
```

DICE:
> "Tienen que ver `sqlite  ✓ Connected`. Si no, lo más probable es path relativo — siempre absoluto. En Windows, si dice 'Connection closed', es porque les falta el `cmd /c`. Adentro de Claude Code, tipeen `/mcp` y van a ver el panel con los tools expuestos: `read_query`, `write_query`, `list_tables`, `describe_table`, `create_table`, `append_insight`."

**1:38 – 1:48 — Crear la Skill con SDD (sí, con SDD)**

DICE:
> "Acá empieza lo bueno. Vamos a crear una Skill usando el mismo flujo SDD. Esta Skill se va a llamar `inventory-ops` y va a orquestar el MCP para operaciones típicas de inventario: chequear stock, agregar items, consolidar. **Lo importante: el procedimiento (la Skill) se apoya en la conectividad (el MCP)**."

Participantes TIPEAN una nueva spec:
```
/speckit.specify
Crear una Claude Skill llamada "inventory-ops" para operaciones de inventario.
Ubicación: .claude/skills/inventory-ops/SKILL.md (project-scoped, commiteable).
Funcionalidades de la Skill:
- "chequear stock bajo": llama a list_tables y read_query del MCP sqlite para devolver todos los items con qty <= 5.
- "agregar item": valida nombre y qty, llama a write_query del MCP sqlite con un INSERT parametrizado.
- "consolidar duplicados": si hay dos items con el mismo name, suma sus qty en uno solo y borra el otro.
Restricciones:
- La Skill NUNCA debe construir SQL por concatenación de strings. Siempre parametrizado.
- La Skill debe pedir confirmación al usuario antes de cualquier operación que modifique datos (consolidar y borrar).
- Frontmatter YAML válido: name=inventory-ops, description en tercera persona con triggers explícitos.
```

```
/speckit.plan
La Skill es un único archivo SKILL.md. Sin scripts auxiliares. El cuerpo en markdown, bajo 200 líneas, con secciones: ## When to use, ## Tools used, ## Procedures (chequear stock, agregar item, consolidar duplicados), ## Safety rules.
```

```
/speckit.tasks
```

```
/speckit.implement
```

DICE durante la corrida:
> "Claude va a crear `.claude/skills/inventory-ops/SKILL.md`. Mientras corre, una pregunta: ¿se dan cuenta de lo que acabamos de hacer? Usamos SDD para construir una Skill que vive junto al proyecto, en el repo, versionada. La Skill es código tanto como el código mismo."

**1:48 – 1:55 — Probar la Skill que llama al MCP**

Participantes TIPEAN dentro de Claude Code, en una sesión nueva (`claude` desde la raíz):
```
Decime qué items hay con stock bajo en la base
```

DICE:
> "Claude debería matchear la descripción de la Skill `inventory-ops`, cargar su SKILL.md, llamar al tool `mcp__sqlite__read_query` con un SELECT parametrizado, y devolverte la lista. Pídanle ahora que agregue un item, y miren cómo pide confirmación antes de ejecutar el write."

```
Agregame "tornillo" con qty 3
```

DICE:
> "Esto es la opción C en vivo: MCP abajo (conectividad), Skill arriba (procedimiento), spec y constitution gobernando todo. Si mañana cambian SQLite por Postgres, cambian el MCP — la Skill no cambia. Si mañana cambia el procedimiento (ej: el threshold de stock bajo pasa a 10), cambian la Skill — el MCP no cambia. Separation of concerns."

### Bloque 5 — Reflexión y extensión (1:55 – 2:10, 15 min)

**1:55 – 2:02 — Qué se puede hacer con Skills**

DICE:
> "Piensen 30 segundos en su día a día como MLOps. ¿Qué procedimiento repiten todas las semanas? Yo les tiro tres que son canónicos:
> 1. **model-validation**: chequear que un modelo nuevo cumpla métricas mínimas y un schema antes de mergear a `models/main`.
> 2. **datadrift-report**: armar el reporte semanal de drift de feature distributions desde un store local.
> 3. **deploy-checklist**: el preflight de deploy a prod (chequear coverage, lint, changelog, SLO de latencia)."

> "Y del lado open-source: el repo oficial `anthropics/skills` en GitHub tiene Skills listas para PDF, Excel, Word, brand-guidelines, `mcp-server` (sí, una Skill que te ayuda a hacer servidores MCP), `webapp-testing` con Playwright. Te las podés bajar a `~/.claude/skills/` con `git clone` o vía `/plugin install document-skills@anthropic-agent-skills`."

**2:02 – 2:07 — SDD a medida para tu empresa, basado en Skills**

DICE:
> "Acá conecto todo. Spec Kit es un sabor de SDD: el de GitHub. Está bueno, pero no es la verdad revelada. Vos podés escribir **tu propio sabor de SDD** y entregarlo como un set de Skills."

> "Imagínense esto: una Skill `our-specify`, una `our-plan`, una `our-tasks`, una `our-implement`, todas en `.claude/skills/` del repo de tu empresa, con el formato que tu equipo necesita: secciones extra para SLA, para data lineage, para compliance. Las usan con `/our-specify`, `/our-plan`, etc. Cuando entra un dev nuevo, clona el repo, abre Claude Code, y tiene **el SDD de tu empresa** en vez del SDD genérico. Esa es la potencia: encodear tu proceso, no adoptar el proceso de otro."

**2:07 – 2:10 — Cierre**

DICE:
> "Cerramos como empezamos: la diferencia no está en la herramienta, está en el proceso. Hoy se llevan tres cosas: (1) un flujo SDD que pueden usar mañana, (2) la idea de que MCP y Skills son piezas distintas y complementarias, y (3) el insight de que el flujo mismo es codificable como Skills. En el canal del workshop dejé el apéndice técnico con todo escrito, los comandos copy-paste, troubleshooting y los tres ejemplos de Skills MLOps que mencioné. Preguntas."

---

## PARTE 3 — ESQUEMA DE SLIDES

**Bloque 0 — Bienvenida (2 slides)**
1. Título + facilitador + agenda + mantra "La diferencia no está en la herramienta, está en el proceso".
2. Checklist de entorno con los 6 checks. Comandos visibles.

**Bloque 1 — Fundamentos SDD (8 slides)**
3. ¿Qué es vibe coding y por qué no escala?
4. Los tres datos: METR 19% slowdown (RCT con Cursor Pro + Claude 3.5/3.7 Sonnet, jul 2025), Veracode 45% vulnerable (Java 72%, ago 2025), DORA "AI is amplifier" (5.000 profesionales, 13-jun a 21-jul 2025).
5. Analogía: SDD = IaC para tu código (diagrama main.tf ↔ EC2 / spec.md ↔ código).
6. La spec como fuente de verdad: diagrama del flujo Git de specs.
7. Versionado: una rama por feature, `specs/NNN-feature/`.
8. Brownfield: dos caminos (spec retroactiva vs delta-feature).
9. SDD taylor-made: el `constitution.md` y la idea de Skills `/our-*`.
10. MCP vs Skills, tabla comparativa. "USB-C" vs "receta".

**Bloque 2 — Setup técnico (4 slides)**
11. `uvx --from git+... specify init . --integration claude` — qué genera.
12. Estructura de carpetas: `.specify/`, `.claude/commands/`, `specs/`.
13. Abrir Claude Code y verificar `/skills` y `/help`.
14. `/speckit.constitution` — qué escribir, ejemplo del workshop.

**Bloque 3 — Flujo SDD completo (8 slides)**
15. El pipeline de comandos: `constitution → specify → clarify → checklist → plan → tasks → analyze → implement` (con la versión "lean" resaltada).
16. Diferencia entre `/speckit.specify` (qué+por qué) y `/speckit.plan` (cómo).
17. `/speckit.specify` — el prompt exacto a tipear (el spec del workshop).
18. `/speckit.clarify` — para qué sirve, cuándo skipearlo.
19. `/speckit.plan` — el prompt exacto a tipear.
20. `/speckit.tasks` — qué te devuelve (T001, T002, ... con dependencias).
21. `/speckit.implement` — qué hace bajo el capó.
22. Pruebas con curl y pytest.

**Bloque 4 — MCP de SQLite + Skill (6 slides)**
23. Las 3 opciones (A, B, C) — por qué la C es la production-like.
24. ¡Aviso! El MCP oficial fue archivado el 29-may-2025; SQLi reportada por Sean Park (Trend Micro) el 11-jun-2025, no parcheada. Usar `mcp-server-sqlite-npx` (ISC) de la comunidad.
25. El comando exacto `claude mcp add --transport stdio --scope project sqlite -- npx -y mcp-server-sqlite-npx ...` (macOS/Linux/Windows).
26. Verificación: `claude mcp list`, `/mcp` panel, tools expuestos.
27. La Skill `inventory-ops` — qué hace, dónde vive, cómo se llama.
28. Demo en vivo: Claude usa la Skill que usa el MCP que toca la base.

**Bloque 5 — Reflexión + extensión (4 slides)**
29. Tres Skills útiles para MLOps en el día a día (model-validation, datadrift-report, deploy-checklist).
30. El repo oficial `anthropics/skills` y cómo bajar Skills de productividad/diseño.
31. "Diseñá tu propio SDD basado en Skills": diagrama de `/our-specify`, `/our-plan`, `/our-tasks`, `/our-implement` en `.claude/skills/`.
32. Cierre: mantra, links al apéndice, espacio para preguntas.

---

## PARTE 4 — APÉNDICE TÉCNICO

### A1. Repo inicial — comandos exactos

```bash
# Crear y entrar
mkdir mlops-sdd-workshop && cd mlops-sdd-workshop

# Inicializar Spec Kit con integración Claude (versión vigente: v0.8.18, 29-may-2026)
uvx --from git+https://github.com/github/spec-kit.git specify init . --integration claude

# Git baseline
git init
git add -A
git commit -m "chore: spec-kit scaffold"
```

Resultado esperado:
```
.specify/
  memory/constitution.md
  scripts/bash/   (o powershell/ en Windows)
  templates/
.claude/
  commands/
    speckit.constitution.md
    speckit.specify.md
    speckit.clarify.md
    speckit.checklist.md
    speckit.plan.md
    speckit.tasks.md
    speckit.analyze.md
    speckit.implement.md
```

### A2. La spec EXACTA del proyecto Flask

Dentro de Claude Code:

```
/speckit.constitution
El proyecto es una API HTTP simple para gestionar items en una base local.
Stack obligatorio: Python 3.11+, Flask 3.x, sqlite3 de stdlib (sin ORMs).
Principios no negociables:
1. Simplicidad antes que cleverness. Si dudás entre dos diseños, el más simple gana.
2. Toda persistencia es local SQLite. Cero servicios externos.
3. Errores devueltos como JSON con código HTTP correcto (400, 404, 500).
4. Cero dependencias más allá de Flask y pytest.
5. Cada endpoint debe tener al menos un test con pytest usando el test client de Flask.
6. Nunca construir SQL por concatenación de strings; siempre placeholders parametrizados.
```

```
/speckit.specify
Construir una API HTTP local que permita gestionar una lista de items (inventario simple).

Funcionalidades:
- GET /items: devuelve todos los items como un array JSON. Cada item tiene id (int), name (string), qty (int).
- POST /items: recibe un JSON {"name": string, "qty": int} y crea un nuevo item. Responde 201 con {"id": <int>}.

Criterios de aceptación:
- Si POST recibe payload inválido (falta name, name vacío, o qty no es int >= 0), responde 400 con {"error": "<motivo>"}.
- Si GET no encuentra items, responde 200 con [].
- Los datos persisten entre reinicios del servidor.
- Debe haber al menos un test por endpoint cubriendo el happy path y un error case.
- El servidor escucha en 127.0.0.1:5000.
```

```
/speckit.clarify
```
(Responder las preguntas según el criterio MLOps del facilitador. Las respuestas quedan guardadas en `spec.md`.)

```
/speckit.plan
Stack: Flask 3.1+, módulo sqlite3 de stdlib, pytest para tests.
Archivos:
- app.py: Flask app, dos rutas, helpers de DB inline (mantener simple para el workshop).
- init_db.py: script idempotente que crea la tabla items si no existe.
- tests/test_api.py: tests con el test client de Flask.
- requirements.txt: flask>=3.1, pytest>=8.
- README.md: instrucciones de cómo correr y testear.
Schema:
- Tabla items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, qty INTEGER NOT NULL DEFAULT 0)
```

```
/speckit.tasks
```

```
/speckit.implement
```

### A3. Verificación de la app

```bash
python init_db.py
python app.py &
sleep 1

# GET vacío
curl -s http://127.0.0.1:5000/items
# → []

# POST válido
curl -s -X POST http://127.0.0.1:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"widget","qty":5}'
# → {"id":1}

# GET con datos
curl -s http://127.0.0.1:5000/items
# → [{"id":1,"name":"widget","qty":5}]

# POST inválido
curl -s -X POST http://127.0.0.1:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"","qty":-1}'
# → {"error":"..."}, código 400

# Tests
pytest -v

# Cierre del server
kill %1
```

### A4. Configuración exacta del MCP de SQLite

**Por qué este servidor, no otro**: el de referencia oficial de Anthropic (`mcp-server-sqlite`, Python) fue archivado el **29 de mayo de 2025** en `modelcontextprotocol/servers-archived` (con más de 5.000 forks vivos para esa fecha). El investigador **Sean Park de Trend Micro** reportó una vulnerabilidad de SQL injection sobre ese servidor el **11 de junio de 2025**; Anthropic la marcó como "out of scope" en el issue público #1348 por estar el repo archivado, y The Register la publicó el **25 de junio de 2025**. El reemplazo más usado por la comunidad es **`mcp-server-sqlite-npx`** (Node, license **ISC**, mantenido por johnnyoshika en GitHub, v0.8.0 del **25 de octubre de 2025**), que es port directo del original y expone las mismas 6 tools: `read_query`, `write_query`, `create_table`, `list_tables`, `describe_table`, `append_insight`.

**Comando exacto (macOS / Linux)**:
```bash
claude mcp add --transport stdio --scope project sqlite \
  -- npx -y mcp-server-sqlite-npx "$(pwd)/items.db"
```

**Windows (cmd / PowerShell native, NO WSL)**:
```cmd
claude mcp add --transport stdio --scope project sqlite -- cmd /c npx -y mcp-server-sqlite-npx "%CD%\items.db"
```

**JSON resultante en `.mcp.json` (raíz del proyecto)**:
```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-server-sqlite-npx",
        "/absolute/path/to/items.db"
      ],
      "env": {}
    }
  }
}
```

**Verificación**:
```bash
claude mcp list
# debe mostrar: sqlite    ✓ Connected

claude mcp get sqlite
# muestra el bloque de config
```

Dentro de Claude Code:
```
/mcp
```
muestra el panel con estado live, tools disponibles y permite gestionar.

**Notas operativas**:
- Transport: stdio (default). HTTP/SSE no aplican para SQLite local.
- Scope project graba en `.mcp.json` y se commitea al repo — todos los del equipo lo levantan al clonar (Claude Code pide aprobación la primera vez por seguridad).
- Las tools del MCP quedan disponibles como `mcp__sqlite__read_query`, `mcp__sqlite__write_query`, etc. en el namespace de Claude.
- Los flags `--transport`, `--scope`, `--env`, `--header` **van siempre antes del nombre del servidor**. El `--` separa los flags del comando stdio.

### A5. Ejercicio COMPLETO: construir la Skill `inventory-ops` con SDD

**Spec de la Skill** (lo que tipeás dentro de Claude Code):

```
/speckit.specify
Construir una Claude Skill llamada "inventory-ops" para operaciones de inventario sobre la base SQLite local.

Ubicación final: .claude/skills/inventory-ops/SKILL.md (project-scoped, commiteable al repo).

Procedimientos que la Skill debe encodear:
1. "chequear stock bajo": llamar a mcp__sqlite__read_query con SELECT id, name, qty FROM items WHERE qty <= ? con threshold parametrizable (default 5). Devolver tabla legible.
2. "agregar item": validar que name es string no vacío y qty es int >= 0. Llamar a mcp__sqlite__write_query con INSERT parametrizado. Confirmar éxito devolviendo el id nuevo.
3. "consolidar duplicados": detectar items con mismo name vía SELECT, mostrarle al usuario los pares duplicados, y SÓLO tras confirmación explícita ejecutar UPDATE+DELETE para unificar qty.

Restricciones:
- La Skill NUNCA construye SQL por concatenación. Siempre placeholders.
- Operaciones destructivas (delete, consolidar) requieren confirmación explícita del usuario antes de ejecutar.
- Frontmatter YAML válido con name=inventory-ops y description en tercera persona explicando QUÉ hace y CUÁNDO usarla.
- Cuerpo bajo 200 líneas. Usar progressive disclosure: lo procedural arriba, ejemplos abajo.
```

```
/speckit.plan
Un único archivo SKILL.md. No requiere scripts auxiliares. Estructura:
- Frontmatter YAML: name, description (con triggers: "inventory", "stock", "items", "consolidate").
- ## Tools required: mcp__sqlite__read_query, mcp__sqlite__write_query.
- ## When to use: bullets.
- ## Procedures: 3 secciones numeradas (chequear stock, agregar item, consolidar).
- ## Safety rules: bullets con las reglas de no-concat y confirmación.
```

```
/speckit.tasks
```

```
/speckit.implement
```

**SKILL.md final esperado como artefacto** (referencia para validación; el `implement` de Claude debería producir algo así):

```markdown
---
name: inventory-ops
description: Manages local SQLite inventory operations including stock checks, adding items, and consolidating duplicates. Use when the user asks about inventory, items, stock levels, low stock, adding products, or consolidating duplicate entries in the local items database.
---

# Inventory Ops

## Tools required
- `mcp__sqlite__read_query`
- `mcp__sqlite__write_query`
- `mcp__sqlite__list_tables` (verification)

## When to use
- The user asks "what's running low?", "show me low stock", "items under X".
- The user wants to add a new item with a name and quantity.
- The user mentions duplicate items or asks to consolidate inventory.

## Procedures

### 1. Check low stock
1. Default threshold: 5. If the user gives a number, use that.
2. Call `mcp__sqlite__read_query` with:
   `SELECT id, name, qty FROM items WHERE qty <= ? ORDER BY qty ASC`
   and the threshold as the parameter.
3. Render the result as a markdown table.

### 2. Add an item
1. Require `name` (non-empty string) and `qty` (integer >= 0). If invalid, ask the user before proceeding.
2. Call `mcp__sqlite__write_query` with:
   `INSERT INTO items (name, qty) VALUES (?, ?)`
   and the validated values.
3. Report the returned id back to the user.

### 3. Consolidate duplicates
1. Call `mcp__sqlite__read_query` with:
   `SELECT name, COUNT(*) AS c, SUM(qty) AS total_qty FROM items GROUP BY name HAVING c > 1`
2. Show the user the duplicates and the consolidated totals.
3. **Ask for explicit confirmation** before any write.
4. On confirmation, for each duplicated name:
   - UPDATE the row with the lowest id to have qty = total_qty.
   - DELETE the remaining rows for that name.
5. Report the final state back.

## Safety rules
- Never build SQL by string concatenation. Always use `?` placeholders.
- Any operation that modifies or deletes data requires explicit user confirmation in the same turn.
- If the connection to the sqlite MCP server fails, do not silently retry; surface the error.
```

### A6. 2-3 ejemplos concretos de Skills útiles para MLOps

#### A6.1 `model-validation`

```markdown
---
name: model-validation
description: Validates a candidate model artifact against minimum metrics, schema, and the project's model registry conventions before allowing a merge to models/main. Use when the user asks to validate a model, check a candidate, or prepare a model promotion.
---

# Model Validation

## When to use
- "Validate model X", "is this model ready", "check candidate before merge".

## Tools required
- Bash (to run evaluation scripts)
- Read (to inspect metrics.json and the model card)

## Procedure
1. Read `candidates/<model_id>/metrics.json`. Fail loud if missing.
2. Check thresholds: AUC >= 0.85, latency_p95_ms <= 50, model_size_mb <= 200.
3. Read `candidates/<model_id>/model_card.md`. Verify sections "Intended use", "Limitations", "Training data" exist.
4. Verify the input/output schema in `schema.json` matches the schema of the current production model.
5. Emit a markdown report with PASS/FAIL per check. Recommend merge only if ALL pass.

## Safety rules
- Do not modify the candidate. Read-only.
- If any threshold fails, explain WHY in human terms.
```

#### A6.2 `datadrift-report`

```markdown
---
name: datadrift-report
description: Generates the weekly data drift report by comparing feature distributions in the current snapshot vs the training baseline, using Kolmogorov-Smirnov tests per numeric feature and chi-square for categorical ones. Use when the user asks for a drift report, weekly drift, or feature distribution check.
---

# Data Drift Report

## When to use
- Mondays. "Drift report", "weekly drift", "have features moved".

## Tools required
- Bash (run the drift script)
- Read (inspect the resulting JSON)

## Procedure
1. Run `python scripts/compute_drift.py --baseline baselines/train.parquet --current snapshots/$(date +%Y-%m-%d).parquet --out /tmp/drift.json`.
2. Read `/tmp/drift.json`.
3. Emit markdown: table of feature, KS or chi2 stat, p-value, verdict (OK / DRIFT).
4. Highlight features with p < 0.01 in bold and recommend retraining if more than 3 features drifted.

## Safety rules
- Never modify baselines.
- If the script fails, surface the stderr verbatim; do not invent results.
```

#### A6.3 `deploy-checklist`

```markdown
---
name: deploy-checklist
description: Runs the pre-production deploy checklist for an ML service. Verifies tests, lint, changelog, observability hooks, rollback plan, and SLOs. Use before any merge to main or any tag intended for production deploy.
---

# Deploy Checklist

## When to use
- "Ready to deploy?", "preflight", "checklist before prod".

## Tools required
- Bash, Read

## Procedure
1. Run `pytest -q` — must pass.
2. Run `ruff check .` — must pass.
3. Verify `CHANGELOG.md` has an entry for the current version.
4. Verify `src/observability/` exports metrics (latency, error_rate, prediction_distribution).
5. Verify `docs/rollback.md` exists and references the previous deploy tag.
6. Check the SLO doc references p95 < 200ms and error_rate < 0.5%.
7. Emit a markdown checklist with ✅ / ❌ per item.

## Safety rules
- Read-only. Never modify code or config.
- If any item fails, block deploy explicitly with "DO NOT DEPLOY".
```

### A7. Diseñá tu propio SDD basado en Skills

Spec Kit es un sabor de SDD: el de GitHub. Vos podés escribir el sabor de tu empresa como Skills. La idea:

```
.claude/skills/
  our-specify/
    SKILL.md         # cómo escribimos specs acá: secciones obligatorias, plantilla
  our-plan/
    SKILL.md         # cómo escribimos plans: stack default, observabilidad obligatoria
  our-tasks/
    SKILL.md         # cómo dividimos tareas: tamaños máx, criterios de done
  our-implement/
    SKILL.md         # cómo implementamos: pre-commit hooks, branch naming
```

Ejemplo de `our-specify/SKILL.md`:

```markdown
---
name: our-specify
description: Acme Inc. specification authoring procedure. Use when the user wants to start a new feature spec. Replaces the generic /speckit.specify with company-specific sections: SLO targets, data lineage, compliance scope, and rollout strategy.
---

# Acme spec

## When to use
- New feature, new endpoint, new model in production.

## Procedure
1. Crear rama `feat/<short-name>` desde `main`.
2. Crear `specs/<NNN>-<short-name>/spec.md` con estas secciones obligatorias:
   - Motivation (link al ticket)
   - User scenarios
   - Functional requirements
   - **SLO targets** (latencia p95, throughput, error rate) ← obligatorio en Acme
   - **Data lineage** (qué tablas se tocan, qué PII puede haber) ← obligatorio en Acme
   - **Compliance scope** (GDPR/SOC2 si aplica) ← obligatorio
   - **Rollout strategy** (canary, dark, full) ← obligatorio
   - Success criteria
3. Validar contra el `constitution.md` de Acme antes de seguir.

## Safety rules
- Si falta SLO o data lineage, no avanzar a `/our-plan`.
```

Resultado: tu equipo tiene **el SDD de Acme**, no el SDD genérico. El procedimiento queda versionado en el repo, igual que el código.

### A8. TROUBLESHOOTING

**Spec Kit / Specify CLI**

| Síntoma | Causa | Fix |
|---|---|---|
| `command not found: specify` después de `uv tool install` | El directorio de bin de uv no está en el PATH | Abrir terminal nueva, o `export PATH="$HOME/.local/bin:$PATH"` |
| `specify init` ofrece sólo GitHub Copilot, no Claude | Estás en modo no-interactivo, default es Copilot | Pasar `--integration claude` explícito |
| Los slash commands no aparecen en Claude Code después de init | Claude no releyó `.claude/commands/` | Reiniciar la sesión Claude Code completa (no es suficiente con re-cargar workspace) |
| Estás usando `/specify` y no funciona | Versión vieja del tutorial; los comandos hoy son namespaced | Usar `/speckit.specify`, `/speckit.plan`, etc. |
| Querés actualizar Spec Kit | `uv tool install --force --from git+...` lo refresca | `uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git` |

**Claude Code**

| Síntoma | Causa | Fix |
|---|---|---|
| `command not found: claude` después de instalar | PATH no recargado | Terminal nueva, o `source ~/.zshrc` / `source ~/.bashrc` |
| EACCES al hacer `npm install -g @anthropic-ai/claude-code` | `sudo` o prefix de npm root-owned | NO usar `sudo`. `npm config set prefix ~/.npm-global` y agregar al PATH; o usar el native installer |
| Node version < 18 | claude-code requiere 18+ | `nvm install --lts && nvm use --lts` |
| OAuth no abre browser (SSH / devcontainer) | Localhost callback bloqueado | Copiar la URL impresa en terminal, completar en otro navegador, pegar el code de vuelta |
| `ANTHROPIC_API_KEY` configurada pero claude no la usa | claude pide aprobación explícita la primera vez | Confirmar la prompt de "trust this API key?"; después persiste |

**MCP de SQLite**

| Síntoma | Causa | Fix |
|---|---|---|
| `claude mcp list` muestra `disconnected` para sqlite | Mil cosas; correr el comando standalone para ver el error real | `npx -y mcp-server-sqlite-npx /abs/path/to/db.db` y leer el stderr |
| Windows: "Connection closed" | Falta `cmd /c` antes de `npx` | Re-agregar con `claude mcp add ... -- cmd /c npx -y mcp-server-sqlite-npx ...` |
| `spawn npx ENOENT` | El subprocess de Claude Code no encuentra `npx` (no carga nvm en shells no interactivas) | Usar path absoluto a `npx` (ej. `/Users/you/.nvm/versions/node/v22.12.0/bin/npx`) o mover el init de nvm a `~/.zshenv` |
| El MCP conecta pero `list_tables` devuelve vacío | Usaste path relativo y abrió otra DB | Siempre absoluto: `$(pwd)/items.db` o ruta completa |
| `~/test.db` no funciona | `~` no se expande en args de MCP | Usar `$HOME/test.db` o path absoluto completo |
| Los flags como `--scope` no funcionan | Los flags van **antes** del nombre del servidor, no después | `claude mcp add --transport stdio --scope project sqlite -- ...` correcto; `claude mcp add sqlite --scope project ...` incorrecto |
| Project scope: el server "desaparece" después de clonar | Claude Code pide aprobación de seguridad para `.mcp.json` la primera vez | Aceptar el prompt; o `claude mcp reset-project-choices` para reiniciar |

**Skills**

| Síntoma | Causa | Fix |
|---|---|---|
| La Skill no se activa nunca | `description` muy genérica | Reescribir la description con triggers explícitos en tercera persona: "Use when the user asks X, Y, or Z" |
| `SKILL.md` no se carga | Archivo mal nombrado (case-sensitive) o frontmatter inválido | Confirmar nombre exacto `SKILL.md`, frontmatter entre `---` en la primera línea |
| Skill duplicada en personal y project | Conflict de nombres | Recordá la precedencia: enterprise > personal > project. Renombrá una. |
| Querés listar las Skills activas | Slash command built-in | `/skills` dentro de Claude Code |

**Flask + SQLite**

| Síntoma | Causa | Fix |
|---|---|---|
| `sqlite3.OperationalError: no such table: items` | Olvidaste correr `init_db.py` | `python init_db.py` antes de `python app.py` |
| El POST tira 400 con payload válido | Falta `Content-Type: application/json` | Agregar el header al curl |
| Puerto 5000 ocupado (macOS) | AirPlay receiver de macOS usa 5000 | Cambiar el puerto en `app.py` a 5001, o desactivar AirPlay receiver en Settings |

---

*Fin del material. Versiones referenciadas en este documento (verificadas a 2 de junio de 2026): Spec Kit v0.8.18 (29-may-2026), Flask 3.1.3 (19-feb-2026), `@anthropic-ai/claude-code` v2.1.x, `mcp-server-sqlite-npx` v0.8.0 (25-oct-2025), uv 0.11.x. Si encontrás divergencias entre lo escrito acá y la documentación oficial actual, prevalece la documentación oficial.*