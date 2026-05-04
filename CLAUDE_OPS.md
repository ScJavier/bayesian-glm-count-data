# Claude Ops — Modelos para Datos de Conteo: Un Recorrido Bayesiano
_Archivo de gestión interna. Actualizado por Claude Code._

---

## Estado actual (2026-05-04)

- **Git:** ✅ rama master
- **Remotes:**
  - `origin` → github.com/ScJavier/bayesian-glm-count-data-dev (**PRIVADO** — trabajo diario)
  - `public` → github.com/ScJavier/bayesian-glm-count-data (**PÚBLICO** — contenido graduado)
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

# 1. Graduar código al repo público (rama main)
git push public master:main

# 2. Publicar sitio — quarto publica a origin/gh-pages (privado) primero
QUARTO_PYTHON=.venv/bin/python quarto publish gh-pages --no-browser

# 3. Copiar gh-pages al repo público
git push public gh-pages --force
```

**Por qué 3 pasos:** quarto usa `origin` (repo privado) para el check de gh-pages.
Publica allí correctamente, y luego se copia a `public/gh-pages` donde vive el sitio real.
El sitio en `https://ScJavier.github.io/bayesian-glm-count-data/` se actualiza desde `public/gh-pages`.

### Re-ejecutar notebooks cuando cambie código Python/Stan o texto

```bash
cd /home/javolet/documents/bayesian-glm-count-data
# 1. Cambiar freeze a auto para que --execute funcione
sed -i 's/freeze: true/freeze: auto/' _quarto.yml
# 2. Re-ejecutar
QUARTO_PYTHON=.venv/bin/python quarto render --execute
# 3. Volver freeze a true
sed -i 's/freeze: auto/freeze: true/' _quarto.yml
# 4. Commit y push
git add _freeze/ notebooks/ _quarto.yml
git commit -m "Re-ejecutar notebooks: <descripción>"
git push
# 5. Publicar
QUARTO_PYTHON=.venv/bin/python quarto publish gh-pages --no-browser
```

⚠️ `freeze: true` hace que `--execute` no funcione a nivel de proyecto. Hay que
cambiar a `freeze: auto` antes de re-ejecutar y volver a `freeze: true` después.

⚠️ Usar `.venv/bin/python` (NO `python3`) — el jupyter del venv tiene shebang incorrecto
(apunta a `poisson-reg-example`), pero Quarto con `python` sí encuentra el kernel correcto.

### Outputs MCMC

Los archivos `.nc` (InferenceData) están en `outputs/` (gitignored).
El notebook `03_inferencia_bayesiana.ipynb` los regenera. Notebooks 04 y 05 los cargan.
Si los `.nc` no existen, notebook 05 tiene fallback para ajustar con Stan.

### Flujo de desarrollo (el usuario edita, Claude ejecuta el resto)

El usuario trabaja en Jupyter. Claude Code se encarga de git, freeze y publicación.

**Cambio pequeño (fix, typo, narrativa sin código nuevo):**
```bash
# No requiere re-ejecutar — solo commit y push a privado
git add notebooks/<archivo>.ipynb
git commit -m "fix: descripción"
git push
# Si se quiere publicar: ver sección "Publicar a GitHub Pages"
```

**Cambio con código nuevo o modificado (nueva celda, gráfica, modelo):**
```bash
# 1. Crear rama (para cambios grandes o exploratorios)
git checkout -b feature/descripcion-corta

# 2. El usuario ejecuta las celdas en Jupyter

# 3. Actualizar _freeze/ con los outputs nuevos
sed -i 's/freeze: true/freeze: auto/' _quarto.yml
QUARTO_PYTHON=.venv/bin/python quarto render --execute
sed -i 's/freeze: auto/freeze: true/' _quarto.yml

# 4. Commit y merge
git add notebooks/<archivo>.ipynb _freeze/ _quarto.yml
git commit -m "feat: descripción"
git checkout master && git merge feature/descripcion-corta
git push

# 5. Publicar cuando esté listo (ver sección de publicación)
```

**Cuándo usar feature branch vs. commit directo en master:**
- Feature branch: cambio grande, exploración que puede no llegar a nada, tarda varios días
- Directo en master: fix puntual, typo, cambio de narrativa sin tocar código

### Reglas de desarrollo

- Cada variación de modelo Stan = nuevo archivo `.stan` (nunca modificar el original)
- nbstripout activo: outputs de notebooks se limpian en cada commit
- `_freeze/` SÍ va al repo (referencia del último render, pero no lo usa CI)
- `_site/` NO va al repo (se regenera en cada render/publish)

---

## Backlog

Ver [BACKLOG.md](BACKLOG.md) — tareas organizadas en 5 fases (bugs, narrativa, cosmético, V2).

---

## Arquitectura de repos (configurado 2026-05-03)

| Remote | Repo | Visibilidad | Rama | Uso |
|---|---|---|---|---|
| `origin` | bayesian-glm-count-data-dev | Privado | `master` | Trabajo diario — `git push` normal |
| `public` | bayesian-glm-count-data | Público | `main` | Solo contenido graduado |
| — | — | Público | `gh-pages` | Sitio renderizado (HTML) |

**Archivos excluidos del repo público** (en `.gitignore` de la rama `main`):
`CLAUDE_OPS.md`, `BACKLOG.md`, `briefing_*.md`

**Repo público tiene historial limpio:** 1 solo commit (rama `main` es orphan, sin historia previa).

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

### 2026-05-04 (project-check)
- Revisión de estado: git limpio, entorno uv OK, sitio publicado
- CLAUDE_OPS.md actualizado

### 2026-05-03 (revisión de calidad)
- Feedback a fondo recibido: 7 bugs/typos críticos identificados en NB01, NB03, NB04
- Decisión de arquitectura: repo privado (sucio) → repo público (graduado)
- BACKLOG.md creado con 5 fases de trabajo
- CLAUDE_OPS.md actualizado con arquitectura de repos

### 2026-05-02 (fix outputs)
- Diagnóstico: CI produce HTML sin outputs por interacción nbstripout + Quarto freeze
- Fix: CI cambiado a validate-only; publicación manual con `quarto publish gh-pages`
- `quarto publish gh-pages --no-browser` publicó HTML correcto con todos los outputs
