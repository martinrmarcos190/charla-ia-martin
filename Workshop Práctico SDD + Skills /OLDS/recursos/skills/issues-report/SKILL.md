---
name: issues-report
description: Genera un reporte HTML autocontenido del estado de los issues de infraestructura, obteniendo los datos exclusivamente vía el MCP issues-api. Usar cuando el usuario pida un reporte, dashboard o resumen del estado de los issues.
---

# issues-report

> Solución de referencia del facilitador (Bloque 6, spec-report.md).

## Cuándo usar
Cuando pidan un reporte, dashboard o resumen del estado de los issues.

## Reglas
- Los datos salen **EXCLUSIVAMENTE** de `issues-api:list_issues` (nombre
  calificado). No leas la base de datos ni el código de la API.
- El output es **un único archivo `issues-report.html` autocontenido**: CSS
  inline, sin assets externos, sin internet.

## Estructura del reporte
1. **Header**: título, fecha/hora de generación, totales por `status`
   (open / investigating / resolved) y por `severity`.
2. **Atención inmediata**: issues `critical` y `high` con status ≠ resolved.
   Si no hay, mostrar "sin críticos abiertos ✅".
3. **Tabla completa**: id, título, servicio, severity, status, solución
   propuesta. Severity con color: critical rojo, high naranja, medium amarillo,
   low gris.
4. **Base de conocimiento**: los `resolved` con sus soluciones.

## Procedimiento
1. Llamá a `issues-api:list_issues`.
2. Calculá los totales y agrupá por status/severity.
3. Generá `issues-report.html` con la estructura de arriba.
4. Decí dónde quedó el archivo y sugerí abrirlo en el navegador.
