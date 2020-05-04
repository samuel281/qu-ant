import backtrader as bt


def create_and_configure_cerebro(
        strategy,
        data_feed_dict,
        strategy_params=dict(),
        initial_cash=1000000,
        comission_params=dict(commission=0.00165),
        analyzer_dict={
            bt.analyzers.SharpeRatio_A: dict(_name='sharpe'),
            bt.analyzers.AnnualReturn: dict(_name='annual_return'),
            bt.analyzers.Returns: dict(_name='returns'),
            bt.analyzers.DrawDown: dict(_name='draw_down'),
            bt.analyzers.PositionsValue: dict(_name='positions_value', cash=True, headers=True),
        }):

    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy, **strategy_params)
    cerebro.broker.setcash(initial_cash)
    cerebro.broker.setcommission(**comission_params)

    # Feed Data.
    for data_feed, params in data_feed_dict.items():
        cerebro.adddata(data_feed, **params)

    # Data analyzers.
    for analyzer, params in analyzer_dict.items():
        cerebro.addanalyzer(analyzer, **params)

    return cerebro