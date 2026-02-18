<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_02_Repo_Sweep_Static_Analysis_DeadCode

## Executive summary (10–15 líneas)

### Facts

- Un “repo sweep” efectivo combina **call graph** + grafo de dependencias + señales de “reachability” para acercarse a “qué corre realmente” vs “qué existe en el repo”.[^1]
- CodeQL permite navegar el call graph y formular queries para detectar “callables” que no son llamados (con filtros para reducir falsos positivos).[^1]
- Para ejecutar CodeQL necesitas construir una base de datos del código con la información necesaria para correr queries.[^2]
- Semgrep permite reglas sintácticas con exclusiones (p. ej. `pattern-not`) para ajustar falsos positivos y modelar convenciones de entrypoints.[^3]
- En TypeScript, `ts-prune` puede integrarse al CI para fallar PRs que introducen exports no usados (bueno para evitar regresión de “dead exports”).[^4]
- En Python, Vulture detecta código no usado y advierte limitaciones por la naturaleza dinámica del lenguaje.[^5]
- En Node.js, `depcheck` analiza dependencias y reporta cuáles son “useless” y cuáles faltan en `package.json`.[^6]
- En Go, `staticcheck` reporta símbolos no usados con el código U1000 (variables, funciones, etc.).[^7]
- En `golangci-lint`, varios linters clásicos de “unused/dead code” fueron deprecados (impacta qué activar en pipelines).[^8]


### Inferences

- La parte “difícil” no es detectar dead code aislado, sino mapear entrypoints no obvios (cron/queues/rutas/eventos) y reducir falsos positivos antes de borrar.
- La metodología más reproducible es “de lo seguro a lo agresivo”: primero inventariar y marcar reachability, luego proponer deletes con rollback rápido (PR pequeño + pruebas + observabilidad).

***

## Definitions and why it matters

### Facts

- Un **call graph** representa relaciones de llamadas (quién llama a quién) y permite queries como “qué no es llamado por nadie”, con soporte directo en librerías de CodeQL para Java/Kotlin mediante abstracciones como `Callable` y `Call`.[^1]
- El análisis de **data flow** modela el flujo de datos mediante un “data flow graph” (distinto del AST) para razonar sobre valores a través del programa.[^9]


### Inferences

- “Dead code” (código no usado) en enterprise suele estar “vivo” por entrypoints indirectos: reflection, DI, handlers registrados por nombre, jobs programados, consumers de colas, flags, o llamadas desde infraestructura.
- Importa porque reduce riesgo operativo (menos superficie), acelera cambios (menos ruido) y mejora costos (builds más rápidos, menos dependencias, menos CVEs por supply chain).

***

## Principles and best practices (con citas por sección + fecha)

### Facts

- **Base reproducible de análisis:** en CodeQL, primero se prepara una base de datos del código (requisito para correr queries de manera consistente en CI).[^2]
- **Call graph first, then filters:** el ejemplo de CodeQL para “Not called” muestra cómo refinar (p. ej. limitar a source files, excluir tests, etc.) para bajar falsos positivos.[^1]
- **Reglas ajustables por convención:** Semgrep soporta exclusiones como `pattern-not` para eliminar matches comunes y afinar reglas según tu arquitectura (p. ej. “todo consumer debe tener decorator X”).[^3]
- **Prevenir reaparición:** `ts-prune` puede correr en CI y fallar PRs al introducir exports no usados, evitando que el dead code vuelva silenciosamente.[^4]
- **Aceptar límites del estático:** Vulture advierte que por lo dinámico de Python puede “perder” dead code o reportar como unused lo que se llama implícitamente.[^5]
- **Limpiar dependencias también es parte del sweep:** `depcheck` reporta dependencias no usadas y dependencias faltantes, ayudando a depurar el grafo de paquetes.[^6]
- **Señal fuerte en Go:** `staticcheck` detecta símbolos no usados con U1000 (útil para barridos por paquete/servicio).[^7]
- **Cuidado con el stack de linters:** en Go, algunos linters de “dead/unused” fueron deprecados dentro de `golangci-lint`, así que conviene validar qué queda activo y con qué equivalencia.[^8]
- Fecha de consulta: 2026-02-17.


### Inferences

- Principio operativo: “no borres nada que no puedas explicar”; cada delete debe tener: por qué está muerto, cuál era el entrypoint supuesto, cómo lo validaste, y cómo revertir.
- Principio de riesgo: rutas/cron/queues son “sensibles” porque pueden activarse fuera del request/response normal (horarios, retries, backfills, integraciones B2B).

***

## Examples (aplicado a CRM enterprise)

### Facts

- Puedes usar CodeQL para buscar funciones/métodos que no son llamados (“Not called”) y luego iterar filtros (tests, públicos, inicializadores) como propone el ejemplo de “Navigating the call graph”.[^1]
- Puedes crear reglas Semgrep con inclusiones/exclusiones (`pattern-not`) para “marcar” entrypoints válidos (p. ej. “todo job debe tener `@Scheduled` o config equivalente”) y reducir falsos positivos.[^3]


### Inferences

- Caso CRM enterprise: tienes “AccountSyncJob” (cron) + “LeadIngestConsumer” (queue) + “LegacyOpportunityEndpoint” (ruta HTTP). El sweep detecta que el endpoint no tiene callers, pero el consumer sí aparece “no llamado” en call graph porque se registra por framework; ahí Semgrep/convenciones + config de despliegue definen reachability.
- Resultado esperado: “LegacyOpportunityEndpoint” se elimina (PR separado) mientras “LeadIngestConsumer” se mantiene pero se documenta como entrypoint indirecto y se prueba con un “smoke event” (mensaje real o fixture).

***

## Metrics / success signals

### Facts

- `depcheck` puede entregar listas de dependencias no usadas y faltantes; estas salidas sirven como métrica base “antes/después” de limpieza de paquetes.[^6]
- `staticcheck` reporta hallazgos U1000 para símbolos no usados, lo que puede cuantificarse por repo/paquete para medir reducción de “unused”.[^7]
- Vulture reporta unused code y reconoce límites por dinámica; útil como métrica de “tendencia”, no como verdad absoluta.[^5]


### Inferences

- Métricas recomendadas (operables en CI): \# de exports no usados (TS), \# de U1000 (Go), \# de findings Vulture (Py), \# de deps “useless”, tiempo de build/test, tamaño de artefactos, y tasa de rollback por sweep.
- Señal comercial/operativa (B2B real): menos incidentes por jobs fantasma, menos CVEs por dependencias muertas, y menos fricción al estimar cambios (menos “código zombi” que revisar).

***

## Operational checklist

### Facts

- CodeQL: crear DB del código antes de correr queries, para asegurar análisis consistente y repetible.[^2]
- CodeQL: correr query tipo “Not called” y refinar con filtros para bajar falsos positivos según el ejemplo de call graph.[^1]
- Semgrep: crear reglas con exclusiones (`pattern-not`) para modelar entrypoints y excepciones permitidas.[^3]
- TS: ejecutar `ts-prune` e idealmente gatearlo en CI para prevenir nuevos exports no usados.[^4]
- Python: correr Vulture y tratar resultados como candidatos (por límites del estático en Python).[^5]
- Node: correr `depcheck` para identificar dependencias “useless” y faltantes.[^6]
- Go: correr `staticcheck` y priorizar U1000 como quick wins de limpieza segura.[^7]


### Inferences

- Inventario inicial (incluye / no incluye / sensible): incluye entrypoints HTTP, CLIs, workers, cronjobs, consumers; no incluye borrado masivo sin PRs pequeños; sensible = anything triggered by schedule/queue/webhook/feature-flag.
- Validación mínima por delete: (1) tests + build, (2) búsqueda de configuración (YAML/helm/terraform) que lo referencie, (3) observabilidad: no baja coverage de rutas críticas, (4) plan de rollback (revert PR).

***

## Anti-patterns

### Facts

- Vulture advierte que puede fallar en detectar dead code o marcar como unused código llamado implícitamente, por la naturaleza dinámica de Python; borrar “a ciegas” desde ese output es riesgoso.[^5]
- El enfoque de `ts-prune` puede fallar en casos donde el export “parece usado” solo por tests, lo que muestra que los detectores tienen edge-cases y requieren criterio operativo.[^4]


### Inferences

- “Borrar por volumen”: eliminar 200 archivos en un PR sin trazabilidad de entrypoints es receta para incidentes (sobre todo cron/queues).
- Confundir “no hay callers en call graph” con “no corre en prod”: frameworks registran handlers por reflexión/config y eso rompe el supuesto.

***

## Diagnostic questions

### Facts

- ¿Tienes una forma estándar de construir la base de datos de CodeQL para todos los repos y correr las mismas queries?[^2]
- ¿Tienes queries de call graph (p. ej. “Not called”) con filtros acordados para evitar falsos positivos recurrentes?[^1]
- ¿Usas reglas Semgrep con exclusiones (`pattern-not`) para expresar “esto es un entrypoint válido” (routes/jobs/consumers) por convención?[^3]
- ¿Tu CI previene regresión de exports muertos con algo como `ts-prune`?[^4]


### Inferences

- ¿Dónde vive la “lista de entrypoints indirectos” (cron/queues/webhooks) y quién la aprueba cuando cambia?
- ¿Cuál es tu política de riesgo: opción segura (solo deletes con reachability demostrada) vs opción agresiva (deletes con monitoreo y rollback rápido)?

***

## Sources (o referencia a SOURCES.md)

- CodeQL — Navigating the call graph (ejemplos “Not called”, refinamientos): https://codeql.github.com/docs/codeql-language-guides/navigating-the-call-graph/[^1]
- GitHub Docs — Preparing your code for CodeQL analysis (crear CodeQL database): https://docs.github.com/en/code-security/tutorials/customize-code-scanning/preparing-your-code-for-codeql-analysis[^2]
- CodeQL — About data flow analysis (data flow graph): https://codeql.github.com/docs/writing-codeql-queries/about-data-flow-analysis/[^9]
- Semgrep Docs — Rule structure syntax (`pattern-not`, paths, etc.): https://semgrep.dev/docs/writing-rules/rule-syntax[^3]
- Theodo — Strategy using ts-prune (CI gate + caveats): https://www.theodo.com/en-fr/blog/seek-and-destroy-dead-code-for-good-a-strategy-using-ts-prune[^4]
- Vulture (PyPI) — Find dead code + limitaciones: https://pypi.org/project/vulture/[^5]
- depcheck (npm) — analiza dependencias, useless/missing/using: https://www.npmjs.com/package/depcheck[^6]
- Staticcheck (ejemplo U1000 unused): http://www.abeji.de/staticchecking-go/[^7]
- golangci-lint issue — deprecate deadcode/varcheck/structcheck (contexto de linters): https://github.com/golangci/golangci-lint/issues/1841[^8]


### SOURCES.md additions (sin duplicados)

- https://codeql.github.com/docs/codeql-language-guides/navigating-the-call-graph/
- https://docs.github.com/en/code-security/tutorials/customize-code-scanning/preparing-your-code-for-codeql-analysis
- https://codeql.github.com/docs/writing-codeql-queries/about-data-flow-analysis/
- https://semgrep.dev/docs/writing-rules/rule-syntax
- https://www.theodo.com/en-fr/blog/seek-and-destroy-dead-code-for-good-a-strategy-using-ts-prune
- https://pypi.org/project/vulture/
- https://www.npmjs.com/package/depcheck
- https://staticcheck.dev/ (si prefieres fuente oficial además del ejemplo práctico)[^10]
- https://github.com/golangci/golangci-lint/issues/1841

***

## Key takeaways for PM practice

- Prioriza un mapa explícito de entrypoints (routes/cron/queues) antes de borrar: sin eso, el sweep se vuelve lotería.
- Estandariza “safe vs aggressive cleanup”: PRs chicos, rollback fácil, y reglas para qué se puede eliminar con evidencia fuerte.
- Mide progreso con señales automáticas (unused deps, unused exports, U1000) y con señales operativas (incidentes, velocidad de delivery).
<span style="display:none">[^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29]</span>

<div align="center">⁂</div>

[^1]: https://codeql.github.com/docs/codeql-language-guides/navigating-the-call-graph/

[^2]: https://docs.github.com/en/code-security/tutorials/customize-code-scanning/preparing-your-code-for-codeql-analysis

[^3]: https://semgrep.dev/docs/writing-rules/rule-syntax

[^4]: https://www.theodo.com/en-fr/blog/seek-and-destroy-dead-code-for-good-a-strategy-using-ts-prune

[^5]: https://pypi.org/project/vulture/

[^6]: https://www.npmjs.com/package/depcheck

[^7]: http://www.abeji.de/staticchecking-go/

[^8]: https://github.com/golangci/golangci-lint/issues/1841

[^9]: https://codeql.github.com/docs/writing-codeql-queries/about-data-flow-analysis/

[^10]: https://staticcheck.dev/docs/configuration/

[^11]: pasted-text.txt

[^12]: https://www.patferraggi.dev/blog/2020/mar/5-clean-code-tecnicas

[^13]: https://certifiedtechdeveloper.com/soluciones-para-la-deteccion-automatica-de-ciclos-de-dependencia-herramientas-y-metodos-avanzados/

[^14]: https://github.blog/developer-skills/github/codeql-zero-to-hero-part-1-the-fundamentals-of-static-analysis-for-vulnerability-research/

[^15]: https://codeql.github.com/docs/writing-codeql-queries/creating-path-queries/

[^16]: https://appsec.guide/docs/static-analysis/semgrep/advanced/

[^17]: https://www.luke-dev.com/blog/finding-unused-exports-with-ts-prune

[^18]: https://github.com/github/codeql/discussions/15982

[^19]: https://semgrep.dev/docs/semgrep-code/pro-rules

[^20]: https://semgrep.dev/docs/semgrep-supply-chain/glossary

[^21]: https://github.com/jendrikseipp/vulture

[^22]: https://adamj.eu/tech/2023/07/12/django-clean-up-unused-code-vulture/

[^23]: https://www.reddit.com/r/Python/comments/1iwbnlh/i_made_a_python_tool_to_detect_unused_code_in/

[^24]: https://www.thatsoftwaredude.com/content/13929/check-unused-modules-node

[^25]: https://github.com/dominikh/go-tools/issues/1333

[^26]: https://www.youtube.com/watch?v=qlX9znhqQ6Q

[^27]: https://classic.yarnpkg.com/en/package/depcheck

[^28]: https://www.youtube.com/watch?v=VmaWQQp4LU8

[^29]: https://dev.to/himanshudevgupta/how-to-check-unused-npm-packages-1hp2

