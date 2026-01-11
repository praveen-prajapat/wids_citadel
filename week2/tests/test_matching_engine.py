from engine.matching_engine import MatchingEngine, Order
from analytics.tape import Tape

def test_market_buy_sweep():
    eng = MatchingEngine()
    tape = Tape()

    eng.asks = {
        101: [Order("SELL",101,10,0)],
        102: [Order("SELL",102,20,0)],
        103: [Order("SELL",103,30,0)]
    }

    eng.submit(Order("BUY",0,60,1,True),0,tape)

    assert len(tape.trades) == 3
    assert not eng.asks
