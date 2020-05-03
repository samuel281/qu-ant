from lib.indicators.first_market_day_of_month import FirstMarketDayOfMonth
from lib.strategies.strategy_base import StrategyBase


class FixedPercentageStrategy(StrategyBase):
    """
    FixedPercentageStrategy.

    Rebalance the portfolio once a month.
    The target percentage of each security is 1.0 / num of security.
    """

    def __init__(self):
        self.fdom = FirstMarketDayOfMonth(self.data, plot=False)
        self.first = True
        self.retries = dict()

    def get_target_value_per_security(self):
        return self.broker.get_value() / len(self.datas)

    def rebalance(self):
        data_value_dict = self.get_portfolio_values()
        target_value_per_sec = self.get_target_value_per_security()

        sec_to_sell = []
        sec_to_buy = []
        for data in self.datas:
            if data_value_dict.get(data, 0) > target_value_per_sec:
                sec_to_sell.append(data)
            elif data_value_dict.get(data, 0) < target_value_per_sec:
                sec_to_buy.append(data)

        # You have to submit sell order first in order to make enough cash to BUY.
        for data in sec_to_sell:
            self.order_target_value(data, target_value_per_sec)

        # Then you can submit but order.
        for data in sec_to_buy:
            # This can't guarantee that your order will be executed.
            # Therefore, better consider putting enough buy_margin.
            self.order_target_value(data, target_value_per_sec * (1 - self.params.buy_margin) )

    def next(self):
        if not self.fdom[0]:
            return

        self.rebalance()