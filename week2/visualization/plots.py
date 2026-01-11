import matplotlib.pyplot as plt
import pandas as pd

def plot_scenario(name, tape, snapshots):
    df = pd.DataFrame(tape.trades, columns=["t","p","q","s"])
    snap = pd.DataFrame(snapshots.data,
        columns=["t","bid","ask","spread","mid"])

    fig, ax = plt.subplots(2,1)
    ax[0].plot(snap.t, snap.mid)
    ax[1].plot(snap.t, snap.spread)

    fig.suptitle(name)
    return fig
