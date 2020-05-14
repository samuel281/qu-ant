import logging

import backtrader as bt

from lib.indicators.first_market_day_of_month import FirstMarketDayOfMonth
from lib.strategies.strategy_base import StrategyBase


class DualmomentumStrategy(StrategyBase):
    """
    Dual Momentum Strategy
    """
    params=dict(
        momentum_period=120,
        rb_ind=FirstMarketDayOfMonth,
        saving_interest=0.02,
    )

    def __init__(self):
        self.indicators = dict()
        for data in self.datas:
            self.indicators[data] = dict(
                roc=bt.indicators.ROC(data, period = self.params.momentum_period)
            )

        self.rebanance_day = self.params.rb_ind(self.data)
        self.cur_security = None

    def next(self):
        if not self.rebanance_day[0]:
            return

        max_profit = self.params.saving_interest
        max_profit_security = None
        for data in self.datas:
            if self.indicators[data].get("roc")[0] > max_profit:
                max_profit = self.indicators[data].get("roc")[0]
                max_profit_security = data

        if max_profit_security == self.cur_security:
            self.log(f'Nothing to do.', level=logging.DEBUG)
            return

        if self.cur_security:
            self.log(f'Close the portfolio {self.cur_security._name}', level=logging.DEBUG)
            self.close(self.cur_security)

        if not max_profit_security:
            self.log(f"Nothing is better than saving. We'd better get out of the market.", level=logging.DEBUG)
            self.cur_security = None
            return

        self.log(f'Buy new portfolio {max_profit_security._name}', level=logging.DEBUG)
        self.order_target_percent(max_profit_security, 1 - self.params.buy_margin)

    def on_order_executed(self, order):
        self.cur_security = order.data


class DualmomentumStrategyWithNaiveStopLoss(StrategyBase):
    """
    Dual Momentum + Stop Loss Strategy
    """
    params=dict(
        momentum_period=120,
        rb_ind=FirstMarketDayOfMonth,
        saving_interest=0.02,
        stop_loss=-0.15
    )

    def __init__(self):
        self.indicators = dict()
        for data in self.datas:
            self.indicators[data] = dict(
                roc=bt.indicators.ROC(data, period = self.params.momentum_period),
            )

        self.rebanance_day = self.params.rb_ind(self.data)
        self.cur_security = None

    def stop_loss(self):
        if not self.cur_security:
            return

        position = self.getposition(self.cur_security)
        if not position.size:
            return
        cur_price = self.getdatabyname(self.cur_security._name).close[0]
        roc = (cur_price - position.price) / position.price
        if roc < self.params.stop_loss:
            self.log(f'Position price: {position.price}, Cur price: {cur_price}. Stop Loss!')
            self.close(self.cur_security)
            self.cur_security = None

    def next(self):
        if not self.rebanance_day[0]:
            self.stop_loss()
            return

        max_profit = self.params.saving_interest
        max_profit_security = None
        for data in self.datas:
            self.log(f'{data._name} roc {self.indicators[data].get("roc")[0]}', level=logging.DEBUG)
            if self.indicators[data].get("roc")[0] > max_profit:
                max_profit = self.indicators[data].get("roc")[0]
                max_profit_security = data
                self.log(f'max_profit_security: {max_profit_security}', level=logging.DEBUG)

        if max_profit_security == self.cur_security:
            self.log(f'Nothing to do.', level=logging.DEBUG)
            return

        if self.cur_security:
            self.log(f'Close the portfolio {self.cur_security._name}', level=logging.DEBUG)
            self.close(self.cur_security)

        if not max_profit_security:
            self.log(f"Nothing is better than saving. We'd better get out of the market.", level=logging.DEBUG)
            self.cur_security = None
            return

        self.log(f'Buy new portfolio {max_profit_security._name}', level=logging.DEBUG)
        self.order_target_percent(max_profit_security, 1 - self.params.buy_margin)

    def on_order_executed(self, order):
        self.cur_security = order.data

