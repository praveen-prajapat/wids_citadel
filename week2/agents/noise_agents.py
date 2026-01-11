import random
from agents.base_agent import BaseAgent
from engine.matching_engine import Order

class NoiseTrader(BaseAgent):
    def get_action(self, price):
        side = random.choice(["BUY", "SELL"])
        qty = random.randint(1, 5)
        is_market = random.random() < 0.5
        p = price * (1 + random.uniform(-0.001, 0.001))
        return Order(side, p, qty, self.id, is_market)
