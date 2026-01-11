import heapq
from engine.events import OrderArrivalEvent, SnapshotEvent, MarketCloseEvent

class EventLoop:
    def __init__(self, engine, tape, snapshots):
        self.engine = engine
        self.tape = tape
        self.snapshots = snapshots
        self.time = 0
        self.q = []
        self.seq = 0
        self.agents = []

    def register_agent(self, agent):
        self.agents.append(agent)

    def push(self, t, ev):
        heapq.heappush(self.q, (t, self.seq, ev))
        self.seq += 1

    def run(self, end_time, snapshot_interval):
        t = 0
        while t <= end_time:
            self.push(t, SnapshotEvent())
            t += snapshot_interval

        self.push(end_time, MarketCloseEvent())

        while self.q:
            t, _, ev = heapq.heappop(self.q)
            assert t >= self.time
            self.time = t

            if isinstance(ev, MarketCloseEvent):
                break

            if isinstance(ev, SnapshotEvent):
                self.snapshots.record(self.time, self.engine)
                for a in self.agents:
                    act = a.get_action(self.engine.mid_price())
                    if act:
                        self.engine.submit(act, self.time, self.tape)
            else:
                ev.process()
