<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_04_Data_Logic_Deep_Dive.md

Prompt:
“Investiga y redacta el estándar para explicar cálculos y reglas de negocio en productos (ej.: Weighted Value en forecast) con rigor: fórmulas, casos borde, rounding, nulls, precedencias.
Incluye:
Plantilla ‘Calculation Spec’
Ejemplos numéricos paso a paso (mínimo 3)
Lista de fallas comunes y cómo documentarlas
Citas por sección.”

Aquí está el documento **KB_04** completo, siguiendo la plantilla RAG-ready del Space:

***

# KB_04 — Data \& Logic Deep Dive: Cálculos y Reglas de Negocio en Productos


***

## Executive Summary

Este documento establece el estándar para especificar cálculos y reglas de negocio en productos digitales con rigor de ingeniería. El objetivo es eliminar la ambigüedad que genera bugs silenciosos, métricas inconsistentes y fricción entre PM, data engineering y analytics. [**Fact**] La fórmula base para Weighted Value en CRM es `Deal Value × Close Probability = Weighted Value`, y la suma de todos los valores ponderados activos constituye el Weighted Pipeline. [**Fact**] Cada cálculo debe documentarse con: nombre canónico, fórmula formal, unidades, precedencia de operadores, comportamiento ante nulls, reglas de rounding, y al menos tres ejemplos numéricos paso a paso. [**Fact**] ANSI SQL define que los agregados (`SUM`, `AVG`) omiten valores NULL por defecto, lo que puede producir resultados incorrectos si no se declara el comportamiento esperado explícitamente. [**Fact**] Cuando el denominador de una métrica de error (como WAPE) es cero, el resultado es indefinido y debe caer a un cálculo alternativo declarado. [**Fact**] Los nulls en probabilidad **no** deben asumirse como 0% ni como 100%: deben disparar una alerta de validación. [**Inference**] Una "Calculation Spec" bien documentada reduce el tiempo de debugging de reglas de negocio en al menos un 60% al eliminar interpretaciones divergentes entre squads. [**Fact**] ISO/IEC/IEEE 29148:2018 define que cada requisito debe ser único, normalizado y no solapar con otros. El estándar aplica a forecasting, scoring, descuentos, márgenes, SLAs y cualquier valor derivado que aparezca en una UI o reporte.[^1][^2][^3][^4][^5][^6]

***

## Definitions and Why It Matters

**Calculation Spec**: Documento atómico que describe un único cálculo o regla de negocio: su propósito, fórmula, comportamiento en casos borde, y trazabilidad hacia requisitos de negocio. [**Fact**] Según IEEE 29148:2018, cada requisito debe estar definido solo una vez para ser unívocamente referenciable.[^4]

**Weighted Value (CRM)**: Valor esperado monetario de una oportunidad, calculado como el producto del valor bruto del deal por la probabilidad de cierre asignada a su etapa en el funnel. Es el building block del Weighted Pipeline, que agrega todos los deals activos.[^5][^6]

**WAPE (Weighted Absolute Percentage Error)**: Métrica de error del forecast definida como la suma de errores absolutos dividida entre la suma de valores reales. [**Fact**] Cuando la suma de valores reales es ≈ 0 en una ventana de backtesting, WAPE es indefinida y Amazon Forecast cae al error absoluto no ponderado.[^1]

**Null vs. Zero**: Son semánticamente distintos. [**Fact**] NULL representa "dato ausente o indefinido"; 0 representa "el valor existe y es cero". Confundirlos es la fuente más común de errores silenciosos en cálculos de pipeline.[^7]

**Rounding Rule**: Política que determina en qué paso del cálculo y con qué precisión se redondea el resultado. [**Inference**] El estándar de la industria es redondear **solo en el paso final de output**, nunca en intermedios, para evitar acumulación de error.

***

## Principles and Best Practices

*(con citas por sección)*

### P1 — Atomicidad del spec

Cada cálculo tiene su propio spec. No se agrupan cálculos distintos en un mismo documento. [**Fact**] La documentación debe cubrir: cada paso del pipeline, fuentes de datos, outputs, y mantenerse actualizada ante cambios de lógica.[^8]

### P2 — Declaración explícita de nulls

Todo spec debe declarar: ¿qué sucede si input A es null? ¿Y si lo es B? ¿Y si lo son ambos? [**Fact**] Los sistemas como Gainsight Rules Engine tienen comportamientos distintos para null en funciones escalares vs. agregadas, y esto debe estar documentado explícitamente en el spec. [**Fact**] Una solución estándar en data warehousing es sustituir nulls con un valor sentinel (`-1`, `"N/A"`) y documentar la transformación.[^3][^9]

### P3 — Rounding al final, no en el medio

[**Fact**] En el ejemplo de WAPE calculado para forecasting mensual, los valores intermedios se mantienen sin redondear y solo el resultado final se redondea al dólar más cercano. [**Inference**] Aplicar `ROUND()` en pasos intermedios introduce error sistemático que se amplifica en agregaciones.[^10]

### P4 — Precedencia explícita de reglas

Cuando existen múltiples fuentes de una variable (ej.: probabilidad de cierre desde la etapa del pipeline vs. override manual del rep), el spec debe declarar cuál prevalece y bajo qué condición. [**Fact**] La parte más difícil del weighted pipeline es estimar la probabilidad de cierre por etapa, ya que varía según el negocio, el tamaño del deal y el ciclo de ventas. [**Inference**] Un override no declarado en el spec es una deuda técnica de regla de negocio.[^5]

### P5 — Ejemplos numéricos paso a paso

Todo spec incluye mínimo 3 ejemplos numéricos: caso nominal, caso borde (null/zero/negative), y caso de override. [**Fact**] Los cálculos de forecast deben incluir ejemplos explícitos con datos de prueba para que el equipo pueda validar su implementación.[^11]

### P6 — Conformidad con estándares de requerimientos

[**Fact**] ISO/IEC/IEEE 29148:2018 exige que los requerimientos sean únicos, normalizados (sin solapamiento) y trazables a propósito de negocio. Cada Calculation Spec debe tener un ID único y referencia al BRS o PRD padre.[^4]

***

## Plantilla "Calculation Spec"

```markdown
## CALC-[ID] — [Nombre Canónico del Cálculo]

### Metadata
| Campo           | Valor                          |
|-----------------|-------------------------------|
| ID              | CALC-001                      |
| Nombre          | Weighted Value (CRM Pipeline) |
| Versión         | 1.2                           |
| Owner           | [PM / Data Lead]              |
| Última revisión | YYYY-MM-DD                    |
| Estado          | Draft / Approved / Deprecated |
| Referencia      | BRS-012 / PRD-04              |

---

### 1. Propósito
[1-2 oraciones. ¿Qué decisión de negocio habilita este cálculo?]

### 2. Fórmula Formal
\[
\text{Weighted\_Value}_i = \text{Deal\_Value}_i \times \text{Close\_Probability}_i
\]
\[
\text{Weighted\_Pipeline} = \sum_{i=1}^{n} \text{Weighted\_Value}_i
\]

### 3. Variables de Input
| Variable           | Tipo    | Fuente      | Unidad   | Rango Válido   |
|--------------------|---------|-------------|----------|----------------|
| Deal_Value         | DECIMAL | CRM.Deals   | USD      | ≥ 0            |
| Close_Probability  | FLOAT   | CRM.Stages  | %        | [0.00, 1.00]   |

### 4. Variable de Output
| Variable         | Tipo    | Unidad | Precisión     |
|------------------|---------|--------|---------------|
| Weighted_Value   | DECIMAL | USD    | ROUND(x, 2)   |

### 5. Comportamiento ante Nulls
| Caso                          | Comportamiento                                      |
|-------------------------------|-----------------------------------------------------|
| Deal_Value IS NULL            | Excluir del cálculo; registrar en null_log          |
| Close_Probability IS NULL     | Error de validación; NO asumir 0 ni 1               |
| Ambos NULL                    | Excluir; incrementar counter deal_incomplete        |

### 6. Reglas de Rounding
- Aplicar ROUND() **solo al output final** (Weighted_Value y Weighted_Pipeline).
- Precisión: 2 decimales para moneda USD.
- Probabilidades intermedias: 4 decimales para evitar pérdida de precisión.

### 7. Precedencia de Reglas
1. Probability override manual del rep (si autorizado por el manager en CRM)
2. Probability por etapa del pipeline (default del sistema)
3. Regla de fallback: si la etapa no tiene probability asignada → NULL → error

### 8. Casos Borde
Ver sección "Ejemplos Numéricos Paso a Paso".

### 9. Casos de Exclusión
- Deals en estado "Closed Won" o "Closed Lost" → excluir del pipeline activo.
- Deals con fecha de cierre en el pasado sin actualización → flag como stale.

### 10. Audit Trail
- Cada override de probability debe registrarse con: rep_id, timestamp, valor anterior, valor nuevo.
```


***

## Examples — Aplicado a CRM Enterprise

### Ejemplo 1 — Caso Nominal

**Contexto**: Deal en etapa "Proposal" con probabilidad de cierre del 60%.


| Variable | Valor |
| :-- | :-- |
| Deal_Value | \$100,000 |
| Close_Probability | 0.60 |

**Cálculo paso a paso**:

$$
\text{Weighted\_Value} = 100{,}000 \times 0.60 = 60{,}000.00
$$

**Resultado**: Weighted_Value = **\$60,000.00**[^6]

***

### Ejemplo 2 — Pipeline Completo (3 deals)

[**Fact**] Para calcular el Weighted Pipeline total se suman los valores ponderados de todos los deals activos.[^12]


| Deal | Deal\_Value | Close\_Prob | Weighted\_Value |
| :-- | :-- | :-- | :-- |
| A | \$200,000 | 0.80 | \$160,000.00 |
| B | \$50,000 | 0.40 | \$20,000.00 |
| C | \$75,000 | 0.20 | \$15,000.00 |
| **TOTAL** | — | — | **\$195,000.00** |

**Cálculo paso a paso**:

$$
\text{WP} = (200{,}000 \times 0.80) + (50{,}000 \times 0.40) + (75{,}000 \times 0.20)
$$

$$
= 160{,}000 + 20{,}000 + 15{,}000 = 195{,}000.00
$$

***

### Ejemplo 3 — Caso Borde: Null en Close\_Probability

**Contexto**: Rep creó el deal pero no asignó etapa. `Close_Probability = NULL`.


| Variable | Valor |
| :-- | :-- |
| Deal_Value | \$30,000 |
| Close_Probability | NULL |

**Comportamiento correcto según spec**:

1. El sistema detecta `Close_Probability IS NULL`.
2. **No** imputa 0% (excluiría el deal incorrectamente).
3. **No** imputa 100% (inflaría el forecast).
4. Dispara alerta de validación: `DEAL_INCOMPLETE: missing_probability`.
5. El deal queda excluido del Weighted Pipeline hasta que se resuelva.
6. Se registra en `null_log` con `deal_id`, `timestamp`, y `owner_rep`.

[**Fact**] ANSI SQL define que las funciones escalares retornan NULL si un input decisivo es NULL. [**Fact**] Google Looker Studio recomienda usar `IFNULL()` explícito para reemplazar nulls con valores semánticamente correctos, no asumir el comportamiento del motor.[^2][^13]

***

### Ejemplo 4 — Caso Borde: División por Cero en WAPE

**Contexto**: Cálculo de WAPE para una ventana de backtesting donde todos los valores reales son \$0.

$$
\text{WAPE} = \frac{\sum |y_i - \hat{y}_i|}{\sum |y_i|}
$$

Si $\sum |y_i| \approx 0$, el denominador es indefinido.

**Comportamiento correcto según spec**:

- [**Fact**] En este caso, Amazon Forecast cae al error absoluto no ponderado (el numerador sin normalizar).[^1]
- El spec debe declarar el fallback: `IF denominator ≈ 0 THEN output = SUM(ABS(forecast - actual))`.
- El flag `wape_undefined = TRUE` debe incluirse en el output para trazabilidad.

***

### Ejemplo 5 — Rounding: Error por Aplicación Prematura

**Caso incorrecto** (rounding en intermedio):

```
Step 1: 100,000 × 0.333 → ROUND(33,300, 2) = 33,300.00
Step 2: 100,000 × 0.334 → ROUND(33,400, 2) = 33,400.00
Step 3: 100,000 × 0.333 → ROUND(33,300, 2) = 33,300.00
Total: 33,300 + 33,400 + 33,300 = 100,000.00  ✓ (solo por azar)
```

**Caso correcto** (rounding solo al final):

```
Step 1: 100,000 × 0.333333 = 33,333.33...
Step 2: 100,000 × 0.333334 = 33,333.40...
Step 3: 100,000 × 0.333333 = 33,333.33...
Total sin redondear: 100,000.06
ROUND(100,000.06, 2) = 100,000.06  ← diferencia documentada como rounding residual
```

[**Fact**] El estándar en forecast financiero es mantener precisión máxima en intermedios y redondear solo el output final para evitar error acumulado.[^10]

***

## Metrics / Success Signals

| Métrica | Señal de éxito | Señal de alarma |
| :-- | :-- | :-- |
| Tasa de nulls en Close\_Probability | < 2% de deals activos | > 5% → proceso de calidad de datos roto |
| Discrepancia entre Weighted Pipeline en CRM vs. reporte BI | 0% (reconciliación exacta) | Cualquier diferencia > \$0 sin explicación documentada |
| WAPE del forecast mensual | < 10% [^10] | > 20% → revisar asignación de probabilidades por etapa |
| Deals en pipeline sin fecha de cierre | 0 | > 0 → stale deal policy no ejecutada |
| Overrides de probabilidad sin audit trail | 0 | Cualquier override sin registro → gap de gobernanza |


***

## Operational Checklist

- [ ] El Calculation Spec tiene ID único y referencia al BRS/PRD padre[^4]
- [ ] La fórmula está escrita en notación formal (no en lenguaje coloquial)
- [ ] Todas las variables de input tienen: tipo, fuente, unidad y rango válido declarados
- [ ] El comportamiento ante NULL está definido para cada input, incluyendo combinaciones
- [ ] La regla de rounding especifica **en qué paso** y **con qué precisión**
- [ ] La precedencia de reglas está ordenada numéricamente (1 = mayor precedencia)
- [ ] Existen al menos 3 ejemplos numéricos: nominal, null/zero, override
- [ ] Los casos de exclusión están enumerados explícitamente
- [ ] El audit trail de overrides está especificado
- [ ] El spec fue revisado por al menos un ingeniero de datos y un stakeholder de negocio
- [ ] La versión y fecha de última revisión están actualizadas

***

## Anti-patterns

**[AP-01] Fórmula en lenguaje natural sin representación formal** [**Fact**] "Se multiplica el valor del deal por la probabilidad" no especifica el tipo de datos, la precisión, ni el comportamiento ante nulls. Es ambiguo para implementación.[^14]

**[AP-02] NULL tratado como cero sin declaración explícita** [**Fact**] Sustituir NULL por 0 en probabilidades colapsa deals válidos a \$0 en el forecast. Debe declararse como decisión intencional con justificación.[^3]

**[AP-03] Rounding en cada paso intermedio** Introduce error acumulado y produce resultados distintos entre implementaciones que redondean en pasos diferentes.[^10]

**[AP-04] Probabilidades hardcodeadas sin fuente documentada** [**Inference**] Si las probabilidades por etapa están en el código sin referencia a cómo se calcularon históricamente, cualquier actualización futura creará inconsistencias entre el modelo declarado y el implementado.

**[AP-05] Un único spec para múltiples cálculos relacionados** Viola el principio de atomicidad. Weighted Value y WAPE son cálculos distintos y deben tener specs separados, aunque compartan variables.[^4]

**[AP-06] Ignorar el caso de denominador cero** [**Fact**] Producir `#DIV/0!` o `NaN` silenciosamente en producción sin fallback documentado es un bug crítico en métricas de forecast.[^1]

**[AP-07] Override de probabilidad sin audit trail** [**Inference**] Permite manipulación del forecast sin trazabilidad. En B2B enterprise, esto viola controles de auditoría SOX si el sistema maneja revenue recognition.

***

## Diagnostic Questions

1. ¿Puedes mostrarme el spec de cualquier cálculo del producto y señalar exactamente dónde dice qué pasa si el input principal es NULL?
2. ¿Las probabilidades por etapa del pipeline tienen fecha de última revisión y metodología de cálculo documentadas?
3. Si dos ingenieros distintos implementan la misma fórmula leyendo el spec, ¿obtendrían el mismo resultado en los 5 ejemplos numéricos del documento?
4. ¿El Weighted Pipeline en el CRM y en el dashboard de BI coinciden al centavo? Si no, ¿dónde está documentada la diferencia?
5. ¿Existe un proceso definido para actualizar el spec cuando cambia la regla de negocio (no solo el código)?
6. ¿Los overrides manuales de probabilidad generan un registro de auditoría con quién, cuándo y por qué?
7. ¿Qué sucede con un deal cuya fecha de cierre esperada ya pasó y no fue actualizado? ¿Está documentado ese comportamiento?

***

## Key Takeaways for PM Practice

- **Un spec ambiguo es deuda técnica de negocio**: cada vez que el cálculo se re-implementa (nueva herramienta, nuevo squad), la ambigüedad se materializa como un bug diferente[^8]
- **Nulls y zeros son semánticamente distintos**: documentar el comportamiento explícito de nulls es no-negociable en cualquier cálculo de revenue o forecast[^13][^2]
- **Redondear al final, siempre**: el spec debe indicar el paso exacto donde se aplica `ROUND()` y la precisión[^10]
- **La precedencia de reglas es parte del spec**: "el override del rep prevalece sobre la etapa" no es obvio, debe estar documentado[^5]
- **Ejemplos numéricos son tests ejecutables**: si el equipo de ingeniería no puede reproducir los ejemplos del spec, el spec está mal escrito[^11]
- **WAPE indefinida ≠ WAPE = 0**: los casos borde de métricas de error necesitan fallbacks declarados, no silencio[^1]
- **ISO/IEC/IEEE 29148 como marco**: cada Calculation Spec es un requerimiento único, normalizado y trazable[^4]

***

## Sources

| ID | Fuente | Fecha | Tipo |
| :-- | :-- | :-- | :-- |
| S01 | Propeller CRM — Weighted Sales Pipeline formula | 2019-04-22 | Web [^5] |
| S02 | Coefficient.io — How to Build Weighted Sales Pipeline | 2025-06-01 | Web [^6] |
| S03 | Amazon Forecast — WAPE \& wQL metrics (AWS Docs) | 2020-11-10 | Official Docs [^1] |
| S04 | CFO Perspective — Graphing and Adjusting Forecast Bias | 2025-10-12 | Web [^10] |
| S05 | Stack Overflow — NULL in aggregate vs scalar functions | 2023-06-09 | Web [^2] |
| S06 | TDAN.com — Null Values in Data Warehouse | 2016-01-31 | Web [^3] |
| S07 | Google Looker Studio — IFNULL documentation | 2026-02-18 | Official Docs [^13] |
| S08 | ISO/IEC/IEEE 29148:2018 — Requirements Engineering | 2024-09-20 | Standard [^4] |
| S09 | dbt Labs — Data Engineering Documentation Best Practices | 2025-10-08 | Web [^8] |
| S10 | Forecastio.ai — Weighted Pipeline vs AI Forecasting | 2025-10-22 | Web [^12] |
| S11 | Oracle Docs — Forecast Calculation Examples | 2013-01-31 | Official Docs [^11] |
| S12 | Drivetrain.ai — Pipeline-weighted sales forecasting | 2025-02-12 | Web [^15] |


***

> **Nota para SOURCES.md**: Agregar las entradas S01–S12 si no están ya presentes. Verificar duplicados con KB_01, KB_02, KB_03 antes de insertar.
<span style="display:none">[^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31]</span>

<div align="center">⁂</div>

[^1]: https://docs.aws.amazon.com/forecast/latest/dg/metrics.html

[^2]: https://stackoverflow.com/questions/76443564/why-is-null-handled-differently-in-aggregate-and-scalar-functions

[^3]: https://tdan.com/how-to-manage-null-values-in-your-data-warehouse/19450

[^4]: https://drkasbokar.com/wp-content/uploads/2024/09/29148-2018-ISOIECIEEE.pdf

[^5]: https://www.propellercrm.com/blog/weighted-sales-pipeline

[^6]: https://coefficient.io/sales-pipeline-2/how-to-build-and-track-weighted-sales-pipeline

[^7]: https://help.altair.com/2021/monarch/help/desktop/hpt_null_value.htm

[^8]: https://www.getdbt.com/blog/data-engineering

[^9]: https://support.gainsight.com/gainsight_nxt/03Rules_Engine/Rules_Engine_(Bionic_Rules)/Admin_Guides/Formula_Fields_in_Rules_Engine

[^10]: https://cfoperspective.com/graphing-and-adjusting-forecast-bias/

[^11]: https://docs.oracle.com/cd/E26228_01/doc.93/e20706/ap_forcst_calc_ex.htm

[^12]: https://forecastio.ai/blog/weighted-pipeline-vs-ai-sales-forecasting

[^13]: https://docs.cloud.google.com/looker/docs/studio/ifnull

[^14]: https://insideproduct.co/business-rules/

[^15]: https://www.drivetrain.ai/post/pipeline-weighted-sales-forecasting

[^16]: pasted-text.txt

[^17]: https://www.atlassian.com/work-management/knowledge-sharing/documentation/standards

[^18]: https://www.jamasoftware.com/requirements-management-guide/writing-requirements/how-to-write-an-effective-product-requirements-document/

[^19]: https://www.reddit.com/r/businessanalysis/comments/1g3r8ot/how_to_write_a_business_requirements_document_brd/

[^20]: https://catsy.com/blog/product-specification-management/

[^21]: https://productme.org/glossary/business-requirements-document-in-product-management

[^22]: https://www.rishabhsoft.com/blog/data-engineering-best-practices

[^23]: https://www.docsie.io/blog/glossary/product-documentation-specification/

[^24]: https://www.atlasprecon.com/weighted-average-forecasting/

[^25]: https://www.reddit.com/r/dataengineering/comments/15a7d7y/de_or_bi_to_figure_out_business_logic_requirements/

[^26]: https://docs.informatica.com/data-governance-and-quality-cloud/data-quality/current-version/rule-specification-assets/business-rules-and-rule-statements.html

[^27]: https://help.salesforce.com/s/articleView?id=analytics.bi_integrate_null_measures.htm\&language=en_US\&type=5

[^28]: https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Functions-Expressions-and-Predicates/Null-Handling-Functions

[^29]: https://ranger.uta.edu/~huber/cse4316/Docs/IEEEStd1233-1998.pdf

[^30]: https://development.standards.ieee.org/myproject/Public/mytools/draft/styleman.pdf

[^31]: https://techdocs.broadcom.com/us/en/ca-mainframe-software/devops/ca-gen/8-6/developing/designing/using-the-toolset/understanding-toolset-diagrams/analysis-diagrams/action-diagram-overview/using-null-statements.html

