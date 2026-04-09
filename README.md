# GLMs para Datos de Conteo — Enfoque Bayesiano

Exploración de regresiones para datos de conteo con Stan: modelos Poisson, Binomial Negativa y sus extensiones. Aplicado al dataset Horseshoe Crab Satellites.

> Para exploración del workflow bayesiano con toy examples, ver [bayesian-workflow-examples](../bayesian-workflow-examples).

## Objetivo

Construir una base de referencia para el análisis bayesiano de datos de conteo:
- EDA y línea base frecuentista (Poisson/NegBin con statsmodels)
- Inferencia bayesiana con Stan (Grid → MCMC manual → HMC)
- Diagnósticos MCMC (R-hat, ESS, divergencias)
- Posterior Predictive Checks (PPCs) y evaluación de sobredispersión
- Comparación Poisson vs NegBin via LOO

## Estructura

```
bayesian-glm-count-data/
├── data/                  # Datasets
├── models/                # Modelos Stan (.stan)
├── notebooks/             # Análisis documentados (numerados por etapa)
│   ├── 01_eda_frecuentista.ipynb         — EDA + Poisson/NegBin frecuentista
│   ├── 02_simulacion_distribucion.ipynb  — Simulación y visualización Poisson
│   ├── 03_inferencia_bayesiana.ipynb     — Grid → MH → Stan (Poisson + NegBin)
│   ├── 04_diagnosticos_estudio.ipynb     — Ejercicios BAP book (diagnósticos MCMC)
│   └── 05_ppc_sobredispersion.ipynb      — PPCs y comparación Poisson vs NegBin
├── scripts/               # Scripts de apoyo / prototipos
└── outputs/               # Archivos generados (gitignored: .nc, plots)
```

## Dataset principal

**Horseshoe Crab Satellites** (Agresti, 1996): n=173 cangrejos hembra.
Variable respuesta: número de satélites (Sa). Predictor: ancho del caparazón (W, cm).
Clásico ejemplo de datos de conteo con sobredispersión.

## Stack

- **Inferencia bayesiana**: `cmdstanpy`, Stan
- **Análisis y diagnósticos**: `arviz`, `xarray`
- **Frecuentista / referencia**: `statsmodels`, `scipy`, `scikit-learn`
- **Python**: 3.11 (ver `.python-version`)

## Cómo ejecutar

```bash
# Activar entorno
uv sync
uv run jupyter notebook notebooks/
```

> Los modelos Stan en `models/` requieren compilación la primera vez (automática via cmdstanpy).
> Los outputs MCMC (`.nc`) se regeneran ejecutando `03_inferencia_bayesiana.ipynb`.

---

## Referencias

### Workflow bayesiano

**Gelman, A., Vehtari, A., Simpson, D., Margossian, C. C., Carpenter, B., Yao, Y., Kennedy, L., Gabry, J., Bürkner, P.-C., & Modrák, M. (2020).** Bayesian workflow. *arXiv preprint*. https://doi.org/10.48550/arXiv.2011.01808
> Referencia principal del proyecto. Describe el workflow completo como ciclo iterativo: prior predictive checks → inferencia → PPCs → expansión de modelos. 77 páginas.

**Gabry, J., Simpson, D., Vehtari, A., Betancourt, M., & Gelman, A. (2019).** Visualization in Bayesian workflow. *Journal of the Royal Statistical Society: Series A*, 182, 389–402. https://doi.org/10.1111/rssa.12378 · arXiv:1709.01449
> Paper operativo: cómo estructurar prior predictive checks, PPCs gráficos, qué visualizaciones usar y cuándo. Es el paper detrás de `bayesplot` — muy recomendable como guía práctica.

**Schad, D. J., Betancourt, M., & Vasishth, S. (2021).** Toward a principled Bayesian workflow in cognitive science. *Psychological Methods*, 26(1), 103–126. https://doi.org/10.1037/met0000275 · arXiv:1904.12765
> Da la secuencia completa como protocolo formal: prior elicitation → prior predictive → fit → PPC → model comparison. Más sistemático que BDA3 como guía paso a paso.

**Gelman, A., & Shalizi, C. R. (2013).** Philosophy and the practice of Bayesian statistics. *British Journal of Mathematical and Statistical Psychology*, 66, 8–38. https://doi.org/10.1111/j.2044-8317.2011.02037.x · arXiv:1006.3868
> Equivalente a BDA3 Ch6 pero argumentado con más claridad filosófica. Discute por qué los modelos bayesianos son hipótesis falsificables y el papel de los PPCs como herramienta de crítica de modelos.

### Textos de referencia

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd ed.). CRC Press.
> BDA3 — texto de referencia fundamental. Capítulo 6: model checking y PPCs.

**Martin, O. A., Kumar, R., & Lao, J. (2021).** *Bayesian Modeling and Computation in Python*. Chapman & Hall/CRC. ISBN: 978-0-367-89436-8. https://bayesiancomputationbook.com
> BAP book. Base del notebook `04_diagnosticos_estudio.ipynb` (ejercicios 2E6-2E7).
