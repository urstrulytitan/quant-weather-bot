def elasticity(conviction, max_conviction, psi_value, alpha=0.6):
    E = 1 + alpha * (conviction / max_conviction)
    return psi_value / E