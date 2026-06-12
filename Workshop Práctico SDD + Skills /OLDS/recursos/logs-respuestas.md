# Clave de respuestas — análisis de logs (Bloque 5) · SOLO FACILITADOR

Los 3 archivos de `recursos/logs/` (gateway / services / infra, ~3900 líneas,
ventana 05:00–11:00) esconden **4 historias** que requieren correlación
**entre archivos**. Ninguna causa raíz aparece como ERROR: `grep ERROR` da 37
red herrings de image-resize, síntomas (504/502) y nada más.

## Historia A — El cron asesino (actualiza el issue de payments-api)
- **Causa raíz:** `infra.log` → `[INFO] cron job analytics-rollup started host=db-01
  (full table scan...)` cada hora en punto (05:00–10:00), corre ~8 min.
- **Cadena:** durante cada ventana :00–:08 → `infra.log` muestra `db-01 io_util=9x%`
  (INFO) → `services.log` muestra `payments-api db acquire=300-1300ms` (WARN) →
  `gateway.log` muestra latencia x5 y **9× 504** en /checkout, /payments, /orders.
- **Lo que debe hacer la skill:** actualizar el issue existente *"Timeouts
  intermitentes contra la DB" (payments-api)* con la causa raíz (el rollup) y
  proponer: mover el cron fuera de hora pico / throttlear / réplica de lectura.
- **Por qué regex no alcanza:** el patrón es *periodicidad horaria + lag de 2-4
  minutos entre tres archivos*; la línea culpable es INFO e inocente.

## Historia B — Leak post-deploy (actualiza el issue de 502 en /checkout)
- **Causa raíz:** `infra.log` 07:14 → `[INFO] deployer checkout-service v2.8.0
  rollout complete ... changelog: connection handling refactor`.
- **Cadena:** `services.log` → `checkout-service pool stats active=N` crece
  gradualmente: ~7-12 antes del deploy → ~21-24 a las 08:30 → 47-50 a las 10:50
  (**tendencia numérica dentro de líneas INFO**) → recién a las 10:41 aparecen
  los primeros `status=502 connect_econnrefused` en gateway y `cannot acquire
  connection` en checkout.
- **Lo que debe hacer la skill:** actualizar *"502 intermitentes en /checkout"*
  con la correlación deploy↔tendencia del pool y proponer rollback de v2.8.0 o
  fix del leak.
- **Por qué regex no alcanza:** hay que *derivar una tendencia* de números en
  INFOs y unirla a un evento de deploy 3 horas anterior en otro archivo.

## Historia C — Clock skew → JWT (crea un issue NUEVO)
- **Causa raíz:** `infra.log` 08:42 → `[WARN] ntp step correction -2.4s applied
  node=worker-2` (con drift detectado 4 min antes).
- **Cadena:** 08:42–08:53 → `services.log` muestra `auth-service token validation
  failed: token used before issued (iat=...)` en worker-2 → `gateway.log`
  muestra **17× status=401** SOLO en esa ventana; después desaparece.
- **Lo que debe hacer la skill:** crear issue nuevo (p. ej. "Skew de reloj en
  worker-2 invalida JWTs", high) con solución: monitoreo NTP / slew en vez de
  step / tolerancia de iat.
- **Por qué regex no alcanza:** tres vocabularios sin strings compartidos
  (ntp step / iat / 401) y ventana de 11 minutos.

## Historia D — Disco + backups (actualiza el issue de backups, la "fácil")
- `infra.log`: `disk usage 84%→97%` (INFO, lento) + `backup nightly-backup
  failed: No space left on device` (05:02 y 06:02).
- Actualiza *"Backups nocturnos fallan esporádicamente" (db-01)* con la causa
  (disco) — está para que el grupo entre en calor.

## Red herrings que la skill debe DESCARTAR explícitamente
- `catalog-service image-resize timeout` (37 ERRORs) — **siempre** seguido de
  retry exitoso; el propio log dice `known-flaky upstream`.
- `logging-pipeline dropping N events` — marcado `known issue LOG-441` (ya hay
  issue seedeado de logging-pipeline; sumar evidencia está OK, escalarlo no).
- Rebalanceos de Kafka, `s3 PUT retry`, `memory pressure worker-3`: ruido normal.

## Señales de éxito en la demo
1. NO duplica los issues de payments/checkout/backups: los **actualiza**.
2. Crea el del clock skew (es el único genuinamente nuevo).
3. Menciona las correlaciones temporales con números (frecuencia, ventanas).
4. Descarta image-resize y compañía con justificación.
5. Si alguien del grupo dice "esto lo hacía con grep", invitalo a encontrar la
   Historia B sin leer los 3 archivos enteros. 😉
