class Tape:
    def __init__(self):
        self.trades = []

    def append(self, t, price, qty, side):
        assert price >= 0 and qty >= 0
        self.trades.append((t, price, qty, side))
