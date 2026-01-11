import random
import numpy as np

from engine.event_loop import EventLoop
from engine.matching_engine import MatchingEngine
from agents.noise_agent import NoiseTrader
from agents.momentum_agent import MomentumAgent
from agents.market_maker_agent import MarketMakerAgent
from analytics.tape import Tape
from analytics.snapshots import SnapshotRecorder
from analytics.metrics import Metrics
from visualization.plots import plot_scenario
from reports.pdf_report import generate_pdf_report

TOTAL_AGENTS = 100
SIMULATION_TIME = 30 * 60
SNAPSHOT_INTERVAL = 1
SEED = 42

SCENARIOS = {
    "A": {"noise": 100, "market_maker": 0, "momentum": 0},
    "B": {"noise": 80, "market_maker": 20, "momentum": 0},
    "C": {"noise": 80, "market_maker": 0, "momentum": 20},
}

def run_scenario(name, config):
    assert sum(config.values()) == TOTAL_AGENTS

    engine = MatchingEngine()
    tape = Tape()
    snapshots = SnapshotRecorder()
    loop = EventLoop(engine, tape, snapshots)

    agents = []
    aid = 0

    for _ in range(config["noise"]):
        agents.append(NoiseTrader(aid)); aid += 1
    for _ in range(config["market_maker"]):
        agents.append(MarketMakerAgent(aid)); aid += 1
    for _ in range(config["momentum"]):
        agents.append(MomentumAgent(aid)); aid += 1

    for agent in agents:
        loop.register_agent(agent)

    loop.run(SIMULATION_TIME, SNAPSHOT_INTERVAL)

    metrics = Metrics(tape, snapshots)
    figs = plot_scenario(name, tape, snapshots)

    return metrics, figs

def main():
    random.seed(SEED)
    np.random.seed(SEED)

    results = {}
    figures = {}

    for name, cfg in SCENARIOS.items():
        m, f = run_scenario(name, cfg)
        results[name] = m
        figures[name] = f

    generate_pdf_report(results, figures)

if __name__ == "__main__":
    main()
