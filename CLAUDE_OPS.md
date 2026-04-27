# Claude Ops — Modelos para Datos de Conteo: Un Recorrido Bayesiano
_Archivo de gestión interna. Actualizado por Claude Code._

---

## Estado actual (2026-04-26)

- **Git:** ✅ rama master
- **GitHub:** ✅ github.com/ScJavier/bayesian-glm-count-data (**PÚBLICO desde 2026-04-26**)
- **GitHub Pages:** ✅ https://ScJavier.github.io/bayesian-glm-count-data/
- **Entorno:** uv ✅ (`pyproject.toml` + `uv.lock`), Python 3.11.15
- **Kernel Jupyter:** `bayesian-glm-count-data` registrado en `~/.local/share/jupyter/kernels/`
- **Quarto:** ✅ configurado (`_quarto.yml`, `index.qmd`), freeze committeado en `_freeze/`
- **CI:** ✅ GitHub Actions en `.github/workflows/publish.yml`

---

## Estructura de notebooks

| Notebook | Parte | Estado |
|---|---|---|
| `00_introduccion.ipynb` | Prefacio | ✅ |
| `01_eda_frecuentista.ipynb` | II — EDA básico | ✅ |
| `01b_eda_general.ipynb` | II — EDA extendido | ✅ |
| `02_mle_datos_simulados.ipynb` | I — Teoría MLE | ✅ |
| `03_inferencia_bayesiana.ipynb` | III — Inferencia Bayesiana | ✅ |
| `04_predictive_checks_base_models.ipynb` | IV — PPCs base | ✅ |
| `05_extended_models.ipynb` | V — ZIP y ZINB | ✅ |

## Modelos Stan

| Modelo | Archivo | generated quantities |
|---|---|---|
| Poisson GLM | `models/poisson_model.stan` | ✅ y_rep + log_lik |
| Binomial Negativa | `models/negative_binomial_model.stan` | ✅ y_rep + log_lik + alpha_sm |
| ZIP | `models/zip_model.stan` | ✅ y_rep + log_lik |
| ZINB | `models/zinb_model.stan` | ✅ y_rep + log_lik + alpha_sm |

---

## Flujo de trabajo

### Publicación (CI automático)

Cada push a `master` activa GitHub Actions:
1. Instala Quarto en ubuntu-latest
2. Corre `quarto render` (usa `_freeze/` — sin ejecutar notebooks)
3. Publica en rama `gh-pages` → GitHub Pages actualiza el sitio

### Re-ejecutar notebooks (cuando cambie código Python/Stan)

```bash
cd /home/javolet/documents/bayesian-glm-count-data
QUARTO_PYTHON=.venv/bin/python quarto render --execute
git add _freeze/ notebooks/
git commit -m "Re-ejecutar notebooks: <descripción>"
git push
```

⚠️ Usar `.venv/bin/python` (NO `python3`) — el jupyter del venv tiene shebang incorrecto
(apunta a `poisson-reg-example`), pero Quarto con `python` sí encuentra el kernel correcto.

### Outputs MCMC

Los archivos `.nc` (InferenceData) están en `outputs/` (gitignored).
El notebook `03_inferencia_bayesiana.ipynb` los regenera. Notebooks 04 y 05 los cargan.
Si los `.nc` no existen, notebook 05 tiene fallback para ajustar con Stan.

### Reglas de desarrollo

- Cada variación de modelo Stan = nuevo archivo `.stan` (nunca modificar el original)
- nbstripout activo: outputs de notebooks se limpian en cada commit
- `_freeze/` SÍ va al repo (es el cache de Quarto para CI)
- `_site/` NO va al repo (se regenera en cada render)

---

## Historial resumido de sesiones

### 2026-04-04
- Restructura completa del proyecto, notebooks numerados, modelos Stan con generated quantities
- git init, GitHub repo creado (privado), kernel Jupyter registrado, nbstripout configurado

### 2026-04-20 (sesión técnica final)
- PPCs completos para Poisson y NegBin (notebook 04)
- Implementación ZIP y ZINB en Stan (notebook 05)
- LOO-CV de 4 modelos
- Notebook 02 (simulación básica) eliminado — reemplazado por scripts

### 2026-04-26 (publicación)
- Reorganización como recorrido de 5 partes:
  - 00 (intro), 02 (MLE desde cero con Newton-Raphson/IRLS), transiciones entre notebooks
  - Tabla PPC completada con p-values exactos (ZIP: solo arregla ceros; ZINB: arregla todo)
  - Gancho quasi-Poisson (Wedderburn 1974) al final de notebook 05
- Quarto book configurado con freeze: auto
- GitHub Pages publicado: https://ScJavier.github.io/bayesian-glm-count-data/
- Repo hecho público
- CI con GitHub Actions configurado (publica automáticamente en push a master)
