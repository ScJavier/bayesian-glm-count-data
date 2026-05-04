# Backlog — bayesian-glm-count-data
_Gestionado por Claude Code. Actualizar al completar cada tarea._

---

## FASE 1 — Bugs y typos ✅ (2026-05-03)

- [x] **NB03** — Título `# Functions` → `## Funciones auxiliares`
- [x] **NB03** — Bug print: segundo `MLE alpha` → `MLE beta`
- [x] **NB03** — Bug: `mean_beta_nb = np.std(...)` → `std_beta_nb`
- [x] **NB03** — Typo `Dianósticos` → `Diagnósticos`
- [x] **NB01** — Bins `'23.25>'`/`'29.25<'` → `'<23.25'`/`'>29.25'`
- [x] **NB01** — `warnings.filterwarnings('ignore')` para suprimir path local
- [x] **NB04** — P-values actualizados con valores reales (0.894, 0.954, 0.968, 0.093)

---

## FASE 2 — Narrativa NB03 ✅ (2026-05-03)

- [x] **Intro bayesiana**: sección completa antes de Grid (posterior, prior, problema de la forma cerrada)
- [x] **Grid → MH**: motivación por escalabilidad (n^k evaluaciones), transición explícita
- [x] **MH → Stan**: dos limitaciones concretas de MH (afinación manual, exploración ineficiente); HMC/NUTS
- [x] **Prior plano**: nota en ambas secciones (Grid y MH usan prior uniforme implícito)

---

## FASE 3 — Narrativa NB01 y fix NB04 ✅ (2026-05-03)

- [x] **NB01** — 3 conectores nuevos: diagnóstico sobredispersión, transición a Poisson, nota antes de NegBin
- [x] **NB04** — P-values actualizados con valores del output almacenado (sin re-ejecutar)

---

## FASE 4 — Cosmético ✅ (2026-05-03)

- [x] **NB01, NB01b, NB02** — `warnings.filterwarnings('ignore')` agregado
- [x] **NB01** — Títulos de plots traducidos al español

---

## FASE 5 — V2 (sin deadline)

- [ ] **NB03** — Prior plano explícito: Grid y MH con `uniform(−∞, ∞)` vs Stan con priors explícitos; comparar formalmente
- [ ] **NB02** — Aclarar dispersión marginal (D≈1.8 en simulación) vs dispersión condicional (φ≈0.96 por Pearson); ambos son correctos pero parecen contradictorios sin explicación
- [ ] **NB01b** — Renombrar NB1/NB2/NB3/NB4 → NB-W, NB-WC, etc. para evitar colisión con nomenclatura técnica NB1 (varianza lineal) vs NB2 (varianza cuadrática)
- [ ] **Mejoras técnicas** (ya en Notion): Score Test de sobredispersión, rootograms, test Cameron-Trivedi para NB1 vs NB2

---

## Workflow de publicación

Este proyecto usa **dos repos**:

- **Repo privado** — fuente de trabajo en sucio (paths locales, warnings, exploración a medias)
- **Repo público** → `github.com/ScJavier/bayesian-glm-count-data` — solo recibe lo que ya pasó el filtro

Implementación pendiente: configurar dos remotes (`origin` privado, `public` público) o flujo de graduación manual. Claude Code puede configurarlo cuando el usuario esté listo.

Publicar a GitHub Pages: `QUARTO_PYTHON=.venv/bin/python quarto publish gh-pages --no-browser` (desde local, no CI — ver CLAUDE_OPS.md).
