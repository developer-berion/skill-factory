<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_15_Entitlements_Billing_Enforcement.md

“Explica entitlements como sistema: modelos (plan→entitlements), enforcement points (API/UI/background jobs), auditoría, caching, upgrades/downgrades, trials, rate limits por plan, y cómo diseñar feature gating sin romper workflows. Incluye un ‘entitlement schema template’ en pseudo-JSON.”

Title
KB_15 – Entitlements \& Billing Enforcement en SaaS B2B

***

## Executive summary (10–15 líneas)

**Facts**

- Un sistema de entitlements es la capa que traduce “plan y contrato” en qué puede hacer realmente cada cuenta/usuario en el producto (features, límites, SLA).[^1][^2]
- La mejor práctica moderna es separar claramente billing (suscripción, facturas) de entitlements (acceso efectivo y límites), aunque estén sincronizados.[^2][^1]
- Entitlements se consultan en todos los enforcement points: API, UI y background jobs, idealmente desde un servicio central con baja latencia.[^3][^1]
- Los modelos típicos son: plan → entitlements (feature flags, límites cuantitativos, reglas de uso), con overrides por cuenta/tenant.[^4][^3]
- Trials, upgrades y downgrades se manejan cambiando el “bundle de entitlements” y las fechas de vigencia, sin tocar código de negocio.[^5][^4]
- Rate limits por plan (por API key/tenant) protegen infraestructura y son un componente estándar de los entitlements técnicos.[^6][^7][^8]
- La auditoría de cambios de entitlements y de decisiones de acceso es crítica para compliance, soporte y resolución de disputas.[^9][^5]

**Inferences**

- Para un CRM/Backoffice B2B (ej. mayorista turismo), los entitlements bien diseñados permiten jugar con pricing, márgenes y riesgo sin depender de desarrollo para cada ajuste.
- Feature gating debe orquestarse con feature flags de larga vida tipo “permission flags”, no con banderas temporales de rollout, para no romper workflows.[^10][^11]
- Caching agresivo de entitlements es clave en APIs de alto tráfico, pero siempre con estrategias claras de expiración e invalidación para evitar desalinearse del billing.
- Un buen “entitlement schema” estable reduce fricción entre producto, ventas y finanzas, y permite que el CRM “entienda” qué puede vender y entregar cada plan.
- Para mercados con fricción (ej. LATAM turismo), los entitlements son una herramienta para controlar riesgo (crédito, emisión, auto-ticketing) sin inventar 20 planes distintos.

***

## Definitions and why it matters

**Facts**

- Entitlements en SaaS = derechos efectivos de uso: qué features, límites de consumo, niveles de servicio y capacidades tiene un tenant según su suscripción y contrato.[^1][^5]
- Se diferencian de la autenticación (quién eres) y autorización RBAC clásica (qué rol tienes), aunque se complementan: primero plan/entitlement, luego rol/permiso.[^12][^3]
- La literatura moderna insiste en separar la vista “billing” (qué se factura) de la vista “entitlement” (qué se habilita), para manejar upgrades, cortes por impago y campañas sin romper el core de negocio.[^2][^1]
- Artículos recientes (Lago 2025, Mind the Product 2025) describen entitlements como un policy engine centralizado, capaz de procesar reglas complejas en tiempo real.[^9][^1]

**Inferences**

- Pensar en entitlements como “contrato ejecutable” entre tu empresa y la agencia: lo que se ve y se puede hacer en el sistema ES el contrato, sin ambigüedades.
- En un CRM enterprise/B2B, esta capa es el puente entre pricing/packaging (planes, descuentos, bundles) y el día a día operativo (qué puede hacer cada cuenta/agente).
- Sin un sistema explícito de entitlements, las reglas se dispersan en el código, en el CRM y en manuales operativos, volviendo imposible escalar pricing, campañas o restricciones por riesgo.

***

## Principles and best practices (con citas por sección + fecha)

**Facts**

- Principio 1 – Single source of truth: un servicio/tabla central de entitlements por tenant/usuario, consumido por API, UI y jobs; recomendado por proveedores modernos (Togai 2024, Lago 2025).[^4][^1]
- Principio 2 – Separación billing vs access: Kill Bill (2022) y otros proveedores recalcan mantener modelos separados pero sincronizados, para manejar mejor upgrades, suspensiones y promociones.[^2]
- Principio 3 – Entitlement granularity: combinar feature gates binarios, límites cuantitativos (cuotas, rate limits) y parámetros de configuración (ej. número de subcuentas).[^13][^1]
- Principio 4 – Engine central con baja latencia y auditoría: Mind the Product (2025) enfatiza motor central con tracking de consumo, self-service y trazabilidad de cambios.[^9]
- Principio 5 – Uso de feature flags como permission flags: guías actualizadas de feature flags (2024–2026) sugieren flags de larga vida ligadas a planes/roles para controlar acceso por tier.[^11][^14][^10]
- Principio 6 – Rate limiting per plan: documentación de API Management y guías de rate limiting (2025) recomiendan límites por organización/API-key y cuotas por intervalo (día/mes).[^7][^8][^6]

**Inferences**

- Diseñar entitlements primero a nivel de “tenant” (agencia, corporativo) y luego refinar a nivel de usuario/rol, reduce complejidad y encaja mejor con ventas B2B.
- La combinación ideal:
    - Servicio de entitlements (o módulo interno)
    - Configuraciones por plan en tablas/versionadas
    - Overrides por cliente clave
    - Y logs/auditoría legibles para soporte y finanzas.
- Para PMs, los entitlements son una palanca de monetización continua: facilitan crear add-ons, bundles temporales o pruebas limitadas sin proyectos de ingeniería largos.

***

## Examples (aplicado a CRM enterprise)

**Facts**

- En la práctica, muchos SaaS CRM agrupan funcionalidades en tiers (Free/Team/Enterprise) y asignan entitlements por tier: número de usuarios, módulos activos, límites de API, SSO, audit logs, etc.[^3][^4]
- Artículos sobre entitlements y feature flags muestran patrones donde el sistema primero verifica plan/tenant, luego rol/permiso, antes de permitir una acción específica en la UI o API.[^12][^13]

**Inferences (ejemplos adaptados a CRM/operador B2B)**

- CRM mayorista turismo – Ejemplo de entitlements por plan:
    - Plan Básico:
        - Módulos: cotizaciones online, emisión manual.
        - Límites: 2 usuarios, 200 cotizaciones/mes, sin API.
    - Plan Pro:
        - Módulos: auto-ticketing, grupos, integraciones GDS.
        - Límites: 20 usuarios, 5.000 cotizaciones/mes, 50 req/s por API key.
    - Plan Enterprise:
        - Módulos: crédito dinámico, overrides de markup por sub-agencia, auditoría avanzada.
        - Límites: usuarios ilimitados, 200 req/s, prioridad en colas de jobs.
- Ejemplo de feature gating sin romper workflow en CRM:
    - UI siempre muestra el botón “Emitir”, pero si el plan no tiene auto-ticketing:
        - Se abre un modal que explica: “Tu plan solo permite emisión manual. Solicita upgrade para auto-ticketing.”
        - Se registra intento fallido como señal de upsell.
- Ejemplo de job de background atado a entitlements:
    - Un job de “reconfirmación automática de reservas” solo procesa agencias con entitlement `auto_reconfirmation.enabled = true`.
    - Al hacer downgrade se respeta el período de gracia (ej. hasta fin de mes) con un campo `valid_until`, y luego el job deja de correr para ese tenant.

***

## Metrics / success signals

**Facts**

- La literatura sobre entitlements sugiere medir adopción de features por plan y su impacto en upsells y expansión de ingresos.[^4][^9]
- En guías de rate limiting se recomiendan métricas de uso por key/tenant y porcentaje de requests bloqueadas por límites como señal de dimensionamiento de planes.[^8][^6][^7]

**Inferences (métricas accionables para PM/RevOps)**

- Métricas clave de salud del sistema de entitlements:
    - % de decisiones de acceso resueltas desde caché vs desde origen.
    - Latencia P95 de check de entitlements en API crítica.
    - Número de incidentes donde entitlements estaban desalineados del billing (errores de acceso).
- Métricas comerciales vinculadas a entitlements:
    - Tasa de upgrade tras bloqueo suave (UI que invita a mejorar plan).
    - % de agencias que llegan al 80–100% de su cuota de uso (señal de potencial upsell).
    - Ingresos por add-ons habilitados via entitlements (ej. módulo de crédito dinámico).
- Métricas de control de riesgo:
    - Número de transacciones bloqueadas por límites de crédito/ cupos por plan.
    - Incidencias por sobreuso no facturado (gap de enforcement).

***

## Operational checklist

**Facts**

- Buenas prácticas modernas recomiendan gobernanza explícita de flags/entitlements: ownership, expiración cuando aplique, y auditoría de cambios.[^14][^10][^11]

**Inferences (checklist práctico)**

- Modelo de datos
    - Definido un schema de entitlements versionado (ver template más abajo).
    - Tablas/colecciones separadas para: plans, entitlements por plan, overrides por tenant, entitlements efectivos calculados.
- Enforcement points
    - API: middleware que resuelva tenant, plan y entitlements antes de entrar al handler de negocio.
    - UI: helpers centralizados (`canUse(feature)`, `getLimit(metric)`) usados en componentes y flujos.
    - Background jobs: lectura de entitlements antes de ejecutar lógicas caras (ej. envío masivo, reconfirmaciones).
- Auditoría y soporte
    - Logging de: cambios de plan, cambios manuales de entitlements, decisiones de acceso denegado (quién, qué, por qué).
    - Herramientas internas para que soporte pueda ver “qué plan/entitlements tiene hoy esta agencia y desde cuándo”.
- Caching
    - Estrategia definida de: TTL base (ej. 5–15 min), invalidación tras cambios de plan, y bypass para operaciones críticas (ej. suspensión inmediata por riesgo).
- Upgrades/downgrades/trials
    - Flujos claros de:
        - Upgrade inmediato (activar entitlements nuevos al instante, billing desde ahora o desde próximo ciclo).
        - Downgrade diferido (marcar cambio para próxima renovación pero mantener entitlements hasta esa fecha).
        - Trial con `trial_end_at` y toggling automático de entitlements.
- Rate limits por plan
    - Definidos por plan y por tipo de endpoint (ej. búsqueda vs emisión).
    - Configurados en gateway/API o middleware, leyendo desde entitlements.

***

## Anti-patterns

**Facts**

- Varias fuentes destacan riesgos de hardcodear clientes, planes y flags en código, y de usar el billing system directamente como sistema de autorización.[^15][^4][^2]

**Inferences**

- Anti-pattern 1 – Lógica de plan dispersa en el código
    - `if (customerId === 'ACME') { enableFeatureX(); }` o `if (plan === 'Enterprise') { ... }` repetido por toda la base de código.
- Anti-pattern 2 – Usar solo roles de usuario para controlar monetización
    - Mezclar permisos de seguridad (ej. “puede editar reservas”) con monetización (ej. “tiene auto-ticketing”) complica auditoría y pricing.
- Anti-pattern 3 – Feature flags temporales como sistema de pricing
    - Flags de rollout (“beta-feature”) usadas permanentemente para definir quién paga o no por un módulo, sin ligarlas a planes/entitlements.
- Anti-pattern 4 – Falta de downgrade seguro
    - Quitar entitlements de golpe sin periodo de gracia ni migración de datos; rompe workflows y genera tickets de soporte y churn.
- Anti-pattern 5 – Rate limiting global sin respetar plan
    - Un solo límite para todos los clientes genera injusticia: las cuentas grandes saturan el canal y las pequeñas sufren igual que las abusivas.

***

## Diagnostic questions

**Facts**

- Guías de gobernanza de entitlements/flags sugieren revisiones periódicas para detectar flags obsoletos, inconsistencias y huecos de monetización.[^10][^11][^14]

**Inferences (preguntas para tu sistema actual)**

- Modelo y datos
    - ¿Dónde vive hoy la verdad de “qué puede hacer esta agencia”? ¿En el CRM, en el core, en el gateway, en personas?
    - ¿Podrías listar, desde una sola tabla o servicio, todos los entitlements de un tenant con fechas de vigencia?
- Operación y riesgo
    - ¿Qué pasa cuando una factura no se paga? ¿El sistema sabe “bajar” entitlements de forma automática y trazable?
    - ¿Hay casos recientes de sobreuso no facturado o de bloqueos injustos por errores de plan?
- Producto y monetización
    - ¿Cuánto te cuesta (tiempo de ingeniería) lanzar un nuevo add-on o un cambio de bundle?
    - ¿Tienes métricas de cuántas veces los usuarios chocan con un límite y cuánto eso convierte a upsell?
- Técnica
    - ¿La API puede responder “403 – entitlement_missing” con un motivo concreto?
    - ¿Qué tan difícil sería mover tu lógica de entitlements a un servicio central si hoy está distribuida?

***

## Entitlement schema template (pseudo-JSON)

**Facts**

- La literatura sugiere representar entitlements como combinaciones de flags binarios, límites cuantitativos y parámetros configurables, normalmente asociados a tenants y planes.[^13][^1][^3]

**Inferences (plantilla genérica)**

```json
{
  "version": "v1",
  "tenant_id": "agency_123",
  "plan": {
    "code": "PRO",
    "display_name": "Pro B2B",
    "billing_period": "monthly",
    "billing_system_subscription_id": "sub_abc123",
    "starts_at": "2026-02-01T00:00:00Z",
    "renews_at": "2026-03-01T00:00:00Z",
    "status": "active" // active | past_due | cancelled | trialing
  },
  "trial": {
    "is_trial": true,
    "trial_ends_at": "2026-02-15T23:59:59Z",
    "post_trial_plan_code": "BASIC"
  },
  "entitlements": {
    "features": {
      "quotations": { "enabled": true },
      "auto_ticketing": { "enabled": true },
      "groups_module": { "enabled": true },
      "multi_branch": { "enabled": false },
      "white_label_portal": { "enabled": false }
    },
    "limits": {
      "users": {
        "max_active_users": 20
      },
      "quotations": {
        "max_per_month": 5000,
        "max_per_day": 500
      },
      "api": {
        "rate_limit_per_second": 50,
        "rate_limit_per_minute": 2000,
        "daily_quota": 100000
      },
      "credit": {
        "max_credit_exposure_usd": 10000,
        "max_booking_amount_per_pnr_usd": 3000
      }
    },
    "behavior_flags": {
      "require_manual_approval_over_credit_limit": true,
      "allow_partial_payment": false,
      "priority_in_background_jobs": "high" // low | normal | high
    }
  },
  "overrides": {
    "features": {
      "white_label_portal": { "enabled": true, "reason": "contract_override" }
    },
    "limits": {
      "api": {
        "rate_limit_per_second": 100,
        "source": "sales_special_deal"
      }
    }
  },
  "audit": {
    "last_synced_from_billing_at": "2026-02-01T00:05:00Z",
    "last_updated_by": "user_999",
    "last_update_reason": "upgrade_from_BASIC",
    "history_ref_id": "ent_hist_456"
  }
}
```


***

## Cómo diseñar enforcement y feature gating sin romper workflows

**Facts**

- Fuentes sobre entitlements + feature flags describen un patrón de tres pasos: chequear flag global, luego entitlement de tenant, luego permisos del usuario.[^12][^13][^3]
- Guías de feature flags recientes recomiendan usar “permission flags” de larga vida para controlar accesos por plan/tier, y no mezclar con flags de rollout temporal.[^11][^10]

**Inferences (diseño práctico)**

- Puntos de enforcement
    - API: middleware `checkEntitlement(tenant_id, feature, usage_context)` que pueda devolver: ALLOW, DENY, ALLOW_WITH_WARNING (para casi-límite), con razón.
    - UI: helpers como `canUse('auto_ticketing')` y `remainingQuota('quotations')` para mostrar/ocultar botones y mensajes de upgrade, sin duplicar lógica.
    - Background jobs: filtros que solo procesen registros de tenants con entitlements activos y cuota disponible (ej. no mandar recordatorios a quien está suspendido).
- Sin romper workflows
    - Usar “bloqueo suave” primero: permitir ver la función pero no ejecutar, con mensajes claros y CTA a upgrade, en lugar de esconder todo.
    - Para downgrades, implementar períodos de gracia y modos “solo lectura” (ej. seguir viendo reportes, pero no crear nuevas reservas/acciones).
    - En entornos de alto riesgo (crédito), separar “bloqueo por riesgo” de “bloqueo por plan” para poder explicar bien el motivo al cliente.

***

## Caching, upgrades/downgrades, trials y rate limits por plan

**Facts**

- Entitlement engines modernos requieren respuestas sub-segundo y suelen usar caching estratégico para decisiones de acceso, mientras monitorean consumo en tiempo real para billing.[^1]
- Documentación de plataformas de API y SaaS describe rate limits configurables por organización/API clave, con cuotas por periodo y diferentes niveles por plan.[^6][^7][^8]

**Inferences**

- Caching
    - Cache por `tenant_id` + `version` de entitlements; invalidar al cambiar de plan o vencer el trial.
    - Para decisiones muy críticas (ej. suspensión por fraude/riesgo), permitir bypass al origen, aunque sea más lento.
- Upgrades
    - Opción segura: upgrade inmediato de entitlements, billing prorrateado o desde próximo ciclo; siempre log de qué cambió y cuándo.
    - Opción agresiva: permitir “overage controlado” (pasarse de límite con recargo) configurado como entitlement adicional.
- Downgrades
    - Opción segura: marcar downgrade efectivo al final del período, mostrar banner en UI y preparar migración de datos (ej. reducir usuarios activos).
    - Opción agresiva: recorte inmediato de límites pero con “exportación” o acceso temporal a lectura para minimizar impacto.
- Trials
    - Definir entitlements específicos de trial (a veces más altos para mostrar valor), con `trial_ends_at` y transición automática a un plan pagado más limitado si no hay conversión.
    - Opcionalmente, mantener algunos entitlements “sticky” (ej. configuración ya creada) para no castigar al usuario que probó intensamente.
- Rate limits por plan
    - Separar tipos de tráfico: lectura, escritura crítica (emisión), background/bulk.
    - En travel B2B, cuidar especialmente:
        - Límites más estrictos para operaciones que disparan costos (emisión, bloqueos de cupos).
        - Límites más suaves para búsqueda/cotización, pero con protección anti-scraping.

***

## Sources (o referencia a SOURCES.md)

**Facts**

- Existen múltiples artículos recientes y documentación técnica que cubren entitlements, feature flags y rate limiting en SaaS B2B.[^15][^7][^5][^8][^14][^10][^6][^3][^11][^4][^1][^9][^2]

**Inferences (entradas sugeridas para SOURCES.md, sin duplicados)**

- Togai – “Unleashing SaaS Entitlement: A Complete Guide” (2024-12-12).[^4]
- Lago – “How do entitlements work in SaaS?” (2025-08-31).[^1]
- Mind the Product – “How entitlement management supports the move to SaaS” (2025-09-03).[^9]
- Stigg / Dev.to – “Entitlements untangled: The modern way to software monetization” (2023-06-17).[^13]
- AWS + LaunchDarkly – “Simple and Flexible SaaS Entitlement Management with LaunchDarkly” (2023-07-10).[^3]
- Broadcom Techdocs – “Manage Rate Limits and Quotas” (última versión consultada 2025).[^6]
- SaasRock – “API Rate Limiting | SaasRock Documentation” (fecha según doc).[^7]
- Zuplo – “10 Best Practices for API Rate Limiting in 2025” (2025-01-05).[^8]
- DesignRevision – “Feature Flags Best Practices: Complete Guide (2026)” (2026-02-07).[^10]
- Octopus Deploy – “The 12 Commandments of Feature Flags in 2025” (2025-11-12).[^15]
- Eppo – “10 Feature Flag Best Practices You Should be Using in 2024” (2024-06-20).[^11]
- Harness – “Best practices for managing flags” (2025-11-09).[^14]
- Nalpeiron – “How to Manage Entitlements in SaaS Product Dev Cycles” (2024-12-31).[^5]
- Kill Bill – “Two Aspects of SaaS Entitlement Management: Access and Billing” (2022-07-21).[^2]

***

## Key takeaways for PM practice

- Diseñar entitlements como “contrato ejecutable” separando claramente billing, entitlements y permisos simplifica pricing, soporte y compliance.
- Centralizar el motor de entitlements (con schema estable + overrides) es condición para escalar planes, add-ons y acuerdos especiales con agencias.
- Usar feature flags de tipo “permission” vinculados a planes/entitlements evita que el sistema de flags temporales se convierta en tu sistema de monetización por accidente.
- Definir enforcement coherente en API, UI y jobs es tan importante como el modelo de datos: sin enforcement homogéneo, los gaps de control y monetización son inevitables.
- La auditoría (qué cambió, quién lo cambió, desde cuándo) no es lujo: es pieza básica para resolver disputas comerciales y problemas de riesgo.
- Métricas de uso vs límites (near-limit, bloqueos, upgrades) son señales directas para roadmap de producto y tácticas de upsell.
- Para mercados con alta fricción y riesgo, los entitlements se vuelven una herramienta táctica de control de crédito y exposición, no solo un tema técnico.
- Empezar pequeño (schema claro, middleware sencillo, logging) y endurecer después (caching avanzado, overage, política de downgrades) es una estrategia más segura que intentar diseñar “el sistema perfecto” desde el día uno.
<span style="display:none">[^16]</span>

<div align="center">⁂</div>

[^1]: https://getlago.com/blog/saas-entitlements

[^2]: https://blog.killbill.io/blog/two-aspects-of-saas-entitlement-management-access-and-billing/

[^3]: https://aws.amazon.com/blogs/apn/simple-and-flexible-saas-entitlement-management-with-launchdarkly/

[^4]: https://www.togai.com/blog/software-entitlement-definition/

[^5]: https://nalpeiron.com/blog/manage-entitlements-saas-product-dev-cycle

[^6]: https://techdocs.broadcom.com/us/en/ca-enterprise-software/layer7-api-management/api-developer-portal/saas/manage/manage-plans/manage-account-plans.html

[^7]: https://saasrock.com/docs/articles/api-rate-limiting

[^8]: https://zuplo.com/learning-center/10-best-practices-for-api-rate-limiting-in-2025

[^9]: https://www.mindtheproduct.com/how-entitlement-management-supports-the-move-to-saas/

[^10]: https://designrevision.com/blog/feature-flags-best-practices

[^11]: https://www.geteppo.com/blog/feature-flag-best-practices

[^12]: https://www.stigg.io/blog-posts/entitlements-untangled-the-modern-way-to-software-monetization

[^13]: https://dev.to/getstigg/entitlements-untangled-the-modern-way-to-software-monetization-2pi0

[^14]: https://developer.harness.io/docs/feature-flags/get-started/feature-flag-best-practices/

[^15]: https://octopus.com/devops/feature-flags/feature-flag-best-practices/

[^16]: pasted-text.txt

