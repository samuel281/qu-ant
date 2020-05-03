from datetime import datetime

from lib.strategies.strategy_base import StrategyBase


class HoldStrategy(StrategyBase):
    """
    Hold Strategy.
    Usually, used for benchmarking test.
    It buys a certain amount of security and holds it until the end of the back-test window.

    buy_date: iso-format str, buy order will be created the first market day after the buy_date.
    """
    params = dict(
        buy_date=datetime.today().date(),
    )

    def next(self):
        if self.get_current_date() >= self.params.buy_date and not self.position:
            self.order_target_percent(data=self.data, target=1.0 - self.params.buy_margin)

    def on_order_executed(self, order):
        pass
