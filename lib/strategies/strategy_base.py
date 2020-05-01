import logging

import backtrader as bt


class StrategyBase(bt.Strategy):
    """
    Strategy Base Class.
    Implements basic order notification logic.
    """
    def log(self, msg, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        logging.info(f'[{dt.isoformat()}] {msg}')

    def on_order_executed(self, order):
        """
        Call back method that is invoked after any successful order execution.
        :param order:  backtrader.order.Order
        :return: None
        """
        pass

    def get_current_date(self):
        return self.data.datetime.date(0)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            order_type = 'BUY' if order.isbuy() else 'SELL'
            self.log(
                f'[{order.data._name}] {order_type} EXECUTED, Price: {order.executed.price:.2f}, '
                f'Cost: {order.executed.value:.2f}, Commission {order.executed.comm:.2f}'
            )
            self.on_order_executed(order)

        elif order.status == order.Canceled:
            self.log('Order Canceled.')
        elif order.status == order.Margin:
            self.log('Order Margin.')
        elif order.status == order.Rejected:
            self.log('Order Rejected.')

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'OPERATION PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}')
