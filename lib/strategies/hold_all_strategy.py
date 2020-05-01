from datetime import datetime

from lib.strategies.strategy_base import StrategyBase


class HoldAllStrategy(StrategyBase):
    """
    HoldAll Strategy.
    Usually, used for benchmarking test.
    Almost same with the HoldStrategy, it tries to buy all provided securities with the same ratio.

    buy_date: iso-format str, buy order will be created the first market day after the buy_date.
    buy_margin: float, the ratio of cash which will be hold out from the buy order.
                BT package creates the buy order at the current close price and it executes the order at the open price next day.
                Therefore, your order can be cancelled because of the OrderMargin.
                Put number (0.0, 1.0]
    """
    params = dict(
        buy_date=datetime.today().isoformat(),
        buy_margin=0.01
    )

    def next(self):
        if self.position:
            return

        if self.get_current_date().isoformat() < self.params.buy_date:
            return

        target_ratio = 1.0 - self.params.buy_margin
        target_ratio_per_sec = target_ratio / len(self.datas)
        for security in self.datas:
            self.order_target_percent(data=security, target=target_ratio_per_sec)

    def on_order_executed(self, order):
        pass
