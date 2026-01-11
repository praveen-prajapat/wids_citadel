from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, id):
        self.id = id
        self.cash = 1e6
        self.inventory = 0

    @abstractmethod
    def get_action(self, snapshot):
        pass
