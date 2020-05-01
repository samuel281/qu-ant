from datetime import datetime

from lib.strategies.strategy_base import StrategyBase


class HoldStrategy(StrategyBase):
    """
    Hold Strategy.
    Usually, used for benchmarking test.
    It buys a certain amount of security and holds it until the end of the back-test window.

    buy_date: iso-format str, buy order will be created the first market day after the buy_date.
    buy_margin: float, the ratio of cash which will be hold out from the buy order.
                BT package creates the buy order at the current close price and it executes the order at the open price next day.
                Therefore, your order can be cancelled because of the OrderMargin.
                Put number (0.0, 1.0]
    """
    params = dict(
        buy_date=datetime.today().date(),
        buy_margin=0.01
    )

    def next(self):
        if self.get_current_date() >= self.params.buy_date and not self.position:
            self.order_target_percent(data=self.data, target=1.0 - self.params.buy_margin)

    def on_order_executed(self, order):
        pass
