# Problema: API local de inventario de modelos

> Este es el documento que recibís en el Bloque 3. Leelo, **estimá cuánto tardarías en hacerlo a mano**, anotá el número, y recién después lo automatizamos con SDD.

## Contexto
Necesitás un servicio local mínimo para registrar artefactos de modelos en un inventario. Todo corre en tu máquina, sin nube, sin auth.

## Objetivo
Levantar una base de datos local y un servidor Flask con endpoints GET y POST, y probarlos con `curl`.

## Stack obligatorio
- Python 3.11+, Flask, módulo `sqlite3` de la stdlib (sin ORM).
- Un solo archivo `app.py`. Base `inventory.db` creada automáticamente.

## Modelo de datos
Tabla `models`:
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `name` TEXT NOT NULL
- `framework` TEXT NOT NULL (ej. "pytorch", "sklearn")
- `accuracy` REAL
- `created_at` TEXT (timestamp ISO)

## Endpoints
1. `GET /models` → lista todos los modelos (JSON array).
2. `GET /models/<id>` → un modelo por id (404 si no existe).
3. `POST /models` → crea un modelo. Body JSON: `{"name","framework","accuracy"}`. Setea `created_at` en el server. Responde 201 con `{"id": <nuevo_id>}`.
4. `GET /health` → `{"status":"ok"}`.

## Datos de ejemplo (seed)
Al iniciar, si la tabla está vacía, insertar:
- `{"name":"resnet50","framework":"pytorch","accuracy":0.76}`
- `{"name":"xgb-churn","framework":"sklearn","accuracy":0.88}`

## Criterios de aceptación
- `GET /health` responde `{"status":"ok"}`.
- `GET /models` devuelve al menos los 2 seeds.
- `POST /models` con body válido crea y devuelve un id; un segundo `GET /models` lo incluye.
- `GET /models/<id>` inexistente devuelve 404.
- `POST /models` sin campos requeridos devuelve 400.
- El server corre en `http://127.0.0.1:5000`.

## Tu tarea (antes de automatizar)
Estimá cuánto tardarías en hacer TODO esto a mano (DB + server + 4 endpoints + seed + pruebas curl). Anotá el número en minutos. Después lo comparás.

## Pruebas con curl (definición de hecho)
```bash
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/models
curl -X POST http://127.0.0.1:5000/models -H "Content-Type: application/json" \
  -d '{"name":"bert-base","framework":"pytorch","accuracy":0.91}'
curl http://127.0.0.1:5000/models/1
```
