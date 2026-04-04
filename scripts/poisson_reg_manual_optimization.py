import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize

# Configuración
np.random.seed(44)
n = 1500

# --- 1. Simulación de Datos ---
# Usamos la configuración LogNormal solicitada previamente
mu_log, sigma_log = 3.5, 0.25
x = np.random.lognormal(mean=mu_log, sigma=sigma_log, size=n)

# Parámetros reales
beta_0_real = -1.0
beta_1_real = 0.8

# Generación de Y
# Modelo: log(lambda) = beta0 + beta1 * log(x)
lam = np.exp(beta_0_real + beta_1_real * np.log(x))
y = np.random.poisson(lam=lam, size=n)

print(f"Datos simulados: n={n}")
print(f"Parámetros reales: Intercepto={beta_0_real}, Coeficiente={beta_1_real}")

# --- 2. Preparación de Datos para Optimización ---
# Variable independiente: log(x)
# Matriz de diseño X: columna de 1s (intercepto) y columna log(x)
X = np.column_stack([np.ones(n), np.log(x)])

# --- 3. Definición de Funciones (Log-Likelihood, Gradiente, Hessiana) ---

def poisson_nll(beta, X, y):
    """
    Negativo de la Log-Verosimilitud (Negative Log-Likelihood).
    LL(beta) = sum( y_i * x_i'beta - exp(x_i'beta) - log(y_i!) )
    Minimizamos -LL. Omitimos log(y_i!) ya que es constante respecto a beta.
    """
    mu = np.exp(np.dot(X, beta))
    ll = np.sum(y * np.dot(X, beta) - mu)
    return -ll

def poisson_gradient(beta, X, y):
    """
    Gradiente del NLL.
    d(-LL)/dbeta = - sum( (y_i - mu_i) * x_i )
    = - X.T @ (y - mu)
    """
    mu = np.exp(np.dot(X, beta))
    grad = -np.dot(X.T, y - mu)
    return grad

def poisson_hessian(beta, X, y):
    """
    Hessiana del NLL.
    d^2(-LL)/dbeta^2 = X.T @ W @ X
    donde W = diag(mu)
    """
    mu = np.exp(np.dot(X, beta))
    # Forma eficiente de calcular X.T @ diag(mu) @ X
    # Multiplicamos cada fila de X por mu correspondiente (broadcasting)
    # luego multiplicamos por X
    H = np.dot(X.T * mu, X)
    return H

# --- 4. Optimización Numérica ---
print("\nOptimizando...")
beta_init = np.zeros(X.shape[1]) # Inicialización en 0

res = minimize(
    fun=poisson_nll,
    x0=beta_init,
    args=(X, y),
    method='Newton-CG', # Newton-CG usa la Hessiana exacta o aproximada, es robusto
    jac=poisson_gradient,
    hess=poisson_hessian
)

if not res.success:
    print("Error en optimización:", res.message)
else:
    print("Optimización exitosa.")

beta_est = res.x

# --- 5. Cálculos de Inferencia ---

# Matriz de Covarianza = Inversa de la Hessiana (Información de Fisher)
# Evaluada en los parámetros estimados
H = poisson_hessian(beta_est, X, y)
cov_matrix = np.linalg.inv(H)

# Errores Estándar
se = np.sqrt(np.diag(cov_matrix))

# Estadístico t (z-score)
t_stat = beta_est / se

# P-values (dos colas)
p_values = 2 * (1 - stats.norm.cdf(np.abs(t_stat)))

# Intervalos de Confianza 95%
z_crit = stats.norm.ppf(0.975)
ci_lower = beta_est - z_crit * se
ci_upper = beta_est + z_crit * se

# --- 6. Prueba LLR vs Modelo Nulo ---

# Modelo Nulo (solo intercepto)
# La estimación ML para lambda constante es la media de y
mu_null = np.mean(y)
ll_null = np.sum(y * np.log(mu_null) - mu_null)

# Log-Likelihood del modelo completo
# Calculamos el valor real incluyendo los términos dependientes de beta
# (Nota: poisson_nll devuelve el negativo sin el factorial, invertimos el signo)
ll_model = -poisson_nll(beta_est, X, y)

# Estadístico LLR (Deviance)
llr = 2 * (ll_model - ll_null)
df_model = X.shape[1]
df_null = 1
p_value_llr = 1 - stats.chi2.cdf(llr, df_model - df_null)


# --- 7. Impresión de Resultados ---
print("\n" + "="*75)
print(f"{'RESULTADOS DE REGRESIÓN POISSON (SCIPY OPTIMIZE)':^75}")
print("="*75)
print(f"{'Variable':<15} {'Coef.':>10} {'Std.Err.':>10} {'z':>10} {'P>|z|':>10} {'[0.025':>10} {'0.975]':>10}")
print("-" * 75)

var_names = ['Intercepto', 'log(x)']
for i, name in enumerate(var_names):
    print(f"{name:<15} {beta_est[i]:10.4f} {se[i]:10.4f} {t_stat[i]:10.4f} {p_values[i]:10.4f} {ci_lower[i]:10.4f} {ci_upper[i]:10.4f}")

print("-" * 75)
print(f"Log-Likelihood Modelo: {ll_model:.4f}")
print(f"Log-Likelihood Nulo:   {ll_null:.4f}")
print(f"LLR p-value:           {p_value_llr:.4e}")
print("="*75)