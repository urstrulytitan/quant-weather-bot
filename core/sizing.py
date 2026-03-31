import math

def target_size(s_max, ev_adj, psi_adj):
    return s_max * (1/(1+math.exp(-ev_adj))) * (1 - psi_adj)

def hysteresis(decision_state, psi_adj, stable_ms):
    if psi_adj > 0.6: return "trim"
    if psi_adj < 0.4 and stable_ms >= 500: return "add"
    return decision_state  # hold