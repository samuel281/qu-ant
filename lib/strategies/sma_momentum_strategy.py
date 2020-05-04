import backtrader as bt

from lib.strategies.strategy_base import StrategyBase


class SMAMomentumStrategy(StrategyBase):
    """
    SMA Momentum Strategy
    Trend is my friend.
    """
    params = (
        ('maperiod', 90),
        ('rocperiod', 10)
    )
    
    def __init__(self):
        self.sma = bt.indicators.MovingAverageSimple(self.data, period=self.params.maperiod)
        self.roc = bt.ind.ROC(self.sma, period=self.params.rocperiod)
        self.cu = bt.ind.CrossUp(self.roc, 0)
        self.cd = bt.ind.CrossDown(self.roc, 0.01)

    def next(self):
        if not self.position and self.cu[0]:
            self.order_target_value(self.data, self.broker.get_cash() * (1.0 - self.params.buy_margin))
        elif self.position and self.cd[0]:
            self.close(self.data)
