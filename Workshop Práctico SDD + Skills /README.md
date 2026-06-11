# Taller práctico (Clase 3): Spec-Driven Development + Claude Skills

Edición **dual-track** · 150 min · 🟧 **[A]** Claude Code + Spec Kit · 🟪 **[B]** Kiro (AWS)

> Idea de fondo (anti lock-in): **SDD, MCP y Skills son estándares abiertos**.
> Todo se construye **desde cero vía specs** (nada de pegar código): los `.md` de
> specs (problema, MCP, Skill) son **idénticos** en ambas herramientas; solo
> cambia *cómo se crean las specs y dónde se registran*. El `server.py` del MCP y
> el `SKILL.md` se generan en vivo; sus soluciones de referencia quedan archivadas
> en `OLDS/recursos/`.

## Contenido del paquete

```
Workshop Práctico SDD + Skills/
├── README.md                         ← este archivo (índice)
├── material-previo.md                ← Parte 1 · para participantes (mandar 3-4 días antes)
├── guion-facilitador.md              ← Parte 2 · guion minuto a minuto (150')
├── guion-facilitador.html            ← mismo guion en HTML para leer/proyectar (índice + timeline)
├── slides/
│   ├── bloque1-fundamentos-sdd.html  ← deck Bloque 1 (qué es SDD)
│   ├── bloque2-setup.html            ← deck Bloque 2 (setup hands-on por camino)
│   └── bloque5-reflexion.html        ← deck Bloque 5 (cierre y extensión)
└── recursos/
    ├── problema.md                   ← el .md del problema, se arma vía specs (tool-agnostic, Bloque 3)
    ├── spec-mcp.md                   ← spec del MCP para pegar, se arma vía specs (tool-agnostic, Bloque 4)
    ├── spec-skill.md                 ← spec de la Skill para pegar, se arma vía specs (tool-agnostic, Bloque 4)
    ├── seed.sh                       ← carga ~10 modelos de ejemplo vía POST /models (poblar inventario)
    └── examples/
        ├── constitution.example.md   ← 🟧 [A] constitución de ejemplo
        ├── steering.example.md       ← 🟪 [B] steering file de ejemplo
        └── mcp.json.example          ← 🟪 [B] registro MCP para Kiro

(El app.py de la API, el server.py del MCP y el SKILL.md se generan en vivo vía
SDD; las soluciones de referencia quedaron archivadas en OLDS/recursos/.)
```

## Cómo presentar los slides

Abrí cualquier `.html` de `slides/` en Chrome (doble clic). Navegación:
**→ / Space / ↓** avanza, **← / ↑** retrocede, **Home / End** primer/último
slide. Son autocontenidos (no necesitan internet) y tema oscuro para proyección.

## Mapa de bloques (150 min)

| Bloque | Tiempo | Material |
|---|---|---|
| B0 · Apertura | 10' | `guion-facilitador.md` |
| B1 · Fundamentos de SDD | 25' | `slides/bloque1-fundamentos-sdd.html` |
| B2 · Setup hands-on | 25' | `slides/bloque2-setup.html` |
| B3 · Práctica guiada | 45' | `recursos/problema.md` (ref. en `OLDS/recursos/app.py`) |
| B4 · Skill + MCP | 35' | `recursos/spec-mcp.md`, `recursos/spec-skill.md`, `recursos/examples/mcp.json.example` (ref. en `OLDS/recursos/`) |
| B5 · Reflexión | 10' | `slides/bloque5-reflexion.html` |

## Checklist de versiones (verificar el día del taller)

- 🟧 **[A]** Spec Kit `0.8.18` (`specify check`, `specify version`); init con `--integration claude` (no el viejo `--ai`).
- 🟧 **[A]** Claude Code: instalador nativo (`~/.local/bin/claude`), `claude --version` / `claude doctor`.
- 🟪 **[B]** Kiro: confirmar nombres de variantes (Requirements-First / Design-First / Quick Plan) y ubicación del panel Specs.
- 🟩 SDK MCP: paquete `mcp` (≈1.27.x, Python ≥3.10). Pinneá la patch que verifiques.

> Fuente: el documento maestro `MD for Workshop Práctico SDD + Skills .md`
> (verificado contra docs oficiales a mediados de 2026).
