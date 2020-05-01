import backtrader as bt

from lib.strategies.strategy_base import StrategyBase


class SMAMomentumStrategy(StrategyBase):
    """
    SMA Momentum Strategy

    This simply follows the trend of the security.


    Usually, used for benchmarking test.
    It buys a certain amount of security and holds it until the end of the back-test window.

    buy_date: iso-format str, buy order will be created the first market day after the buy_date.
    buy_margin: float, the ratio of cash which will be hold out from the buy order.
                BT package creates the buy order at the current close price and it executes the order at the open price next day.
                Therefore, your order can be cancelled because of the OrderMargin.
                Put number (0.0, 1.0]
    """
    params = (
        ('maperiod', 90),
    )

    def __init__(self):
        self.sma = bt.indicators.MovingAverageSimple(self.datas, period=self.params.maperiod)
        self.roc = bt.ind.ROC(self.sma, period=10)
        self.cu = bt.ind.CrossUp(self.roc, 0)
        self.cd = bt.ind.CrossDown(self.roc, 0.01)

    def next(self):
        if not self.position and self.cu[0]:
            size = int(self.broker.get_cash() * self.cash_margin / self.data)
            self.order = self.buy(size=size)
        elif self.position and self.cd[0]:
            self.order = self.sell(size=self.position.size)