# Modelos para Datos de Conteo: Un Recorrido Bayesiano

Minicurso sobre GLMs para datos de conteo — desde MLE frecuentista hasta modelos
Zero-Inflated en Stan. Aplicado al dataset **Horseshoe Crab Satellites** (Agresti 2002),
un caso clásico con sobredispersión (D≈3.38) y exceso de ceros (~33%).

> El origen del proyecto fue un problema real de predicción de demanda donde la regresión
> Poisson resultó insuficiente. El recorrido documenta el proceso de exploración sistemática
> — no un tutorial diseñado desde cero.

## Estructura del minicurso

| Notebook | Parte | Contenido |
|---|---|---|
| `00_introduccion` | — | Contexto del problema, dataset, mapa del recorrido |
| `01_eda_frecuentista` | II — EDA básico | Distribución de Sa, sobredispersión, relación con W |
| `01b_eda_general` | II — EDA extendido | Todos los features, selección de variables, Poisson vs NegBin frecuentista |
| `02_mle_datos_simulados` | I — Teoría | GLM Poisson: formulación, MLE manual con `scipy`, verificación con `statsmodels` |
| `03_inferencia_bayesiana` | III — Inferencia | Grid → Metropolis-Hastings → Stan (Poisson + NegBin) |
| `04_predictive_checks_base_models` | IV — PPCs | Posterior Predictive Checks: Poisson vs NegBin, LOO-CV |
| `05_extended_models` | V — Modelos extendidos | ZIP y ZINB en Stan, PPCs y LOO-CV de los 4 modelos |

**Nota de lectura:** El notebook `02` (base teórica) puede leerse antes o después de los
notebooks de EDA. Los notebooks `01/01b → 03 → 04 → 05` forman una secuencia lineal.

## Dataset

**Horseshoe Crab Satellites** (Agresti 2002): n=173 hembras de cangrejo herradura.

| Variable | Descripción |
|---|---|
| `Sa` | Número de satélites (conteo; variable respuesta) |
| `W` | Ancho de caparazón en cm (predictor principal) |
| `Wt` | Peso en kg (alta colinealidad con W) |
| `C` | Color del caparazón (ordinal 1–4) |
| `S` | Condición de la espina (ordinal 1–3) |

## Modelos Stan

```
models/
├── poisson_model.stan          # GLM Poisson
├── negative_binomial_model.stan # GLM Binomial Negativa
├── zip_model.stan              # Zero-Inflated Poisson
└── zinb_model.stan             # Zero-Inflated Binomial Negativa
```

## Stack

- **Inferencia bayesiana**: `cmdstanpy`, Stan
- **Análisis y diagnósticos**: `arviz`, `xarray`
- **Frecuentista / referencia**: `statsmodels`, `scipy`
- **Python**: 3.11 (ver `.python-version`)

## Cómo ejecutar

```bash
uv sync
uv run jupyter notebook notebooks/
```

Los modelos Stan se compilan automáticamente en la primera ejecución.
Los outputs MCMC (`.nc`) se generan ejecutando `03_inferencia_bayesiana.ipynb`
y se reutilizan en los notebooks `04` y `05`.

---

## Referencias

- Agresti, A. (2002). *Categorical Data Analysis*, 2nd ed. Wiley.
- Carlin, B. P. & Louis, T. A. (2009). *Bayesian Methods for Data Analysis*, 3rd ed.
- Gamerman, D. & Freitas Lopes, H. (2006). *Markov Chain Monte Carlo*, 2nd ed.
- Gelman, A. et al. (2020). Bayesian Workflow. *arXiv*:2011.01808.
- Gelman, A., Carlin, J. B. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press.
- Martin, O. A., Kumar, R. & Lao, J. (2021). *Bayesian Modeling and Computation in Python*. CRC Press.
- Wedderburn, R. W. M. (1974). Quasi-likelihood functions, generalized linear models, and the Gauss-Newton method. *Biometrika*, 61(3), 439–447.
