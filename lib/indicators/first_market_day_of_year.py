import backtrader as bt


class FirstMarketDayOfYear(bt.Indicator):
    lines = ('fdoy', )

    def next(self):
        if not self.data.datetime.date(-1):
            # today is the first day
            self.lines.fdoy[0] = True
        else:
            # month changed.
            self.lines.fdoy[0] = self.data.datetime.date(-1).year < self.data.datetime.date(0).year