import logging

import backtrader as bt


class StrategyBase(bt.Strategy):
    """
    Strategy Base Class.
    Implements basic order notification logic.

    buy_margin: float, the ratio of cash which will be hold out from the buy order.
                BT package creates the buy order at the current close price and it executes the order at the open price next day.
                Therefore, your order can be cancelled because of the OrderMargin.
                Put number (0.0, 1.0]
    """

    params=dict(buy_margin=0.01)

    def log(self, msg, dt=None, level=logging.INFO):
        dt = dt or self.datas[0].datetime.date(0)
        logging.log(level, f'[{dt.isoformat()}] {msg}')

    def on_order_executed(self, order):
        """
        Call back method that is invoked after any successful order execution.
        :param order:  backtrader.order.Order
        :return: None
        """
        pass

    def on_order_margin(self, order):
        pass

    def get_portfolio_values(self):
        """
        Returns values of securities in the portfolio
        :return: dict(data_name=value)
        """
        return {
            data: self.broker.get_value(datas=[data]) if self.broker.get_value(datas=[data]) else 0.0
            for data in self.datas
        }

    def get_current_date(self):
        return self.data.datetime.date(0)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        order_type = 'BUY' if order.isbuy() else 'SELL'

        if order.status in [order.Completed]:
            self.log(
                f'[{order.data._name}] {order_type} EXECUTED, Price: {order.executed.price:.2f}, '
                f'Cost: {order.executed.value:.2f}, Commission {order.executed.comm:.2f}',
                level=logging.DEBUG
            )
            self.on_order_executed(order)

        elif order.status == order.Canceled:
            self.log(f'[{order.data._name}] {order_type} order canceled.', level=logging.WARNING)
        elif order.status == order.Margin:
            self.log(f'[{order.data._name}] {order_type} order Margin.', level=logging.WARNING)
            self.on_order_margin(order)
        elif order.status == order.Rejected:
            self.log(f'[{order.data._name}] {order_type} order Rejected.', level=logging.WARNING)

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'OPERATION PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}', level=logging.DEBUG)
