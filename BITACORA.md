# Bitácora — Bayesian Workflow para Datos de Conteo

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
- El nombre del folder `poisson-reg-example` es demasiado estrecho para el scope actual — pendiente de renombrar

---
