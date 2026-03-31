CONSISTENCY_FLOOR = 0.15
WEIGHTS = {"market":0.6,"regime":0.3,"global":0.1}

def consistency(c_market: float, c_regime: float, c_global: float) -> float:
    c = (WEIGHTS["market"]*c_market +
         WEIGHTS["regime"]*c_regime +
         WEIGHTS["global"]*c_global)
    return max(c, CONSISTENCY_FLOOR)