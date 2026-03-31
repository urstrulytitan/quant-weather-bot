def ev_model(p_model: float, p_market: float) -> float:
    return max(0.0, p_model - p_market)  # only positive EV