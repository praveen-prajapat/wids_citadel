from collections import deque

class Order:
    def __init__(self, side, price, qty, agent_id, is_market=False):
        assert qty >= 0
        self.side = side
        self.price = price
        self.qty = qty
        self.agent_id = agent_id
        self.is_market = is_market

class MatchingEngine:
    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.last_price = 100.0

    def mid_price(self):
        if not self.bids or not self.asks:
            return self.last_price
        return (max(self.bids) + min(self.asks)) / 2

    def submit(self, order, t, tape):
        if order.side == "BUY":
            self._match(order, self.asks, min, tape, t)
        else:
            self._match(order, self.bids, max, tape, t)

    def _match(self, order, book, best_fn, tape, t):
        while order.qty > 0 and book:
            price = best_fn(book)
            if not order.is_market:
                if (order.side == "BUY" and price > order.price) or \
                   (order.side == "SELL" and price < order.price):
                    break

            level = book[price]
            resting = level[0]
            traded = min(order.qty, resting.qty)

            tape.append(t, price, traded, order.side)
            self.last_price = price

            order.qty -= traded
            resting.qty -= traded

            if resting.qty == 0:
                level.popleft()
            if not level:
                del book[price]

        if order.qty > 0 and not order.is_market:
            book.setdefault(order.price, deque()).append(order)

        for p in book:
            for o in book[p]:
                assert o.qty >= 0
