import asyncio, time
from infra.redis_client import redis
from infra.pg import pg_log
from config import settings
from core import signal, extractability, hsdc, orderbook, classifier, ssp, elasticity, sizing, execution, risk, gks

# minimal market stub; replace with real adapter for Polymarket-style API
class Market:
    def __init__(self, market_id):
        self.id = market_id
    async def fetch_probs(self):              # return (P_model, P_market)
        return 0.55, 0.50
    async def consistency_inputs(self):
        return 0.6, 0.5, 0.4
    def expected_slippage(self):
        return 0.01
    async def get_ob_snapshots(self):
        return []
    async def position(self):
        return execution.Position(current=0.0, pending=0.0)
    def drawdown(self):
        return 0.0
    def s_slippage(self):
        return 0.1
    def fill_score(self):
        return 0.9
    async def apply_gks(self, state):         # store GKS state if needed
        await redis.set("gks", state)
    async def shadow_intent(self, delta, psi_adj, g_state):
        # No real trades; just log to redis for observability
        await redis.lpush(f"pending:{self.id}", f"{time.time()}|{delta}|{psi_adj}|{g_state}")

async def load_markets():
    # stub: create a few demo markets
    return [Market(f"demo-{i}") for i in range(3)]

async def process_market(market):
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
    mult = risk.rdg_multiplier(market.drawdown())
    if mult == 0: return
    s_target *= mult
    g = gks.gks(market.s_slippage(), 1-es, psi_raw, market.fill_score())
    g_state = gks.gks_state(g)
    await market.apply_gks(g_state)
    await market.shadow_intent(delta, psi_adj, g_state)
    await pg_log("executions_shadow", dict(
        ts=time.time(), market=market.id, ev=ev, ev_adj=ev_adj,
        es=es, sl_exp=market.expected_slippage(), sl_real=None,
        psi=psi_raw, psi_adj=psi_adj, gks=g, state=state,
        decision=delta))

async def main():
    markets = await load_markets()
    while True:
        tasks = [process_market(m) for m in markets]
        await asyncio.gather(*tasks)
        await asyncio.sleep(0.15)

if __name__ == "__main__":
    asyncio.run(main())