// 1. Bloque de Datos: Definimos lo que el modelo recibe
data {
  int<lower=0> N;              // Número de observaciones (173 en el dataset de cangrejos)
  vector[N] x;                 // Variable independiente (Ancho de la hembra 'W')
  array[N] int<lower=0> y;     // Variable dependiente (Número de satélites 'Sa')
}

// 2. Bloque de Parámetros: Lo que queremos estimar
parameters {
  real alpha;                  // Intercepto
  real beta;                   // Pendiente
}

// 3. Bloque del Modelo: Definimos priors y verosimilitud
model {
  // Priors: Podemos usar distribuciones normales débilmente informativas
  // Esto ayuda a la estabilidad numérica comparado con las uniformes
  alpha ~ normal(0, 10);
  beta ~ normal(0, 10);

  // Verosimilitud (Likelihood)
  // poisson_log(x) es equivalente a poisson(exp(x))
  // Esto es más estable numéricamente que calcular exp() manualmente
  y ~ poisson_log(alpha + beta * x);
}

generated quantities {
  array[N] int y_rep;
  vector[N] log_lik;
  for (n in 1:N) {
    y_rep[n] = poisson_log_rng(alpha + beta * x[n]);
    log_lik[n] = poisson_log_lpmf(y[n] | alpha + beta * x[n]);
  }
}