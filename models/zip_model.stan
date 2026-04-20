data {
  int<lower=0> N;
  vector[N] x;               // predictor escalado (W_scaled)
  array[N] int<lower=0> y;
}

parameters {
  real alpha_count;          // intercepto componente de conteo
  real beta_count;           // pendiente componente de conteo
  real alpha_zero;           // intercepto componente de ceros
  real beta_zero;            // pendiente componente de ceros
}

model {
  alpha_count ~ normal(0, 10);
  beta_count  ~ normal(0, 10);
  alpha_zero  ~ normal(0, 10);
  beta_zero   ~ normal(0, 10);

  for (n in 1:N) {
    real lambda = exp(alpha_count + beta_count * x[n]);
    real theta  = inv_logit(alpha_zero + beta_zero * x[n]);  // P(cero estructural)

    if (y[n] == 0) {
      target += log_sum_exp(
        log(theta),
        log1m(theta) + poisson_lpmf(0 | lambda)
      );
    } else {
      target += log1m(theta) + poisson_lpmf(y[n] | lambda);
    }
  }
}

generated quantities {
  array[N] int y_rep;
  vector[N] log_lik;

  for (n in 1:N) {
    real lambda = exp(alpha_count + beta_count * x[n]);
    real theta  = inv_logit(alpha_zero + beta_zero * x[n]);

    y_rep[n] = bernoulli_rng(theta) ? 0 : poisson_rng(lambda);

    if (y[n] == 0) {
      log_lik[n] = log_sum_exp(
        log(theta),
        log1m(theta) + poisson_lpmf(0 | lambda)
      );
    } else {
      log_lik[n] = log1m(theta) + poisson_lpmf(y[n] | lambda);
    }
  }
}
