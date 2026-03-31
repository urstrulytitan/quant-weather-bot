import time
from dataclasses import dataclass

@dataclass
class OBSnapshot:
    ts: float
    bid_px: float
    ask_px: float
    bid_sz: float
    ask_sz: float
    depth_curve: list[tuple[float,float]]  # [(px, qty)...]

def compute_features(snaps: list[OBSnapshot]) -> dict:
    # simplistic placeholders; replace with real microstructure math
    if len(snaps) < 2: return {}
    last = snaps[-1]; prev = snaps[-2]
    spread = last.ask_px - last.bid_px
    spread_velocity = spread - (prev.ask_px - prev.bid_px)
    imbalance = (last.bid_sz - last.ask_sz) / max(last.bid_sz + last.ask_sz, 1e-6)
    depth_slope = (last.depth_curve[-1][1] - last.depth_curve[0][1]) / len(last.depth_curve)
    persistence = sum(1 for s in snaps[-10:] if (s.bid_px<=last.bid_px<=s.ask_px))/10
    flicker = sum(abs(snaps[i].bid_px-snaps[i-1].bid_px)>0 for i in range(1,min(20,len(snaps))))/20
    return dict(spread_velocity=spread_velocity, imbalance=imbalance,
                depth_slope=depth_slope, persistence=persistence, flicker=flicker, spread=spread)