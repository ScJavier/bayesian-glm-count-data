# Bayesian Workflow para Datos de Conteo

Exploración incremental del workflow bayesiano (Gelman et al. 2020) aplicado a regresiones para datos de conteo: GLMs Poisson, Binomial Negativa y sus extensiones.

## Objetivo

Construir una base de referencia progresiva que cubra cada etapa del workflow bayesiano para modelos de conteo:
- EDA y línea base frecuentista
- Prior predictive checks
- Inferencia bayesiana (Grid → MCMC manual → Stan/HMC)
- Diagnósticos numéricos (R-hat, ESS, divergencias)
- Posterior Predictive Checks (PPCs) y evaluación de sobredispersión
- Comparación y expansión de modelos

## Estructura

```
poisson-reg-example/
├── data/                  # Datasets
├── models/                # Modelos Stan (.stan)
├── notebooks/             # Análisis documentados (numerados por etapa)
│   ├── 01_eda_frecuentista.ipynb         — EDA + Poisson/NegBin frecuentista
│   ├── 02_simulacion_distribucion.ipynb  — Simulación y visualización Poisson
│   ├── 03_inferencia_bayesiana.ipynb     — Grid → MH → Stan (Poisson + NegBin)
│   ├── 04_diagnosticos_estudio.ipynb     — Ejercicios BAP book (diagnósticos MCMC)
│   └── 05_ppc_sobredispersion.ipynb      — PPCs y métricas de sobredispersión
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
source .venv/bin/activate

# Ejecutar notebooks en orden
jupyter notebook notebooks/
```

> Los modelos Stan en `models/` requieren compilación la primera vez (automática via cmdstanpy).
> Los outputs MCMC (`.nc`) se regeneran ejecutando `03_inferencia_bayesiana.ipynb`.
