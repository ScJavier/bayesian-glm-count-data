data {
  int<lower=0> N;
  vector[N] x;               // predictor escalado (W_scaled)
  array[N] int<lower=0> y;
}

parameters {
  real alpha_count;          // intercepto componente de conteo (NegBin)
  real beta_count;           // pendiente componente de conteo
  real<lower=0> phi;         // precisión NegBin (phi grande → menos sobredispersión)
  real alpha_zero;           // intercepto componente de ceros
  real beta_zero;            // pendiente componente de ceros
}

model {
  alpha_count ~ normal(0, 10);
  beta_count  ~ normal(0, 10);
  phi         ~ exponential(1);   // half-prior: phi>0, media=1, colas ligeras
  alpha_zero  ~ normal(0, 10);
  beta_zero   ~ normal(0, 10);

  for (n in 1:N) {
    real eta   = alpha_count + beta_count * x[n];
    real theta = inv_logit(alpha_zero + beta_zero * x[n]);  // P(cero estructural)

    if (y[n] == 0) {
      target += log_sum_exp(
        log(theta),
        log1m(theta) + neg_binomial_2_log_lpmf(0 | eta, phi)
      );
    } else {
      target += log1m(theta) + neg_binomial_2_log_lpmf(y[n] | eta, phi);
    }
  }
}

generated quantities {
  real alpha_sm = 1.0 / phi;  // equivalente al alpha de statsmodels
  array[N] int y_rep;
  vector[N] log_lik;

  for (n in 1:N) {
    real eta   = alpha_count + beta_count * x[n];
    real theta = inv_logit(alpha_zero + beta_zero * x[n]);

    if (bernoulli_rng(theta)) {
      y_rep[n] = 0;
    } else {
      y_rep[n] = neg_binomial_2_log_rng(eta, phi);
    }

    if (y[n] == 0) {
      log_lik[n] = log_sum_exp(
        log(theta),
        log1m(theta) + neg_binomial_2_log_lpmf(0 | eta, phi)
      );
    } else {
      log_lik[n] = log1m(theta) + neg_binomial_2_log_lpmf(y[n] | eta, phi);
    }
  }
}
