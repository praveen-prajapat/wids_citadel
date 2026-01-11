import numpy as np

class Metrics:
    def __init__(self, tape, snapshots):
        prices = [p for _, p, _, _ in tape.trades]
        spreads = [s for _,_,_,s,_ in snapshots.data if s is not None]

        self.vwap = np.average(prices) if prices else 0
        self.avg_spread = np.mean(spreads) if spreads else 0
        self.volatility = np.std(prices) if prices else 0
