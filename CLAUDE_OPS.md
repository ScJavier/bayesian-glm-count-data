# Claude Ops — Bayesian Workflow para Datos de Conteo
_Archivo de gestión interna. Actualizado por Claude Code._

---

## Workflow activo

**Exploración incremental del Bayesian Workflow (Gelman et al. 2020)**

Cada etapa del workflow = un notebook numerado. Los modelos se construyen de forma acumulativa:
empezando con la línea base frecuentista hasta PPCs y expansión de modelos.

**Reglas:**
- Cada variación de un modelo Stan = nuevo archivo `.stan` (nunca modificar el original)
- Los notebooks son el registro de análisis; los scripts son prototipos rápidos
- Los outputs MCMC (`.nc`) son reproducibles — no son fuente de verdad, se regeneran
- El notebook `03_inferencia_bayesiana.ipynb` es el punto de entrada para regenear outputs

**Flujo de trabajo para un nuevo modelo:**
```
definir .stan → agregar generated quantities (y_rep + log_lik) →
correr en 03 (o nuevo notebook) → guardar idata → analizar PPCs en 05
```

---

## Estado actual
- **Git:** ✅ inicializado (rama: master)
- **Entorno:** `.venv` legacy (Python 3.11.14) — no migrar sin indicación explícita
- **Python:** 3.11.14
- **README:** ✅
- **BITACORA:** ✅
- **Backlog:** CLAUDE_OPS.md (este archivo)

## Notebooks — estado

| Notebook | Contenido | Estado |
|---|---|---|
| 01_eda_frecuentista | EDA + Poisson/NegBin statsmodels, dataset cangrejos | ✅ funcional |
| 02_simulacion_distribucion | Visualización Poisson con distintos λ | ✅ funcional |
| 03_inferencia_bayesiana | Grid → MH → Stan, guarda pois_idata.nc y neg_idata.nc | ✅ actualizado (genera y_rep + log_lik) |
| 04_diagnosticos_estudio | Ejercicios BAP book (pymc3 + arviz). Secciones 2E6-2E7 usan .nc | ⚠️ pymc3 no disponible en el entorno del proyecto |
| 05_ppc_sobredispersion | PPCs y métricas de sobredispersión Poisson vs NegBin | 🔧 en desarrollo (sesión 2026-04-04) |

## Modelos Stan — estado

| Modelo | Archivo | generated quantities |
|---|---|---|
| Poisson GLM | models/poisson_model.stan | ✅ y_rep + log_lik (agregado 2026-04-04) |
| Binomial Negativa | models/negative_binomial_model.stan | ✅ y_rep + log_lik + alpha_sm (actualizado 2026-04-04) |

## Backlog

- [ ] Ejecutar `03_inferencia_bayesiana.ipynb` para regenerar `.nc` con y_rep y log_lik
- [ ] Completar `05_ppc_sobredispersion.ipynb` con métricas de sobredispersión
- [ ] Considerar renombrar carpeta del proyecto a `bayesian-glm-count-data` (más descriptivo)
- [ ] Migrar entorno de `.venv` a `uv` cuando sea conveniente

## Historial de acciones de Claude

### 2026-04-04
- Identificado contenido y estructura existente
- Restructura completa: data/, models/, notebooks/, scripts/, outputs/
- Notebooks renombrados con prefijo numérico (01-04)
- Stan models actualizados con generated quantities (y_rep + log_lik)
- Paths actualizados en todos los notebooks
- Celdas de guardado de InferenceData agregadas en 03
- 04_diagnosticos_estudio identificado como ejercicios del libro BAP (Osvaldo Martin)
- git init + primer commit
- README.md, BITACORA.md, CLAUDE_OPS.md creados
- Skeleton de 05_ppc_sobredispersion.ipynb creado
