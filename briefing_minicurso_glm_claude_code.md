# Briefing para Claude Code — Minicurso: Modelos para Datos de Conteo

## Contexto del proyecto

Este repositorio contiene un **minicurso de modelos para datos de conteo** que documenta un recorrido intelectual genuino, no un tutorial diseñado desde cero. El enfoque es mostrar el proceso de pensamiento mientras se estudia y aplica — la marca de un methodological researcher.

### Origen real

Todo empezó con un problema aplicado en Kavak: predecir ventas usando regresión de Poisson. La Poisson no bastó (sobredispersión), lo cual llevó a explorar Negative Binomial. El estudio sistemático del libro de Agresti (*Categorical Data Analysis*) usando el dataset Horseshoe Crab Satellites fue el vehículo. De ahí la exploración se expandió naturalmente:

1. MLE desde cero para Poisson y NegBin (datos simulados con ground truth conocido)
2. Verificación con `statsmodels`
3. EDA con datos reales — sobredispersión, exceso de ceros, selección de features
4. Conexión con el enfoque bayesiano (falta de experiencia aplicada propia)
5. Ajuste en grid (inspirado por Carlin & Louis / Gamerman & Freitas, visto en clase de Análisis Bayesiano)
6. Refresco de MCMC con Metropolis-Hastings
7. Implementación en Stan (CmdStanPy)
8. PPCs como herramienta de diagnóstico de adecuación del modelo
9. LOO-CV y LOO-PIT (inspirado por Martin, Kumar & Lao 2021, Cap. 3)
10. Extensión a modelos Zero-Inflated (ZIP, ZINB) — motivada por el exceso de ~33% de ceros

El workflow bayesiano (Gelman et al. 2020) fue descubierto *durante* el proceso, no como punto de partida.

## Estructura del minicurso (5 partes)

### Parte I — Teoría con datos simulados
- Implementación desde cero: GLM Poisson y NegBin por MLE
- Optimización custom de la log-verosimilitud
- Verificación con `statsmodels`
- Propósito: mostrar que la teoría funciona cuando los datos se portan bien (ground truth conocido)
- **Estado**: scripts Python existentes. Decisión pendiente: ¿notebook introductorio `00_` o apéndice referenciado?

### Parte II — EDA con datos reales
- `01_eda_frecuentista.ipynb`: distribución de `Sa`, sobredispersión (D≈3.38), relación con `W`, modelos base Poisson vs NegBin
- `01b_eda_general.ipynb`: EDA extendido (todos los features), heatmap, LOWESS, 4+4 modelos frecuentistas
- Conclusión: `Wt` colineal con `W` (redundante), `C`/`S` relación inversa débil; BIC favorece `Sa ~ W`
- **Estado**: completos. La inclusión de 01b se justifica porque así fue el proceso real de exploración (¿cómo descartar features con enfoque frecuentista vs bayesiano?)

### Parte III — Inferencia Bayesiana
- Progresión: Grid → Metropolis-Hastings desde cero → Stan (CmdStanPy)
- Modelos: Poisson y NegBin con predictor `W`
- La progresión Grid → MH → Stan es un diferenciador, no un lastre: muestra el razonamiento, no solo la herramienta
- **Estado**: existe. Cada método debe motivar el siguiente por una limitación concreta.

### Parte IV — Posterior Predictive Checks (modelos base)
- PPCs para Poisson y NegBin: densidad, estadísticos de prueba (media, std, dispersión, prop. ceros)
- p-values bayesianos: Poisson falla (p≈0); NegBin corrige dispersión pero prop_zeros borderline (p=0.096)
- LOO-CV: NegBin ELPD=-378.5 vs Poisson -465.4 (diff=86.8 ±17.3 SE)
- Narrativa: NegBin mejor pero ceros siguen siendo problema → motiva expansión
- **Estado**: completo y funcional

### Parte V — Modelos extendidos: ZIP y ZINB
- Implementación Stan de ZIP y ZINB
- PPCs lado a lado (4 modelos)
- Test statistics: prop_zeros — ZIP p=0.514, ZINB p=0.532 (resuelven el problema)
- LOO-CV progresión clara: Poisson → NegBin → ZIP → ZINB
- Visualización del componente zero-inflation en función de `W`
- **Estado**: completo y funcional

## Tareas para la publicación v1 (deadline: 30 abril 2026)

La consigna es **imperfecto pero publicado**. No es un producto final — es una v1 que puede iterarse.

1. **Renumerar/reordenar notebooks**: la secuencia actual es 01, 01b, 03, 04, 05 (no hay 02). Renumerar para que refleje las partes del tutorial. Propuesta: 00 (intro), 01 (EDA), 02 (simulación/MLE), 03 (bayesiano), 04 (PPCs), 05 (ZIP/ZINB).
2. **Notebook introductorio `00_`**: breve. Contexto del problema (horseshoe crabs, 2-3 párrafos), pregunta de investigación explícita, mapa del recorrido ("vamos a hacer esto en 5 partes porque..."), mención de que el origen fue un problema real de negocio. No más de una página renderizada.
3. **Narrativa de transición entre partes**: cada notebook debe terminar motivando el siguiente. Una celda markdown de cierre: "esto nos dejó con esta pregunta abierta, que atacamos en el siguiente notebook." Revisar especialmente las transiciones 01b→03 y 03→04.
4. **README actualizado**: índice del minicurso con descripción de cada parte, dataset, referencias clave, y una nota sobre el enfoque (proceso genuino de estudio, no tutorial pre-diseñado).
5. **Gancho al final del notebook 05**: mención del quasi-binomial como extensión para tasas de conversión y conexión con causalidad/DoubleML. Solo un párrafo — no desarrollar.
6. **Publicar en GitHub Pages** (nbconvert o Quarto).

## Decisiones de enfoque ya tomadas

- **Es un minicurso, no un tutorial de PPCs bayesianos.** El alcance es modelos para datos de conteo con comparación de paradigmas frecuentista y bayesiano.
- **El EDA frecuentista extendido (01b) se incluye** porque refleja el proceso real de exploración y la pregunta legítima de cómo descartar features.
- **La progresión Grid → MH → Stan se mantiene** como diferenciador pedagógico.
- **El quasi-binomial queda fuera** del minicurso — se menciona solo como gancho narrativo al final.
- **El tono es de proceso genuino**: "me surgió esta duda y fui a explorar qué pasa cuando..." No un tutorial pulido que simula que todo se sabía de antemano.

## Referencias clave

- Agresti (2002/2013) — *Categorical Data Analysis*
- Carlin & Louis (2009) — *Bayesian Methods for Data Analysis*
- Gamerman & Freitas (2006) — *Markov Chain Monte Carlo*
- Gelman et al. (2020) — *Bayesian Workflow*
- Martin, Kumar & Lao (2021) — *Bayesian Modeling and Computation in Python*, Cap. 3

## Dataset

**Horseshoe Crab Satellites** (Agresti 2002): número de satélites (`Sa`) en función de características morfológicas del cangrejo herradura hembra (peso `W`, ancho `Wt`, color `C`, espina `S`). Sobredispersión D≈3.38, exceso de ceros ~33%.

---

## Apéndice: Conexión con trabajo aplicado — ZINB jerárquico para retail (hackathon Kavak, abril 2026)

> **Nota**: Esta sección documenta una conexión emergente entre el minicurso y un problema real. No forma parte del minicurso publicado — es un gancho para una posible expansión o especialización futura.

### Contexto

Durante un hackathon de ML en pricing (abril 2026), se identificó que los modelos de compras del sistema de pricing de Kavak presentaban un problema de exceso de ceros en los datos. La conexión fue inmediata: las distribuciones Zero-Inflated estudiadas el fin de semana previo para la Parte V del minicurso eran directamente aplicables.

### Enfoque explorado

- **ZINB jerárquico** para modelar la dependencia entre celdas (combinaciones de marca/modelo/año/mercado) en datos de retail de alta dimensión
- La estructura jerárquica captura la variabilidad inter-celda que un modelo flat no resuelve
- El componente zero-inflation modela las celdas sin transacciones (la mayoría en mercados con inventario disperso)

### Status

Enfoque prometedor pero en fase exploratoria. Requiere investigación adicional sobre:
- Escalabilidad del ZINB jerárquico a la dimensionalidad real del catálogo (~miles de celdas activas × 6 países)
- Comparación contra el baseline actual (modelos agregados sin estructura de ceros)
- Viabilidad de implementación en producción (Stan vs alternativas más rápidas)

### Posibles líneas de expansión

- **Minicurso II**: extensión a GLMs multivariados para datos escasos en retail (ya documentado en Notion como idea: "GLMs multivariados para datos escasos")
- **Charla Data Pub CDMX**: presentación del sistema de precios de mercado, con el enfoque de zero-inflation como caso de innovación metodológica
- **Artículo técnico**: ZINB jerárquico como solución a la "maldición de los ceros" en pricing algorítmico de marketplaces

---

*Documento generado el 26 de abril de 2026. Para contexto completo del proyecto, consultar la página de Notion: Portafolio | Seguimiento — Methodological Researcher.*
