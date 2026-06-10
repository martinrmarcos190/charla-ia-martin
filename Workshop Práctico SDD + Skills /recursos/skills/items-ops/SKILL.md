---
name: items-ops
description: Opera el inventario de modelos (listar, consultar y dar de alta) a través del MCP items-api. Usar cuando el usuario pida ver, buscar o agregar modelos al inventario local.
---

# items-ops

## Cuándo usar
Usá esta skill cuando el usuario quiera listar modelos, consultar un modelo por
id, o dar de alta un modelo en el inventario.

## Reglas
- Usá siempre los nombres calificados de las tools del MCP:
  - `items-api:list_models`
  - `items-api:get_model`
  - `items-api:add_model`
- Antes de un alta, validá que `accuracy` esté entre 0 y 1. Si no, pedí corrección.
- Después de un alta, confirmá el `id` devuelto llamando a `items-api:get_model`.

## Procedimiento
1. Identificá la intención (listar / consultar / alta).
2. Para alta: validá campos (`name`, `framework`, `accuracy`).
3. Ejecutá la tool correspondiente.
4. Mostrá el resultado de forma legible.
