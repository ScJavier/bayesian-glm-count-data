# Claude Ops — Modelos para Datos de Conteo: Un Recorrido Bayesiano
_Archivo de gestión interna. Actualizado por Claude Code._

---

## Estado actual (2026-05-02)

- **Git:** ✅ rama master
- **GitHub:** ✅ github.com/ScJavier/bayesian-glm-count-data (**PÚBLICO desde 2026-04-26**)
- **GitHub Pages:** ✅ https://ScJavier.github.io/bayesian-glm-count-data/
- **Entorno:** uv ✅ (`pyproject.toml` + `uv.lock`), Python 3.11.15
- **Kernel Jupyter:** `bayesian-glm-count-data` registrado en `~/.local/share/jupyter/kernels/`
- **Quarto:** ✅ configurado (`_quarto.yml`, `index.qmd`), `freeze: true`
- **CI:** ✅ GitHub Actions — solo valida, NO publica (ver razón abajo)

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

### ⚠️ Por qué la publicación es MANUAL (no CI)

El CI (`quarto render`) produce HTML sin outputs porque:
1. nbstripout limpia los notebooks al hacer `git add` → git almacena notebooks sin outputs
2. CI recibe notebooks sin outputs y el mecanismo de freeze de Quarto no bypassa el
   hash check en la práctica (aunque `freeze: true` está configurado)
3. `quarto publish gh-pages` desde **local** sí funciona porque Quarto escribe los
   outputs de vuelta en los notebooks durante `--execute`, y el publish usa esos outputs

**Consecuencia:** publicar siempre desde local con el comando de abajo.

### Publicar a GitHub Pages (comando principal)

```bash
cd /home/javolet/documents/bayesian-glm-count-data
QUARTO_PYTHON=.venv/bin/python quarto publish gh-pages --no-browser
```

Esto hace render (con outputs) y publica directamente a gh-pages. No requiere
commit previo — el sitio queda actualizado en minutos.

### Re-ejecutar notebooks cuando cambie código Python/Stan

```bash
cd /home/javolet/documents/bayesian-glm-count-data
QUARTO_PYTHON=.venv/bin/python quarto render --execute
git add _freeze/ notebooks/
git commit -m "Re-ejecutar notebooks: <descripción>"
git push
# Luego publicar:
QUARTO_PYTHON=.venv/bin/python quarto publish gh-pages --no-browser
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
- `_freeze/` SÍ va al repo (referencia del último render, pero no lo usa CI)
- `_site/` NO va al repo (se regenera en cada render/publish)

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
- Reorganización como recorrido de 5 partes
- Quarto book configurado, GitHub Pages publicado, CI configurado

### 2026-05-02 (fix outputs)
- Diagnóstico: CI produce HTML sin outputs por interacción nbstripout + Quarto freeze
- Fix: CI cambiado a validate-only; publicación manual con `quarto publish gh-pages`
- `quarto publish gh-pages --no-browser` publicó HTML correcto con todos los outputs
