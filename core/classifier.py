def classify(persistence, consistency, depth_slope, flicker):
    if flicker > 0.6 or consistency < 0.2: return "ILLUSORY"
    if depth_slope < 0 and persistence < 0.3: return "PREDATORY"
    if persistence > 0.7 and consistency > 0.35: return "CALM"
    return "COMPETITIVE"