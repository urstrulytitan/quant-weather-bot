def condition(raw_metric, volatility):
    return raw_metric / (1 + 2.5 * volatility)