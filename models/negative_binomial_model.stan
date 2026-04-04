data {
  int<lower=0> N;
  vector[N] x;
  array[N] int<lower=0> y;
}

parameters {
  real alpha;             // Intercepto
  real beta;              // Pendiente
  real<lower=0> phi;      // Parámetro de precisión (dispersión inversa)
}

model {
  // Priors débilmente informativos
  alpha ~ normal(0, 10);
  beta ~ normal(0, 10);
  phi ~ normal(0, 10);

  // Verosimilitud: Binomial Negativa tipo 2 con liga log
  // y ~ neg_binomial_2(exp(alpha + beta * x), phi)
  y ~ neg_binomial_2_log(alpha + beta * x, phi);
}

generated quantities {
  real alpha_sm = 1.0 / phi;  // alpha de statsmodels para comparar directamente
  array[N] int y_rep;
  vector[N] log_lik;
  for (n in 1:N) {
    y_rep[n] = neg_binomial_2_log_rng(alpha + beta * x[n], phi);
    log_lik[n] = neg_binomial_2_log_lpmf(y[n] | alpha + beta * x[n], phi);
  }
}