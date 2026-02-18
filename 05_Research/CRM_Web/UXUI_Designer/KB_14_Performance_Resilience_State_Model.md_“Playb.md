<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_14_Performance_Resilience_State_Model.md

“Playbook de estados: loading/error/empty/skeleton, retries, optimistic UI, conflictos, y fallos de red (web CRM). Incluye checklist QA.”

```md
# KB_14_Performance_Resilience_State_Model
Playbook de estados y resiliencia para un CRM web (B2B): loading/error/empty/skeleton, retries, optimistic UI, conflictos y fallos de red. Incluye checklist QA.

## 1) Alcance (qué sí / qué no / sensible)
**Incluye**: modelo de estados UI por vista (listado, detalle, formularios, dashboards), políticas de reintento, patrones de “optimistic UI”, manejo de conflictos (versionado), y degradación por fallos de red (timeouts, offline parcial, rate limit).  
**No incluye**: observabilidad backend profunda (tracing), diseño visual detallado, ni arquitectura de microservicios; esto es un playbook front + contrato API mínimo para operar bien en fricción LATAM.  
**Sensible** (define antes de construir): reglas de idempotencia (POST/PUT), “source of truth” por campo (quién gana en conflictos), y límites de riesgo (acciones que NO pueden ser optimistas sin confirmación, ej. emitir factura, liberar cupo, anular reserva).

## 2) Modelo de estados UI (por pantalla)
Regla base: cada “screen” debe poder estar en 1 estado principal + 0..n “sub-estados” por componente (tabla, panel, botón) para evitar pantallas congeladas.  
Separa “estado de datos” (no hay datos / hay datos) de “estado de red” (cargando / falló / reintentando) para no mezclar empty con error.

### Estados estándar
| Estado | Cuándo aplica | UI requerida | Qué NO hacer |
|---|---|---|---|
| `skeleton` | Primera carga o cambio fuerte de vista | Placeholder de estructura (tabla/cards) para anticipar layout; reduce carga cognitiva vs spinner genérico [web:12] | Mostrar datos viejos como si fueran nuevos sin indicar “stale” |
| `loading` | Acción puntual (guardar, filtrar, paginar) | Bloqueo parcial (solo el área afectada), spinner inline, texto “Guardando…” | Bloquear toda la app por acciones locales |
| `success` | Datos listos | Contenido + estado “fresh/stale” si aplica | Ocultar latencia: siempre muestra feedback de acción |
| `empty` | Respuesta válida sin registros | Mensaje claro + CTA (“Crear”, “Quitar filtros”, “Importar”) | Usar empty como fallback cuando hubo error |
| `error` | Fallo definitivo o sin reintentos | Mensaje accionable + “Reintentar” + “Ver detalle” (código/trace id) | Mensajes genéricos tipo “Algo salió mal” sin opciones |
| `retrying` | Fallo recuperable | Contador + backoff visible si afecta flujo | Reintentar infinito sin límite ni salida |

### Transiciones (mini state machine)
- `skeleton -> success` (200 OK con datos)  
- `skeleton -> empty` (200 OK sin datos)  
- `skeleton/loading -> retrying -> success/empty` (timeouts, 502/503/504)  
- `loading -> error` (4xx validación/permiso, o agotó reintentos)  
- `success -> loading` (refetch por filtro, cambio de pestaña, refresh)  
- `success -> stale` (cuando cae red: muestra datos cacheados con banner “Sin conexión / datos pueden estar desactualizados”)

## 3) Retries, timeouts y rate limit (contrato mínimo)
Define “qué se reintenta” y “qué no” por tipo de error, no por intuición.

### Política recomendada (cliente web)
- **Timeouts**: por request define `connect + read` (ej. 10–30s según operación); si expira, pasa a `retrying` si es idempotente.
- **Reintentos** (solo para idempotentes o con idempotency-key):
  - Reintenta en 408/429/500/502/503/504 si el método es seguro (GET) o si tu API soporta idempotencia para escrituras.
  - Usa **exponential backoff con jitter** para evitar “retry storms” (muchos clientes reintentando sincronizados) [web:7].
- **Rate limit (429)**: si viene `Retry-After`, respétalo como tiempo de espera antes del próximo intento [web:2].
- **Service unavailable (503)**: `Retry-After` puede indicar cuánto esperar porque el servicio no estará disponible temporalmente [web:2][web:1].

### Reglas prácticas (B2B CRM)
- GET de listados: reintenta (con backoff) y permite “Ver últimos datos” si hay cache.
- POST “crear”: solo optimistic si tienes `idempotency-key` y puedes detectar duplicados; si no, usa confirmación explícita.
- PUT/PATCH “editar”: optimistic con rollback si hay conflicto/permiso, pero siempre conserva el input del usuario en memoria local hasta confirmación.
- DELETE: evita optimistic agresivo en objetos críticos; usa “soft delete UI” (marcar como eliminado) hasta confirmación.

## 4) Optimistic UI, conflictos y consistencia
Optimistic UI sirve para velocidad percibida, pero en B2B debes controlar el riesgo: no todo puede “parecer hecho” si tiene impacto financiero u operativo.

### Patrón base (optimistic seguro)
- Al hacer una acción, crea una “pending mutation” con `mutationId`, `timestamp`, payload y snapshot previo (para rollback).
- Refleja UI inmediato (optimistic), pero etiqueta el ítem como “Pendiente de confirmación”.
- Cuando llega respuesta:
  - `success`: reemplaza por “server state” (lo que diga el backend).
  - `error`: rollback + toast con causa + CTA (“Reintentar”, “Copiar detalles”, “Contactar soporte”).

### Manejo de conflictos (multiusuario / multi-dispositivo)
- Recomendación de contrato API: ETag/If-Match o un `version` incremental por registro; si el servidor detecta edición concurrente, responde 409 Conflict.
- UI ante 409:
  - Opción **segura**: modal de resolución (Tu cambio vs Cambio remoto), permite “Aplicar encima” solo si el rol lo permite.
  - Opción agresiva: “Last write wins” solo para campos no críticos (notas internas, tags), nunca para montos/fechas de emisión/estado de pago.
- “Draft local”: en formularios largos, persiste borrador local (localStorage/IndexedDB) para evitar pérdida por refresh o caída de red.

## 5) Checklist QA (resiliencia + estados)
### Estados por vista
- Skeleton aparece solo cuando corresponde (primera carga o cambio fuerte), no en micro-acciones. [web:12]
- Empty se muestra únicamente cuando la respuesta fue válida y sin registros (no por error).
- Error incluye acción concreta (Reintentar / Cambiar filtros / Volver) y un identificador de diagnóstico (requestId).

### Red / fallos simulados
- Simular offline: la app muestra banner de desconexión, deshabilita acciones no soportadas offline y conserva input del usuario.
- Simular latency alta (3G/Slow): no hay “layout shift” fuerte; skeleton mantiene estructura.
- Simular 429: el cliente respeta `Retry-After` y no martilla el backend. [web:2]
- Simular 503: si viene `Retry-After`, espera lo indicado; si no viene, aplica backoff con jitter y límite de intentos. [web:2][web:7]

### Retries y límites
- Máximo de reintentos por request definido (ej. 3–5) y luego cae en error con opción manual.
- Backoff tiene jitter (verifica que no sea delay fijo); evita picos de reintento simultáneo. [web:7]
- Requests de escritura sin idempotencia NO se reintentan automáticamente (solo manual, con confirmación).

### Optimistic UI / consistencia
- Cada optimistic deja evidencia “pendiente” y permite rollback sin perder datos.
- Conflicto 409: la UI ofrece resolución clara y no sobrescribe silenciosamente datos críticos.
- Duplicados: si el usuario hace doble click o refresh, no genera doble creación (idempotency-key o bloqueo UI).

### Observabilidad mínima (para soporte B2B)
- Cada error visible al usuario incluye: endpoint lógico, timestamp, requestId (si existe), y “copiar detalles”.
- Eventos de analítica: `state_entered` (loading/skeleton/error/empty), `retry_started`, `retry_exhausted`, `optimistic_applied`, `conflict_detected`.

---
Notas de implementación: si necesitas, lo aterrizo a tu stack (React/Next, Vue, etc.) con un ejemplo de “state slice” + middleware de retries + cola de mutaciones.
```

<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^2][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.rfc-editor.org/rfc/rfc9110.html

[^2]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Retry-After

[^3]: https://stackoverflow.com/questions/3764075/retry-after-http-response-header-does-it-affect-anything

[^4]: https://github.com/curl/curl/issues/11447

[^5]: https://community.atlassian.com/forums/Jira-questions/I-m-not-able-to-get-retry-after-header-on-getting-429/qaq-p/1656672

[^6]: https://clickhelp.com/clickhelp-technical-writing-blog/skeleton-illustrations-to-improve-ux-in-technical-documentation/

[^7]: https://www.presidio.com/technical-blog/exponential-backoff-with-jitter-a-powerful-tool-for-resilient-systems/

[^8]: https://kolmafia.us/threads/request-discuss-retry-after-header-in-generic-request.29637/

[^9]: https://www.educative.io/answers/how-to-use-material-uis-skeleton-component

[^10]: https://www.baeldung.com/resilience4j-backoff-jitter

[^11]: https://workos.com/blog/http-error-codes

[^12]: https://mui.com/material-ui/react-skeleton/

[^13]: https://oneuptime.com/blog/post/2026-01-25-retry-exponential-backoff-spring/view

[^14]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status

[^15]: https://m3.material.io/styles/motion/transitions

