import backtrader as bt


class FirstMarketDayOfMonth(bt.Indicator):
    lines = ('fdom', )

    def next(self):
        if not self.data.datetime.date(-1):
            # today is the first day
            self.lines.fdom[0] = True
        else:
            # month changed.
            self.lines.fdom[0] = self.data.datetime.date(-1).month < self.data.datetime.date(0).month