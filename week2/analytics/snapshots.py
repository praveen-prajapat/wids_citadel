class SnapshotRecorder:
    def __init__(self):
        self.data = []

    def record(self, t, engine):
        bid = max(engine.bids) if engine.bids else None
        ask = min(engine.asks) if engine.asks else None
        if bid and ask:
            spread = ask - bid
            assert spread >= 0
            mid = (bid + ask) / 2
        else:
            spread = None
            mid = engine.last_price
        self.data.append((t, bid, ask, spread, mid))
