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

## Análisis de logs
Cuando el usuario pida analizar un archivo de logs (te pasa la ruta):

1. Leé el archivo completo. Formato: `timestamp [NIVEL] servicio mensaje`.
2. Ignorá el ruido: INFO de requests normales, health checks y cache no son issues.
3. Agrupá los problemas por patrón (mismo servicio + mismo tipo de error), con
   frecuencia y ventana temporal (primera y última aparición).
4. Compará contra los issues existentes con `issues-api:list_issues`:
   - Patrón que matchea un issue registrado → `issues-api:update_issue`,
     sumando a `description` la evidencia (frecuencia, ventana, 1-2 líneas de
     log representativas) sin borrar lo original.
   - Patrón nuevo → `issues-api:add_issue` con severity según frecuencia y
     criticidad (FATAL recurrente o recurso ≥95% = critical; warnings
     preventivos = medium/low) y una `proposed_solution` concreta.
5. Correlacioná señales entre servicios (p. ej. disco de la DB llenándose y
   backups de esa DB fallando): decilo explícitamente y sumá la hipótesis de
   causa raíz al issue correspondiente.
6. Nunca dupliques: ante la duda, consultá con `issues-api:get_issue`; si sigue
   ambiguo, preguntá al usuario.
7. Cerrá con un resumen: issues creados, actualizados y descartados como ruido.
