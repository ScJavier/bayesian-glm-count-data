import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
import os


OUTPUT_DIR = 'outputs/poisson_simple_output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_style('darkgrid')
np.random.seed(44)


n = 1500
x = np.random.normal(size=n, loc=35, scale=6)
log_x = np.log(x)
y = np.random.poisson(lam=np.exp(1.0 + 0.8 * log_x), size=n)
df = pd.DataFrame({'x':x, 'y':y, 'log_x':log_x})

df['x_cat'] = pd.qcut(df['x'], q=10)

print('Datos simulados (head):')
print(df.head())

print('\nValidación de supuesto de Poisson (Media vs Varianza por grupo):')
# La varianza debería ser similar a la media.
print(df.groupby('x_cat', observed=False).agg(
    conteo=('y', 'count'),
    media_y=('y','mean'),
    varianza_y=('y', 'var')
))

# --- Gráfica 1: Hexbin Plot (Reemplaza al scatterplot) ---
plt.figure(figsize=(10, 6))
# Usamos hexbin para visualizar la densidad de puntos
hb = plt.hexbin(df['x'], df['y'], gridsize=25, cmap='viridis', mincnt=1)
plt.colorbar(hb, label='Cantidad de puntos')
plt.title('Relación X vs Y (Densidad Hexagonal)')
plt.xlabel('Variable X')
plt.ylabel('Conteo Y')

# Guardar Gráfica 1
plot1_path = os.path.join(OUTPUT_DIR, '1_hexbin_densidad.png')
plt.savefig(plot1_path, dpi=300, bbox_inches='tight')
print(f'\nGráfica de hexágonos guardada en: {plot1_path}')
plt.show()


# --- Gráfica 2: Boxplot por categorías (Nuevo) ---
plt.figure(figsize=(12, 6))
# Rotamos las etiquetas del eje X porque los intervalos de qcut son largos
sns.boxplot(data=df, x='x_cat', y='y', palette='viridis')
plt.xticks(rotation=45)
plt.title('Distribución de Y según deciles de X')
plt.xlabel('Deciles de X')
plt.ylabel('Conteo Y')

# Guardar Gráfica 2
plot2_path = os.path.join(OUTPUT_DIR, '2_boxplot_categorias.png')
plt.savefig(plot2_path, dpi=300, bbox_inches='tight')
print(f'Gráfica de boxplots guardada en: {plot2_path}')
plt.show()


# --- 3. Ajuste del Modelo y Guardado ---

print('\n--- Ajustando Modelo Poisson ---')
# La fórmula es correcta. Statsmodels añade intercepto por defecto.
model = smf.poisson(formula="y ~ log_x", data=df)
results = model.fit(disp=0) # disp=0 silencia el output del proceso de optimización

print(results.summary())

# --- Interpretación de Resultados ---
print('\n--- Interpretación ---')
intercepto_estimado = results.params['Intercept']
coef_x_estimado = results.params['log_x']

print(f"Valores reales simulados:    Intercepto = -1.0,  Coeficiente log(X) = 0.8")
print(f"Valores estimados por modelo: Intercepto = {intercepto_estimado:.4f}, Coeficiente X = {coef_x_estimado:.4f}")
print("\nNOTA: Observa que el Intercepto estimado debe estar cerca de 1.0,")
print("y el coeficiente de log(X) cerca de 0.8. ¡El modelo funciona bien!")

# Calcular los Incident Rate Ratios (IRR) - Exponenciar coeficientes
# Esto es más fácil de interpretar: "Por cada unidad que aumenta X, el conteo esperado de Y se multiplica por..."
irr = np.exp(results.params)
print('\nIncident Rate Ratios (IRR - exp(coef)):')
print(irr)

# --- Diagnósticos de Sobredispersión ---
print('\n--- Diagnósticos ---')
phi = np.sum(results.resid_pearson**2) / results.df_resid
print(f'Dispersión (Phi = Chi2/df): {phi:.4f}')
if phi > 1.5:
    print("ADVERTENCIA: Existe sobredispersión (Phi >> 1). Considera Binomial Negativa.")
else:
    print("La dispersión es aceptable para Poisson (cercana a 1).")

# Gráfica de Residuos
plt.figure(figsize=(10, 6))
plt.scatter(results.fittedvalues, results.resid_pearson, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.title('Residuos de Pearson vs Valores Ajustados')
plt.xlabel('Valores Ajustados')
plt.ylabel('Residuos de Pearson')
plot3_path = os.path.join(OUTPUT_DIR, '3_residuos_diagnostico.png')
plt.savefig(plot3_path, dpi=300, bbox_inches='tight')
print(f'Gráfica de residuos guardada en: {plot3_path}')
plt.show()

# --- 4. Guardar Datos y Modelo ---

# Guardar datos CSV
csv_path = os.path.join(OUTPUT_DIR, 'datos_simulados.csv')
df.to_csv(csv_path, index=False)
print(f'\nDatos guardados en: {csv_path}')

# Guardar el modelo ajustado (formato pickle nativo de statsmodels)
model_path = os.path.join(OUTPUT_DIR, 'modelo_poisson_ajustado.pickle')
results.save(model_path)
print(f'Modelo guardado en: {model_path}')
print(f'\nPara cargar el modelo después usa: results = sm.load("{model_path}")')