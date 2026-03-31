from math import isclose

def extractability(ev_model: float, expected_slippage: float, consistency: float) -> tuple[float,float,float]:
    if isclose(ev_model, 0.0):
        return 0.0, 0.0, 0.0
    c = max(consistency, 0.0)
    sl_adj = expected_slippage
    if c < 0.15:  # toxic-liquidity penalty
        sl_adj = expected_slippage / c * (1/c)**1.5
    es = 1 - (sl_adj / ev_model)
    ev_adj = ev_model * es
    return es, ev_adj, sl_adj

def sizing_bucket(es: float) -> str:
    if es > 0.7: return "full"
    if es >= 0.4: return "reduced"
    return "skip"