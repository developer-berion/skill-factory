<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_08_Forms_Data_Quality_Governance.md

“Cómo diseñar forms y validaciones para mejorar calidad de datos sin frenar productividad. Incluye data hygiene UX, dedupe flows, progressive profiling, permisos por campo, audit trails desde UX.”

Diseña tus forms como “captura mínima útil + validación en el momento correcto + dedupe asistido”, para subir calidad sin subir fricción. El truco es que el usuario avance aunque el dato no sea perfecto, pero que el sistema lo normalice, lo valide y lo haga auditable.

## Qué incluye / no incluye / sensible

- Incluye: patrones de UX para data hygiene, validaciones (cliente/servidor), flujos de deduplicación/merge, progressive profiling, permisos por campo y audit trails visibles desde UX.
- No incluye: implementación específica en un CRM (Salesforce/HubSpot/Dynamics) ni reglas legales por país.
- Sensible: PII (documentos, teléfono, email), datos de pago (mejor no almacenar PAN/CVV en CRM aunque “lo enmascares”), y cualquier campo que afecte precio/comisiones/crédito (debe auditarse).[^1]


## Data hygiene UX (sin frenar)

- Pide menos al inicio: si el form tiene demasiados campos temprano, aumenta la probabilidad de datos falsos/“de relleno” y por tanto data sucia.[^2]
- Prefiere restricciones que ayuden: dropdowns vs texto libre, máscaras de teléfono, autocompletar, defaults inteligentes, y normalización silenciosa (trim, case, quitar símbolos en teléfono) para reducir variación.
- Valida “justo a tiempo”: la validación inline cerca del campo reduce costo de corrección porque el usuario arregla el error sin buscar dónde falló.[^3]
- Evita el “error rojo mientras tipea” sin umbral: validación en tiempo real demasiado temprana genera flashes de errores prematuros y fricción; usa umbrales (p.ej., validar email tras perder foco o tras N caracteres).[^4]
- Para validaciones complejas, considera validar al enviar: hay evidencia de menos errores cuando los mensajes aparecen después de presionar submit (modo “revisión” del usuario).[^5]


## Dedupe flows (prevención + resolución)

- Prevención al capturar: antes de crear un registro, busca posibles duplicados por claves “fuertes” (email, teléfono normalizado) y muestra coincidencias. Si el riesgo es alto, no bloquees; manda a “cola de revisión” (operaciones) en vez de rebotar al vendedor.
- “Dos carriles” recomendado: auto-merge solo cuando la coincidencia sea muy alta y el resto a revisión; un esquema típico es auto-merge ≥95%, revisión 80–94%, ignorar <80% (ajustable por tolerancia al riesgo).[^6]
- UX de merge: cuando se detecta dupe, abre una pantalla de comparación campo-a-campo y deja elegir qué valor “se queda” (columna “keep”).[^7]
- Reglas de supervivencia (merge rules): define por campo si gana “más reciente”, “más completo”, “más confiable”, etc.; en dedupe por workflows se suele soportar escoger por fecha de última modificación para conservar el dato más nuevo en campos como nombre/teléfono.[^8]
- No rompas trazabilidad: al merge, protege ownership, relaciones (negocios, reservas) y auditabilidad; si automatizas merges, exige preview/log y capacidad de revertir en casos críticos.


## Progressive profiling (calidad por etapas)

- Empieza pequeño y progresa: pedir datos básicos primero y luego completar el perfil en interacciones posteriores reduce fatiga; buena práctica es “start small”.[^9]
- Sé contextual: pregunta lo siguiente solo cuando tenga sentido por el flujo/uso (p.ej., cuando la agencia pide crédito, ahí sí pides docs fiscales).[^9]
- Limita preguntas por “momento”: 1–2 preguntas adicionales por interacción suele ser el sweet spot para no cortar conversión.[^9]
- Permite omitir lo opcional y explica el intercambio de valor: “para qué” y “qué gana” el usuario, con opción de skip cuando no es obligatorio.[^10]


## Permisos por campo + audit trails desde UX

- Permisos por campo (field-level): define perfiles (Ventas, Operaciones, Finanzas) donde campos sensibles sean “solo lectura” o invisibles para algunos roles, y habilita auditoría en esos campos protegidos para saber quién cambió qué y cuándo.[^1]
- No guardes datos de tarjeta en CRM “por comodidad”: incluso con seguridad por campo, no se recomienda almacenar números de tarjeta por requisitos PCI (usa PSP/tokenización).[^1]
- Audit trail operativo: registra cambios de alto riesgo (permisos, exportaciones, etc.) y revísalos periódicamente; los sistemas de audit trail suelen capturar cambios de seguridad/acceso y acciones administrativas de riesgo.[^11]
- “Audit trail desde UX”: en campos críticos muestra “Última edición: usuario/fecha” y un link a “ver historial”, y para cambios sensibles pide motivo (dropdown) + comentario; eso baja disputas internas y acelera soporte.

Si me dices en qué módulo lo estás aplicando (alta de agencias, solicitudes de reserva, pagos/crédito, o carga de pasajeros), te lo aterrizo a un blueprint con: campos mínimos por etapa, reglas de validación, llaves de dedupe y matriz de permisos por rol.
<span style="display:none">[^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29]</span>

<div align="center">⁂</div>

[^1]: https://www.encorebusiness.com/blog/field-level-security-in-microsoft-dynamics-365-crm/

[^2]: https://www.forbes.com/sites/falonfatemi/2019/01/30/best-practices-for-data-hygiene/

[^3]: https://www.nngroup.com/articles/errors-forms-design-guidelines/

[^4]: https://www.smashingmagazine.com/2022/09/inline-validation-web-forms-ux/

[^5]: https://uxmovement.com/forms/why-users-make-more-errors-with-instant-inline-validation/

[^6]: https://databar.ai/blog/article/crm-deduplication-complete-guide-to-finding-merging-duplicate-records

[^7]: https://help.element451.com/en/articles/9472960-merging-duplicate-records

[^8]: https://experienceleague.adobe.com/en/docs/campaign/automation/workflows/use-cases/data-management/deduplication-merge

[^9]: https://support.blueconic.com/en/articles/248006-build-unified-profiles-with-progressive-profiling-use-case

[^10]: https://www.avatier.com/blog/progressive-profiling-building/

[^11]: https://gearset.com/blog/salesforce-audit-trail/

[^12]: https://usask.ca-central.catalog.canvaslms.com/certificates/data-governance-training-1604.pdf

[^13]: https://formulayt.com/guides/ultimate-guide-progressive-profiling

[^14]: https://www.descope.com/learn/post/progressive-profiling

[^15]: https://emarsys.com/learn/blog/5-progressive-profiling-best-practices-for-driving-customer-loyalty/

[^16]: https://appfrontier.com/blog/audit-trail-field-history-tracking

[^17]: https://smart-interface-design-patterns.com/articles/inline-validation-ux/

[^18]: https://www.pingidentity.com/en/resources/blog/post/what-is-progressive-profiling.html

[^19]: https://nation.marketo.com/t5/product-discussions/progressive-profiling-what-should-we-consider-before/td-p/51458

[^20]: https://community.dynamics.com/forums/thread/details/?threadid=301497f7-44f3-4b73-a6f4-24a4783ce4ea

[^21]: https://www.plauti.com/platform/salesforce/deduplicate

[^22]: https://blog.insycle.com/data-retention-merging-duplicates

[^23]: https://www.salesgenie.com/blog/top-data-hygiene-best-practices/

[^24]: https://dedupe.ly/blog/matching-and-merging-salesforce-duplicates-with-dedupely

[^25]: https://knowledge.hubspot.com/records/deduplication-of-records

[^26]: https://www.xappex.com/blog/salesforce-duplicate-management/

[^27]: https://www.humanitru.com/14-data-hygiene-tips-for-nonprofits/

[^28]: https://help.zoho.com/portal/en/community/topic/tip-8-merge-duplicate-records

[^29]: https://appexchange.salesforce.com/partners/servlet/servlet.FileDownload?file=00P4V000011djAeUAI

