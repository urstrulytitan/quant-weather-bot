import asyncio, time
from infra.redis_client import redis
from infra.pg import pg_log
from config import settings
from core import signal, extractability, hsdc, orderbook, classifier, ssp, elasticity, sizing, execution, risk, gks

async def process_market(market):
    # Pull inputs (model prob, market price, expected slippage, vols, etc.)
    p_model, p_market = await market.fetch_probs()
    ev = signal.ev_model(p_model, p_market)
    if ev == 0: return
    c_market, c_regime, c_global = await market.consistency_inputs()
    C = hsdc.consistency(c_market, c_regime, c_global)
    es, ev_adj, sl_adj = extractability.extractability(ev, market.expected_slippage(), C)
    bucket = extractability.sizing_bucket(es)
    if bucket == "skip": return
    snaps = await market.get_ob_snapshots()
    feats = orderbook.compute_features(snaps)
    state = classifier.classify(feats.get("persistence",0), C, feats.get("depth_slope",0), feats.get("flicker",0))
    psi_raw = ssp.psi(feats.get("spread_velocity",0), feats.get("imbalance",0), feats.get("flicker",0))
    psi_adj = elasticity.elasticity(abs(p_model-p_market), settings.max_conviction, psi_raw)
    s_target = sizing.target_size(settings.s_max, ev_adj, psi_adj)
    pos = await market.position()
    delta = execution.compute_delta(s_target, pos, settings.min_trade_size)
    # enforce hysteresis & cooldown handled in market methods
    # RDG / RRP
    mult = risk.rdg_multiplier(market.drawdown())
    if mult == 0: return  # stop regime
    s_target *= mult
    # GKS
    g = gks.gks(market.s_slippage(), 1-es, psi_raw, market.fill_score())
    g_state = gks.gks_state(g)
    await market.apply_gks(g_state)
    # Shadow execution only
    await market.shadow_intent(delta, psi_adj, g_state)
    # Logging
    await pg_log("executions_shadow", dict(ts=time.time(), market=market.id, ev=ev, ev_adj=ev_adj,
                                           es=es, sl_exp=market.expected_slippage(), sl_real=None,
                                           psi=psi_raw, psi_adj=psi_adj, gks=g, state=state,
                                           decision=delta))
async def main():
    markets = await load_markets()
    while True:
        tasks = [process_market(m) for m in markets]
        await asyncio.gather(*tasks)
        await asyncio.sleep(0.15)  # minimum heartbeat; per-market overrides inside process_market

if __name__ == "__main__":
    asyncio.run(main())