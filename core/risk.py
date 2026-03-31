def rdg_multiplier(drawdown_pct):
    if drawdown_pct < 0.4: return 1.0
    if drawdown_pct < 0.7: return 0.6
    if drawdown_pct < 1.0: return 0.3
    return 0.0  # stop trading regime

def rrp_state(divergence, shadow_pnl, samples, current):
    if current == "LOCKED":
        if divergence < 0.08 and shadow_pnl > 0 and samples >= 30:
            return "OBSERVATION"
        return "LOCKED"
    if current == "OBSERVATION":
        if divergence < 0.08 and shadow_pnl > 0 and samples >= 30:
            return "PROBATION"
        return "LOCKED"
    if current == "PROBATION":
        if divergence >= 0.08 or shadow_pnl <= 0:
            return "LOCKED"
        return "PROBATION"