from dataclasses import dataclass

@dataclass
class Position:
    current: float
    pending: float

def compute_delta(s_target, position: Position, min_trade):
    delta = s_target - (position.current + position.pending)
    if abs(delta) < min_trade: return 0.0
    return delta  # negative => trim immediately; positive => add if allowed elsewhere