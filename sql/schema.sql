CREATE TABLE executions_shadow (
  id SERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  market_id TEXT, ev_model NUMERIC, ev_adj NUMERIC,
  es_pred NUMERIC, slippage_exp NUMERIC, slippage_real NUMERIC,
  psi NUMERIC, psi_adj NUMERIC,
  gks_short NUMERIC, gks_long NUMERIC, gks_combined NUMERIC,
  state TEXT, decision NUMERIC, outcome JSONB
);

CREATE TABLE orderbook_snapshots (
  id SERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  market_id TEXT,
  snapshot JSONB
);

CREATE TABLE gks_metrics (
  id SERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  gks NUMERIC, state TEXT,
  s_slippage NUMERIC, s_es NUMERIC, s_ssp NUMERIC, s_fill NUMERIC
);

CREATE TABLE ssp_events (
  id SERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  market_id TEXT,
  omega NUMERIC, imbalance NUMERIC, flicker NUMERIC, psi NUMERIC
);