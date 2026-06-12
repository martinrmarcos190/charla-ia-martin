---
name: issues-ops
description: Opera el registro de issues de infraestructura (listar, consultar, crear y actualizar) a través del MCP issues-api, y analiza archivos de logs para crear o actualizar issues con evidencia. Usar cuando el usuario pida ver, crear, editar o resolver issues, o analizar logs.
---

# issues-ops

> Solución de referencia del facilitador. La sección "Análisis de logs" es la
> evolución que se agrega en el Bloque 5 (spec-logs.md); hasta el Bloque 4 la
> skill llega hasta "Procedimiento".

## Cuándo usar
Usá esta skill cuando el usuario quiera listar issues, consultar uno por id,
crear un issue nuevo, actualizar uno existente (cambiar status, severity,
descripción o solución), o analizar un archivo de logs.

## Reglas
- Usá siempre los nombres calificados de las tools del MCP:
  - `issues-api:list_issues`
  - `issues-api:get_issue`
  - `issues-api:add_issue`
  - `issues-api:update_issue`
- Validá los enums antes de llamar a la tool:
  - `severity` ∈ {low, medium, high, critical}
  - `status` ∈ {open, investigating, resolved}
  Si el valor pedido no es válido, pedí corrección.
- **Para marcar un issue como `resolved`, `proposed_solution` no puede quedar
  vacía**: si falta, pedila o redactala con el usuario antes de actualizar.
- Después de crear o actualizar, confirmá leyendo el issue con
  `issues-api:get_issue` y mostralo legible.

## Procedimiento
1. Identificá la intención (listar / consultar / crear / actualizar / analizar logs).
2. Para crear: validá campos (`title`, `service`, `severity`) y enums.
3. Para actualizar: validá enums y la regla de `resolved`.
4. Ejecutá la tool correspondiente.
5. Mostrá el resultado de forma legible.

## Análisis forense de logs distribuidos
Cuando el usuario pida analizar logs (te pasa una carpeta con varios archivos:
gateway, servicios, infraestructura):

1. Inventariá los archivos y entendé qué capa describe cada uno.
2. Separá síntomas de ruido: errores que se auto-resuelven (retry OK), issues
   marcados como conocidos en el propio log y chatter operativo **no son
   hallazgos** — descartalos explícitamente con justificación.
3. Buscá anomalías aunque no haya ERROR:
   - **Periodicidad**: síntomas en ventanas regulares → ¿qué evento de otra
     capa coincide con el inicio de cada ventana?
   - **Tendencias**: métricas dentro de INFOs que degradan gradualmente
     (pools, heap, disco) → ¿qué evento puntual inició la tendencia?
   - **Ventanas acotadas**: ráfagas que empiezan y terminan de golpe → ¿qué
     evento puntual las abre?
4. Construí la cadena causal completa: evento origen (archivo + timestamp) →
   efecto intermedio → síntoma. Citá 1-2 líneas de **cada archivo** involucrado.
5. Compará contra los issues existentes con `issues-api:list_issues`:
   - El hallazgo explica un issue registrado → `issues-api:update_issue`
     sumando causa raíz + evidencia a `description` (sin borrar lo original) y
     un fix dirigido a la causa en `proposed_solution`.
   - Problema nuevo → `issues-api:add_issue` con severity según impacto.
6. Nunca dupliques: ante la duda, consultá con `issues-api:get_issue`; si sigue
   ambiguo, preguntá al usuario.
7. Cerrá con un informe: tabla causa raíz → síntoma → issue actualizado/creado,
   y la lista de descartados con el porqué.
