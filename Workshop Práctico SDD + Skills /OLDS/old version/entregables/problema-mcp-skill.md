# Problema: MCP propio + Skill para operar el inventario

> Este es el documento que recibís en el **Bloque 4**. Tiene todo lo necesario para que lo **construyas en clase**: primero un MCP que le pega a la API del Bloque 3, después una Skill (vía SDD) que lo usa con criterio. No hay código resuelto: lo programamos juntos.

## Contexto
Ya tenés la API de inventario del Bloque 3 corriendo en `http://127.0.0.1:5000` (los endpoints `GET/POST /models`, etc.). Ahora querés que Claude Code pueda **operar ese inventario** por su cuenta: listar, consultar y dar de alta modelos, pero siguiendo el criterio de tu equipo.

Para eso necesitás dos piezas:
- **Un MCP server** que exponga las operaciones del inventario como *tools* → la **conectividad**.
- **Una Skill** que le enseñe a Claude **cómo** usar esas tools bien → el **procedimiento**.

> Requisito previo: la API Flask del Bloque 3 tiene que estar **corriendo** durante todo este bloque.

---

## PARTE A — El MCP server `items-api`

### Objetivo
Un MCP server local que traduzca pedidos del modelo en llamadas HTTP a la API del Bloque 3.

### Stack obligatorio
- SDK **oficial** de MCP para Python: paquete `mcp` (usá `FastMCP`).
- Cliente HTTP: `httpx`.
- Transporte: **stdio** (local, mismo árbol de proceso).
- Entorno con `uv`.

### Setup (lo tipeás vos)
```bash
uv init mcp-items && cd mcp-items
uv venv && source .venv/bin/activate
uv add "mcp[cli]" httpx
```

### Tools que tiene que exponer
El server se llama `items-api` y expone exactamente estas tres tools (cada una con su docstring, que es lo que el modelo lee para decidir cuándo usarla):

| Tool | Firma | Qué hace |
|---|---|---|
| `list_models` | `() -> str` | `GET /models` → devuelve todos los modelos del inventario |
| `get_model` | `(model_id: int) -> str` | `GET /models/<id>` → un modelo por id; si es 404, avisa que no existe |
| `add_model` | `(name: str, framework: str, accuracy: float) -> str` | `POST /models` con el body JSON → crea un modelo y devuelve el id |

Apuntá todas contra `API_BASE = "http://127.0.0.1:5000"`.

### Restricción crítica (no la saltees)
En transporte **stdio, NUNCA escribas a stdout** (un `print()` corrompe el JSON-RPC y el server deja de funcionar). Si querés loguear, mandá todo a `stderr` (`logging.basicConfig(stream=sys.stderr)`).

### Arranque
El server arranca con `mcp.run(transport="stdio")`.

### Registrar y verificar en Claude Code
```bash
claude mcp add items-api -- uv run server.py
claude mcp list                 # items-api debe aparecer "connected"
# dentro de una sesión de Claude Code:
/mcp                            # muestra estado y las 3 tools
```
> Para compartirlo con el equipo (genera un `.mcp.json` commiteable): agregá `--scope project`.
> Los servers stdio descubren las tools al **inicio de la sesión**: si registrás el MCP a mitad de una sesión, abrí una sesión nueva.

### Criterios de aceptación (Parte A)
- `claude mcp list` muestra `items-api` conectado.
- `/mcp` lista las tres tools: `list_models`, `get_model`, `add_model`.
- Pedirle a Claude "listá los modelos" hace que invoque `items-api:list_models` y devuelva los seeds del Bloque 3.

---

## PARTE B — La Skill `items-ops` (vía SDD)

Ahora le damos **criterio**. La Skill la generás con el mismo flujo SDD que usaste para la app: `/speckit.specify` → `plan` → `tasks` → `implement`.

### Spec para pegar en `/speckit.specify`

> Quiero una Skill de Claude Code llamada `items-ops` que opere el inventario de modelos a través de las tools del MCP `items-api`. Generá vía SDD (specify/plan/tasks/implement) la Skill completa. La Skill debe:
>
> 1. Explicar **cuándo usarse** (cuando el usuario pida listar, consultar o agregar modelos al inventario).
> 2. Instruir a Claude a usar SIEMPRE los **nombres calificados** de las tools del MCP: `items-api:list_models`, `items-api:get_model`, `items-api:add_model`.
> 3. **Validar** que `accuracy` esté entre 0 y 1 antes de un alta; si no, pedir corrección.
> 4. Ante un alta, **confirmar** el id devuelto leyendo el modelo con `items-api:get_model`.
>
> El `SKILL.md` debe tener frontmatter YAML con `name: items-ops` y un `description` en tercera persona (máx. 1024 caracteres) que diga qué hace y cuándo usarse. Cuerpo por debajo de 500 líneas. Ubicación: `.claude/skills/items-ops/SKILL.md`.

### Pasos
1. `/speckit.specify` pegando la spec de arriba.
2. `/speckit.plan` (Claude Code, MCP `items-api`, sin dependencias extra).
3. `/speckit.tasks` y luego `/speckit.implement`.
4. Si la carpeta de skills es nueva, **reiniciá Claude Code** (no alcanza `/reload-skills` para directorios que no existían al arrancar la sesión).

### Requisitos del frontmatter (recordatorio)
- `name`: máximo 64 caracteres, solo minúsculas, números y guiones.
- `description`: máximo 1024 caracteres, en tercera persona, **qué hace + cuándo usarse**. Es lo único que Claude lee al arrancar: si está mal escrito, la Skill no se activa nunca.

---

## Prueba end-to-end (definición de hecho)

Con la API Flask corriendo, el MCP `items-api` conectado y la Skill `items-ops` cargada, pedile a Claude en **lenguaje natural** (sin nombrar la Skill):

```text
Listame los modelos del inventario y agregá uno: bert-base, pytorch, accuracy 0.91.
```

Tiene que pasar todo esto, solo:
- La Skill `items-ops` se activa sola (por su `description`).
- Lista los modelos vía `items-api:list_models`.
- Valida que `0.91 ∈ [0, 1]`.
- Da de alta con `items-api:add_model` y obtiene un `id`.
- Confirma el id leyéndolo con `items-api:get_model`.

Y lo verificás por afuera:
```bash
curl http://127.0.0.1:5000/models/3
```

> Si todo eso funciona: construiste la conectividad (MCP) y el procedimiento (Skill), y los uniste — Skill que da el **criterio**, MCP que da la **capacidad**, API que **ejecuta**.
