# Workshop SDD + Skills — Guía del facilitador

Todo lo necesario para dar la **Clase 3** (taller práctico, 150 min). Material para participantes y para el facilitador, con los prompts copy-paste.

## Mapa de archivos

| Archivo | Para | Cuándo |
|---|---|---|
| `../index.html` | Proyectar | Toda la clase (deck reveal.js, 28 slides) |
| `../notas_orador.html` | Solo el facilitador | Toda la clase (cronómetro + guion por slide) |
| `material-previo.md` | Participantes | **3–4 días antes** de la clase |
| `problema-inventario.md` | Participantes | **Bloque 3** — el problema de la app, lo construyen vía SDD |
| `problema-mcp-skill.md` | Participantes | **Bloque 4** — el problema del MCP + la Skill, lo construyen en vivo |

> **No hay código resuelto en `entregables/`, a propósito.** La app (`app.py`), el MCP (`server.py`) y la Skill (`SKILL.md`) **se programan en clase** vía SDD a partir de los dos `.md` de problema. El código de referencia del MCP está en la **slide 18 del deck** como apoyo visual durante el armado en vivo.

## Reparto de bloques (150 min)

| | Bloque | Min |
|---|---|---|
| B0 | Apertura + checklist de entorno | 10 |
| B1 | Fundamentos de SDD + Spec Kit | 25 |
| B2 | Setup hands-on (repo + Spec Kit) | 25 |
| B3 | Flujo SDD completo (la app) | 45 |
| B4 | Skill con SDD + MCP propio | 35 |
| B5 | Reflexión y cierre | 10 |

---

## Prompts copy-paste

### Bloque 2 — Setup
```bash
mkdir taller-sdd && cd taller-sdd
git init
claude            # primera vez: autenticar en el navegador
# dentro de Claude Code:
/init
# después, en la terminal:
specify init . --integration claude
ls .specify/ .claude/commands/
# dentro de Claude Code: tipear "/" y confirmar los /speckit.*
```

### Bloque 3 — Flujo SDD completo
```text
/speckit.constitution Proyecto local y simple. Solo stdlib + Flask. SQLite con el módulo sqlite3. Sin auth. Tests con curl. Código documentado.

/speckit.specify   <pegar el contenido de problema-inventario.md>
/speckit.clarify   <responder las preguntas que haga>
/speckit.plan      Flask + módulo sqlite3 de la stdlib, sin dependencias extra.
/speckit.tasks
/speckit.analyze
/speckit.implement
```
Probar la app generada:
```bash
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/models
curl -X POST http://127.0.0.1:5000/models -H "Content-Type: application/json" \
  -d '{"name":"bert-base","framework":"pytorch","accuracy":0.91}'
curl http://127.0.0.1:5000/models/1
```

### Bloque 4 — MCP propio (se construye en vivo según `problema-mcp-skill.md`, Parte A)
```bash
uv init mcp-items && cd mcp-items
uv venv && source .venv/bin/activate
uv add "mcp[cli]" httpx
# se programa server.py en clase (3 tools, FastMCP, stdio; ver slide 18), después:
claude mcp add items-api -- uv run server.py
claude mcp list
# dentro de Claude Code: /mcp
```
> La API Flask del Bloque 3 tiene que estar **corriendo** para que el MCP le pegue.

### Bloque 4 — Skill vía SDD (Parte B de `problema-mcp-skill.md`)
```text
/speckit.specify   <pegar la spec de la Skill que está en problema-mcp-skill.md (Parte B)>
/speckit.plan      Claude Code, MCP items-api, sin dependencias extra.
/speckit.tasks
/speckit.implement
# carpeta de skills nueva → reiniciar Claude Code (o /reload-skills si ya existía)
```
Prueba end-to-end (en Claude Code):
```text
Listame los modelos del inventario y agregá uno: bert-base, pytorch, accuracy 0.91.
```

---

## Recomendaciones

1. **Antes del taller:** mandá `material-previo.md` con 3–4 días de anticipación y pedí que peguen el output del checklist en un canal. Quien no lo complete no debería arrancar el Bloque 2 en vivo.
2. **La noche anterior:** abrí `index.html` y `notas_orador.html` en Chrome y revisalos. Corré `specify check` y confirmá los nombres de comandos con `/` dentro de Claude Code (Spec Kit se mueve rápido).
3. **Pinneá versiones** si querés que todos vean lo mismo: Spec Kit `@v0.8.18`, MCP SDK `uv add "mcp[cli]==1.27.1"`.
4. **Umbral de decisión:** si más del 20% tiene el entorno roto al minuto 8, corré el Bloque 2 como "setup asistido" extendido y recortá 10 min del Bloque 3 (estimación + una sola pasada de SDD).

## Troubleshooting de errores comunes

- **Python viejo / no encontrado:** `python3 --version`. Si es <3.11, `uv python install 3.12`. Spec Kit y el SDK de MCP requieren Python ≥3.10.
- **`uv`/`uvx` "command not found":** reabrí la terminal (el instalador modifica el perfil de shell). Si persiste, agregá `~/.local/bin` al PATH.
- **Claude Code "command not found":** abrí una terminal nueva o `source ~/.zshrc` / `~/.bashrc`. El binario nativo queda en `~/.local/bin/claude`.
- **Node viejo (instalación npm):** la vía npm (legada) requiere Node 18+. Mejor usá el instalador nativo. Nunca `sudo npm`.
- **Registro del MCP falla / 0 tools:** corré el server a mano para ver errores en stderr; revisá que no haya `print()` a stdout (corrompe el JSON-RPC). Los servers stdio descubren tools al inicio de sesión: si lo agregaste a mitad, abrí una sesión nueva. Verificá con `claude mcp list` y `/mcp`.
- **No aparecen los `/speckit.*`:** carpeta equivocada o falta reiniciar Claude Code. Confirmá con `ls .claude/commands/`. Usá `--integration claude`, no el viejo `--ai`.
- **Flask/SQLite:** "no such table" = no inicializaste la DB (`init_db()` antes del primer query); si el POST falla, verificá `-H "Content-Type: application/json"`; el puerto 5000 ocupado → cambialo.

## Caveats (datos sensibles a fecha)

- Spec Kit estable a 0.8.18 (29-may-2026), 0.9.0 en desarrollo: verificá `specify check` el día.
- El SDK `mcp` figura como "Beta" en PyPI; el `server.py` usa solo lo estable (FastMCP + stdio). La patch exacta (1.27.0 vs 1.27.1) puede variar; pinneá la que verifiques.
- La instalación npm de Claude Code está deprecada pero funciona; priorizá el instalador nativo en clase.
- Windows nativo difiere; recomendá WSL2 para uniformar.
