from datetime import datetime

from lib.strategies.strategy_base import StrategyBase


class HoldAllStrategy(StrategyBase):
    """
    HoldAll Strategy.
    Usually, used for benchmarking test.
    Almost same with the HoldStrategy, it tries to buy all provided securities with the same ratio.

    buy_date: iso-format str, buy order will be created the first market day after the buy_date.
    """
    params = dict(
        buy_date=datetime.today().isoformat(),
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
