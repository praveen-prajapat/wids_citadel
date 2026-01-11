from agents.base_agent import BaseAgent
from engine.matching_engine import Order

class MarketMakerAgent(BaseAgent):
    def get_action(self, price):
        spread = 0.01
        skew = self.inventory * 0.0001
        buy = Order("BUY", price - spread - skew, 1, self.id)
        sell = Order("SELL", price + spread - skew, 1, self.id)
        return buy, sell
