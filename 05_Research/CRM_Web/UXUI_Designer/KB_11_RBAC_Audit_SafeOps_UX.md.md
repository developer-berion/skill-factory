<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_11_RBAC_Audit_SafeOps_UX.md

Aquí tienes patrones UX accionables para CRM enterprise que combinan RBAC, seguridad por campo, acciones sensibles, “diff before apply”, audit log visible y “undo” donde aplique. Incluyo ejemplos aplicados, microcopy sugerido y puntos “incluye / no incluye / sensible”.

## Principios base (para alinear UX + seguridad)

RBAC se apoya en que los usuarios se asignan a uno o más roles y los roles agrupan privilegios (permisos) que se otorgan a quienes tienen ese rol.[^1]
El estándar ANSI/INCITS 359-2004 (modelo de referencia RBAC) formaliza elementos como usuarios, roles, permisos y sesiones, y cómo se relacionan (por ejemplo, roles activos por sesión).[^2]

- Incluye: “explicar” permisos en lenguaje de negocio (qué puede hacer/ver), y hacerlo observable en UI (por qué veo/no veo algo).
- No incluye: delegar a usuarios la responsabilidad de “adivinar” por qué una acción falla.
- Sensible: consistencia; si el sistema es aditivo (permisos efectivos = suma), UI debe evitar falsas expectativas de “deny” implícito.[^3]

Ejemplo (CRM B2B): “Rol: Ventas Agencia” puede “Crear cotización”, pero no “Aprobar descuento > 8%” ni “Editar condiciones de pago”.

## RBAC + Field-level security (FLS)

Cuando el control es granular, el acceso efectivo tiende a ser **aditivo** (la suma de asignaciones puede anular restricciones más finas), así que el diseño debe mostrar “de dónde viene” el permiso.[^3]
En entornos con privacidad y cumplimiento, la motivación típica de granularidad es proteger datos sensibles (PII/financiero) y cumplir regulaciones, por lo que ocultar o enmascarar campos debe ser una decisión explícita y auditable.[^3]

Patrones UX recomendados (aplicables a CRM):

- Estado de permiso “en línea”
    - En botones/acciones: “Deshabilitado + motivo” en tooltip o texto secundario.
    - Microcopy: `No puedes aprobar descuentos. Requiere rol: Finance Approver.`
- FLS con 3 niveles claros por campo (no solo “visible/no visible”)
    - Ver (read), editar (write), ver-mascarado (masked).
    - Ejemplo campo: “Tarifa neta”, “Markup”, “Límite de crédito”, “Documento fiscal”.
- “Permission peek” para admins (sin abrir consola)
    - Link contextual: `Ver permisos efectivos` (abre drawer con: roles activos, políticas/condiciones relevantes y alcance).
- “Scope chips” (alcance) para datos multi-tenant / multi-sucursal
    - Chips tipo: `Sucursal: Bogotá`, `País: CO`, `Marca: X`, y si aplica condiciones.

Incluye / No incluye / Sensible:

- Incluye: explicar permisos efectivos y evitar sorpresas por sumatoria de roles.[^3]
- No incluye: mensajes genéricos “Forbidden/403” sin contexto de rol/alcance.
- Sensible: no filtrar por UI solamente; si el usuario no debe ver un campo, el backend tampoco debe retornarlo (UI es la última capa).

Ejemplo aplicado (ficha de Deal): el campo “Costo proveedor” aparece como `•••••` con badge `Restringido`, y al hover: `Visible solo para roles Finance/Ops`.

## Acciones sensibles: confirmación + “diff before apply”

Los diálogos son interruptivos y deberían usarse con moderación; si todo es modal, el usuario se habitúa y deja de leer.[^4]
En acciones destructivas o de consecuencias serias, una confirmación debe restatar la acción y explicar el impacto, y debería evitar respuestas por defecto para forzar la verificación consciente.[^5]

### 1) Clasifica acciones por riesgo (y aplica fricción proporcional)

- Nivel 0 (reversible, baja consecuencia): toggle, etiquetas, mover etapa del pipeline.
- Nivel 1 (reversible con impacto): desasignar owner, archivar registro.
- Nivel 2 (difícil de revertir): eliminar, cambiar moneda/condición de pago, cambiar política comercial aplicada.
- Nivel 3 (irreversible o regulatorio): borrar PII, revocar acceso, cambiar permisos/roles, modificar límites de crédito.

Patrones de fricción por nivel:

- Nivel 0–1: feedback no bloqueante + “undo” (siempre que sea realmente reversible).[^6]
- Nivel 2: modal de confirmación bien redactado + resumen de impacto.[^5]
- Nivel 3: confirmación reforzada (p.ej. “escribe DELETE”, 2FA/step-up, doble aprobación), y logging reforzado.[^7]


### 2) “Diff before apply” (previsualiza el cambio real)

Objetivo: que la agencia/usuario vea “qué va a cambiar” antes de ejecutar una acción sensible, especialmente en edición masiva, cambios de políticas, o aprobación de excepciones.

UI pattern (drawer o modal):

- Encabezado: `Revisar cambios (3)`
- Bloque “Antes / Después” por campo
- Destaca cambios sensibles (monto, moneda, descuento, condiciones)
- CTA principal explícito: `Aplicar cambios` (no “Sí/OK”)[^5]

Ejemplo aplicado (aprobación de descuento):

```text
Revisar cambios
- Descuento: 5%  →  12%
- Margen estimado: 9%  →  2%
- Requiere aprobación: Finance Approver (por >8%)
Impacto: el margen cae por debajo del mínimo permitido.
[Cancelar] [Solicitar aprobación] [Aplicar cambios]
```

Incluye / No incluye / Sensible:

- Incluye: explicación de consecuencias + botones con verbo específico (Delete account / Aplicar cambios).[^5]
- No incluye: “¿Estás seguro?” genérico sin impacto ni detalle.
- Sensible: evita poner acciones peligrosas pegadas a benignas (p.ej., “Archivar” al lado de “Eliminar” sin separación).[^8]


## Audit log visible (sin volverse SIEM)

Buenas prácticas de logging de seguridad incluyen registrar actividades privilegiadas (por ejemplo cambios de privilegios) con suficiente detalle para trazabilidad.[^7]
También se recomienda capturar datos clave del evento (timestamp e identificación del usuario, entre otros) con cuidado de no registrar información privada innecesaria.[^9]

Patrones UX para “audit log visible” en CRM enterprise:

- “History/Audit” como pestaña de primera clase en entidades clave
    - Ej.: Account, Deal, Pricing Rule, User, Role, Policy.
- Vista por evento (quién / qué / cuándo / desde dónde)
    - “Quién”: usuario/rol efectivo.
    - “Qué”: acción + objeto + campos cambiados (ideal con diff).
    - “Cuándo”: timestamp.
    - “Desde dónde”: IP / app / integración (si aplica).
- Filtros listos para auditoría operativa
    - `Cambios de permisos`, `Acciones de borrado`, `Exportaciones`, `Cambios de pricing`.
- “Explainability” para soporte
    - Link desde errores: `Ver evento en audit log`.

Controles y seguridad del propio log:

- Los audit logs deben protegerse contra manipulación y acceso no autorizado (son un activo sensible) y aplicar control de acceso estricto al sistema de logs.[^10]
- No registrar credenciales/tokens en claro y aplicar minimización de datos en lo que se guarda.[^10]
- En productos enterprise, es común que los audit logs cubran cambios de permisos y seguridad (ejemplo: logs de auditoría que registran cambios en permisos/configuración).[^11]

Incluye / No incluye / Sensible:

- Incluye: “visibilidad operativa” para admins y soporte, con filtros útiles.
- No incluye: exponer audit logs completos a roles de ventas por defecto (riesgo interno).
- Sensible: logs con PII o secretos; aplicar masking y minimización.[^10]

Ejemplo aplicado (evento de permisos):
`Admin juan.p cambió rol de maria.r: Sales → Sales+Refunds (scope: Sucursal CCS)` (evento tipo “privilege_change”).[^7]

## “Undo” para acciones reversibles (y cuándo no)

Dar “undo” reduce ansiedad y mejora control del usuario; un ejemplo conocido es el “Undo” contextual para acciones destructivas como borrado accidental.[^6]
En confirmaciones destructivas, idealmente se permite deshacer cuando sea posible; si no se puede, se incrementa fricción (p.ej. confirmación más deliberada).[^5]

Patrones UX:

- “Soft delete” + snackbar con Undo (ventana corta)
    - Útil: archivar, desasignar owner, remover item, mover etapa.
    - Evitar auto-dismiss sin alternativa inline en web cuando el usuario necesita recuperar la acción.[^12]
- “Undo” real requiere reversión real
    - Si tu backend no soporta revertir, no muestres “undo” (es peor que no tenerlo).
- “Undo” vs “Restore”
    - Undo: inmediato y temporal.
    - Restore: desde papelera/archivados con permisos adecuados.

Ejemplos aplicados:

- Reversible: “Se archivó el Deal \#8921” `[Deshacer]`
- No reversible (o regulatorio): “Se eliminó el registro fiscal” (sin undo; en su lugar: doble confirmación + auditoría reforzada).[^5]

Pregunta para aterrizar esto a tu CRM: ¿tu modelo de permisos es 100% RBAC (roles) o mezcla RBAC + condiciones por atributo (ABAC) para alcance (sucursal/país/canal)?
<span style="display:none">[^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41]</span>

<div align="center">⁂</div>

[^1]: https://csrc.nist.gov/projects/role-based-access-control

[^2]: https://profsandhu.com/journals/tissec/ANSI+INCITS+359-2004.pdf

[^3]: https://learn.microsoft.com/es-es/azure/azure-monitor/logs/granular-rbac-log-analytics

[^4]: https://m3.material.io/components/dialogs/guidelines

[^5]: https://uxpsychology.substack.com/p/how-to-design-better-destructive

[^6]: https://www.nngroup.com/articles/user-mistakes/

[^7]: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Vocabulary_Cheat_Sheet.html

[^8]: https://www.nngroup.com/articles/proximity-consequential-options/

[^9]: https://top10proactive.owasp.org/the-top-10/c9-security-logging-and-monitoring/

[^10]: https://www.sonarsource.com/resources/library/audit-logging/

[^11]: https://docs.sonarsource.com/sonarqube-server/9.8/instance-administration/audit-logs

[^12]: https://m3.material.io/components/snackbar/guidelines

[^13]: https://blog.ansi.org/ansi/role-based-access-control-rbac-incits-359/

[^14]: https://en.wikipedia.org/wiki/Role-based_access_control

[^15]: https://blog.securelayer7.net/a09-security-logging-and-monitoring/

[^16]: https://www.reddit.com/r/UXDesign/comments/1g5lz1p/snackbar_after_dialog_confirmation/

[^17]: https://csrc.nist.gov/files/pubs/journal/2010/06/adding-attributes-to-rolebased-access-control/final/docs/kuhn-coyne-weil-10.pdf

[^18]: https://stackoverflow.com/questions/53497575/confirm-message-before-closing-material-dialog-accidentally-in-angular

[^19]: https://csrc.nist.gov/projects/role-based-access-control/faqs

[^20]: https://www.chaossearch.io/blog/cyber-security-logging

[^21]: https://mui.com/material-ui/react-snackbar/

[^22]: https://pathlock.com/blog/role-based-access-control-rbac/

[^23]: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

[^24]: https://m2.material.io/develop/web/components/dialogs

[^25]: https://uxplanet.org/confirmation-dialogs-how-to-design-dialogues-without-irritation-7b4cf2599956

[^26]: https://github.com/MaterialDesignInXAML/MaterialDesignInXamlToolkit/wiki/Snackbar

[^27]: https://www.designsystemscollective.com/designing-better-buttons-how-to-handle-destructive-actions-d7c55eef6bdf

[^28]: https://proandroiddev.com/implementing-snackbar-to-undo-actions-in-jetpack-compose-7b8ec92cf8a7

[^29]: https://m1.material.io/components/dialogs.html

[^30]: https://blog.iamsuleiman.com/material-design-snackbar/

[^31]: https://shiftasia.com/community/applying-jakob-nielsens-10-usability-heuristics-for-better-ux-design/

[^32]: https://www.andrewcoyle.com/blog/designing-confirmation

[^33]: https://www.oligo.security/academy/owasp-top-10-cheat-sheet-of-cheat-sheets

[^34]: https://www.scribd.com/document/752825173/OWASP-Logging-Cheat-Sheet

[^35]: https://github.com/hashicorp/terraform-provider-aws/issues/19010

[^36]: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

[^37]: https://www.zengrc.com/blog/audit-log-best-practices-for-information-security/

[^38]: https://stackoverflow.com/questions/56336942/terraform-apply-has-different-plan-than-terraform-plan

[^39]: https://pangea.cloud/securebydesign/secure-audit-records/

[^40]: https://discuss.hashicorp.com/t/is-there-any-way-to-check-for-diffs-after-executing-apply-in-terraform-test/61534

[^41]: https://docs.rapid7.com/insightvm/audit-logs/

