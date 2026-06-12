# Taller práctico (Clase 3): Spec-Driven Development + Skills para DevOps

Edición **dual-track** · ~195 min (núcleo 150' + extensión B5/B6) · 🟧 **[A]** Claude Code + Spec Kit · 🟪 **[B]** Kiro (AWS)

> Idea de fondo (anti lock-in): **SDD, MCP y Skills son estándares abiertos**.
> Todo se construye **desde cero vía specs** (nada de pegar código): los `.md` de
> specs (problema, MCP, skills, plugin) son **idénticos** en ambas herramientas;
> solo cambia *cómo se crean las specs y dónde se registran*. Las soluciones de
> referencia quedan archivadas en `OLDS/recursos/`.

**El caso:** un equipo de DevOps registra **issues de infraestructura** en una
API local. Sobre eso se construye un MCP, una skill que opera los issues **y
analiza logs**, una skill que genera el **reporte HTML**, y al final todo se
empaqueta en un **plugin/Power** instalable.

## Contenido del paquete

```
Workshop Práctico SDD + Skills/
├── README.md                         ← este archivo (índice)
├── material-previo.md                ← Parte 1 · para participantes (mandar 3-4 días antes)
├── guion-facilitador.html            ← Parte 2 · guion minuto a minuto — índice + timeline
├── slides/
│   ├── bloque1-fundamentos-sdd.html  ← deck Bloque 1 (qué es SDD)
│   ├── bloque2-setup.html            ← deck Bloque 2 (setup hands-on por camino)
│   └── bloque7-reflexion.html        ← deck Bloque 7 (cierre y extensión)
└── recursos/                         ← organizado por bloque
    ├── bloque3-api/
    │   ├── problema.md               ← spec del problema: API de issues (tool-agnostic)
    │   ├── constitution.example.md   ← 🟧 [A] constitución de ejemplo
    │   └── steering.example.md       ← 🟪 [B] steering file de ejemplo
    ├── bloque4-mcp-skill/
    │   ├── spec-mcp.md               ← spec del MCP issues-api (tool-agnostic)
    │   ├── spec-skill.md             ← spec de la skill issues-ops (tool-agnostic)
    │   ├── seed.sh                   ← carga ~8 issues de ejemplo vía POST/PUT
    │   └── mcp.json.example          ← 🟪 [B] registro MCP para Kiro
    ├── bloque5-logs/
    │   ├── spec-logs.md              ← spec: la skill aprende a leer logs (evolución)
    │   └── logs/                     ← gateway + services + infra (~3900 líneas,
    │                                    4 historias que solo se resuelven correlacionando
    │                                    ENTRE archivos; respuestas en OLDS/recursos/logs-respuestas.md)
    └── bloque6-reporte-plugin/
        ├── spec-report.md            ← spec de la skill issues-report
        └── spec-plugin.md            ← spec del empaquetado devops-issues

(El app.py de la API, el server.py del MCP y los SKILL.md se generan en vivo vía
SDD; las soluciones de referencia quedaron archivadas en OLDS/recursos/.)
```

## Distribución a participantes

Lo que reciben los participantes (material-previo + specs + logs + examples +
seed.sh, **sin** soluciones de referencia) vive en el repo público:
**https://github.com/martinrmarcos190/repo-charla-ia** — mandales ese link junto
con el material previo. Si cambiás una spec acá, replicá el cambio allá y pusheá.

## Cómo presentar los slides

Abrí cualquier `.html` de `slides/` en Chrome (doble clic). Navegación:
**→ / Space / ↓** avanza, **← / ↑** retrocede, **Home / End** primer/último
slide. Son autocontenidos (no necesitan internet) y tema oscuro para proyección.

## Mapa de bloques (~195 min · B5/B6 elásticos)

| Bloque | Tiempo | Material |
|---|---|---|
| B0 · Apertura | 10' | `guion-facilitador.html` |
| B1 · Fundamentos de SDD | 25' | `slides/bloque1-fundamentos-sdd.html` |
| B2 · Setup hands-on | 25' | `slides/bloque2-setup.html` |
| B3 · Práctica guiada: API de issues | 45' | `recursos/bloque3-api/problema.md` (ref. en `OLDS/recursos/app.py`) |
| B4 · MCP + Skill | 35' | `recursos/bloque4-mcp-skill/spec-mcp.md`, `recursos/bloque4-mcp-skill/spec-skill.md`, `recursos/bloque4-mcp-skill/mcp.json.example`, `recursos/bloque4-mcp-skill/seed.sh` |
| B5 · La skill lee logs *(elástico)* | 20' | `recursos/bloque5-logs/spec-logs.md`, `recursos/bloque5-logs/logs/` (respuestas: `OLDS/recursos/logs-respuestas.md`) |
| B6 · Reporte + plugin *(elástico)* | 25' | `recursos/bloque6-reporte-plugin/spec-report.md`, `recursos/bloque6-reporte-plugin/spec-plugin.md` |
| B7 · Reflexión | 10' | `slides/bloque7-reflexion.html` |

> **Si el slot es de 2 h:** el taller cierra digno al final del B4 (la prueba
> integrada de la skill + MCP). B5 y B6 son la extensión para slots de 2.5-3 h.

## Checklist de versiones (verificar el día del taller)

- 🟧 **[A]** Spec Kit `0.8.18` (`specify check`, `specify version`); init con `--integration claude` (no el viejo `--ai`).
- 🟧 **[A]** Claude Code: instalador nativo (`~/.local/bin/claude`), `claude --version` / `claude doctor`.
- 🟧 **[A]** Plugins (B6): flujo verificado contra la doc oficial (`--plugin-dir` para probar; marketplace local + `/plugin install` + `/reload-plugins` para distribuir). Solo dar una pasada rápida ese día por si cambió.
- 🟪 **[B]** Kiro: confirmar nombres de variantes (Requirements-First / Design-First / Quick Plan), panel Specs, y si los **Powers** de la versión soportan skills adentro (B6).
- 🟩 SDK MCP: paquete `mcp` (≈1.27.x, Python ≥3.10). Pinneá la patch que verifiques.

> El documento maestro v1 (edición "inventario de modelos") quedó archivado en
> `OLDS/`. Esta versión DevOps (issues + logs + reporte + plugin) es la vigente.
