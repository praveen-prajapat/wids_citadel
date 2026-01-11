from collections import deque
from agents.base_agent import BaseAgent
from engine.matching_engine import Order

class MomentumAgent(BaseAgent):
    def __init__(self, id):
        super().__init__(id)
        self.hist = deque(maxlen=50)

    def get_action(self, price):
        self.hist.append(price)
        if len(self.hist) < 50:
            return None
        sma = sum(self.hist) / 50
        if price > sma:
            return Order("BUY", price, 1, self.id, True)
        if price < sma:
            return Order("SELL", price, 1, self.id, True)
        return None
