# Bitácora — Modelos para Datos de Conteo: Un Recorrido Bayesiano

---

## 2026-04-26 — Publicación del recorrido en GitHub Pages

**Qué se hizo:**

- Reorganización narrativa completa del proyecto como recorrido de 5 partes:
  - `00_introduccion`: origen del problema (Kavak), dataset, mapa del recorrido
  - `02_mle_datos_simulados`: GLM Poisson MLE desde cero — log-verosimilitud, Newton-Raphson, IRLS, verificación statsmodels
  - Celdas de transición al final de `01b` (→ inferencia) y `03` (→ PPCs)
  - Gancho quasi-Poisson al final de `05` (Wedderburn 1974)
  - Tabla de conclusiones completada con p-values exactos de todos los modelos
- Configuración de Quarto book (`_quarto.yml`, `index.qmd`, `freeze: auto`)
- Publicación en GitHub Pages: https://ScJavier.github.io/bayesian-glm-count-data/
- CI con GitHub Actions — publica automáticamente en cada push a master
- Repo hecho público en GitHub

**Resultados clave de PPCs (p-values bayesianos):**

| Modelo | std | Dispersión | max | prop. ceros |
|---|---|---|---|---|
| Poisson | p=0 ❌ | p=0 ❌ | p=0.07 ⚠️ | p=0 ❌ |
| NegBin | p=0.89 ✅ | p=0.95 ✅ | p=0.96 ✅ | p=0.09 ⚠️ |
| ZIP | p=0.01 ⚠️ | p=0.01 ❌ | p=0.01 ⚠️ | p=0.51 ✅ |
| ZINB | p=0.64 ✅ | p=0.69 ✅ | p=0.62 ✅ | p=0.53 ✅ |

**Próximos pasos:**
- El recorrido está publicado como v1. Puede iterarse con feedback.

---

## 2026-04-04 — Restructura y nuevo feature: PPCs de sobredispersión

**Qué se hizo:**
- Restructura completa del proyecto para reflejar el objetivo más general: Bayesian workflow incremental para datos de conteo
- Nueva estructura: data/, models/, notebooks/ (numerados), scripts/, outputs/
- Modelos Stan actualizados con `generated quantities` (y_rep + log_lik) — necesario para PPCs reales
- Celdas de guardado de InferenceData agregadas al notebook de inferencia
- 04_diagnosticos_estudio identificado como ejercicios del libro *BAP* (Osvaldo Martin)
- Git inicializado, primer commit

**Pendiente / próximos pasos:**
- [ ] Reejecutar `03_inferencia_bayesiana.ipynb` para regenerar `.nc` con y_rep y log_lik
- [ ] Completar `05_ppc_sobredispersion.ipynb` — PPCs y métricas de sobredispersión

**Notas:**
- Los `.nc` existentes en outputs/ son de versiones anteriores sin y_rep — deben regenerarse
- 04_diagnosticos_estudio usa pymc3 (no disponible en el entorno); las secciones 2E6-2E7 sí funcionan
- Proyecto renombrado a `bayesian-glm-count-data` (2026-04-04)

---
