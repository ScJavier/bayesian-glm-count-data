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
- **Entorno:** uv ✅ (`pyproject.toml` + `uv.lock`)
- **Python:** 3.11.15
- **Kernel Jupyter:** `bayesian-glm-count-data` registrado
- **GitHub:** ✅ github.com/ScJavier/bayesian-glm-count-data (privado)
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

- [x] ~~Ejecutar `03_inferencia_bayesiana.ipynb`~~ — `.nc` regenerados con y_rep + log_lik (2026-04-04)
- [x] ~~Renombrar proyecto a `bayesian-glm-count-data`~~ (2026-04-04)
- [ ] Completar `05_ppc_sobredispersion.ipynb` con métricas de sobredispersión

## Historial de acciones de Claude

### 2026-04-04 (sesión 1)
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

### 2026-04-04 (sesión 3)
- Sección `## Referencias` agregada al README.md con 6 citas verificadas
- Referencias: Gelman et al. 2020, Gabry et al. 2019, Schad et al. 2021, Gelman & Shalizi 2013, BDA3, Martin et al. 2021

### 2026-04-04 (sesión 2)
- Migración de `.venv` roto (symlink a pyenv inexistente) a uv
- Kernel Jupyter registrado: `bayesian-glm-count-data`
- requirements.txt eliminado (pyproject.toml + uv.lock son la fuente de verdad)
- Proyecto renombrado a `bayesian-glm-count-data`
- nbstripout instalado — outputs se limpian automáticamente en cada commit
- Repo GitHub creado y pusheado: github.com/ScJavier/bayesian-glm-count-data (privado)
- 03_inferencia_bayesiana ejecutado — .nc regenerados con y_rep + log_lik
