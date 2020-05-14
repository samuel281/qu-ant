import pandas as pd
import empyrical as ep


def positions_value_to_df(position_value, enrich_total=True, total_col_name='total'):
    """
    Convert bt.analyzers.PositionsValue result to pandas DF
    :param position_value: order_dict
    :param enrich_total: whether enriching total value column or not.
    :param total_col_name: name of the total column in case set enrich_total true.
    :return: DF
    """
    df = pd.DataFrame(
        index=list(position_value.keys())[1:],
        data=list(position_value.values())[1:],
        columns=list(position_value.values())[0]
    )
    df.index = df.index.rename('date')

    if enrich_total:
        df[total_col_name] = df.sum(axis=1)

    return df


def annual_return_to_df(annual_return, value_col='return'):
    """
    Convert bt.analyzers.AnnualReturn result to pandas DF
    :param annual_return: order_dict
    :return: DF
    """
    df = pd.DataFrame({
        'year': list(dict(annual_return).keys()),
        value_col :list(dict(annual_return).values())
    })
    df = df.set_index('year')
    return df


def get_annual_return_analysis_df(res):
    if not res.analyzers.annual_return:
        return None

    return annual_return_to_df(res.analyzers.annual_return.get_analysis())


def get_pos_values_analysis_df(res):
    if not res.analyzers.positions_value:
        return None

    return positions_value_to_df(res.analyzers.positions_value.get_analysis())


def get_default_perf_analysis_df(res, index):
    if not res.analyzers.sharpe:
        return None

    if not res.analyzers.draw_down:
        return None

    annual_return_df = get_annual_return_analysis_df(res)
    best_year = annual_return_df['return'].max()
    worst_year = annual_return_df['return'].min()
    mean = annual_return_df['return'].mean()
    stddev = annual_return_df['return'].std()


    pos_val_df = get_pos_values_analysis_df(res)
    if pos_val_df is None:
        return None

    period_start = pos_val_df.index.min()
    period_end = pos_val_df.index.max()
    initial_value = pos_val_df['total'][0]
    final_value = pos_val_df['total'][-1]
    period_year = round((period_end - period_start).days / 365)
    cagr = pow((final_value / initial_value), (1 / period_year)) -1
    # TODO(Sungwoo): calculate inflation adjusted cagr
    # inflation = (Ending CPI level - Beginning CPI level) / Beginning CPI level
    # inflation_adjusted_cagr = (1 + cagr) / (1 + inflation) - 1

    return pd.DataFrame(
        dict(
            initial_value=pos_val_df['total'][0],
            final_value=pos_val_df['total'][-1],
            period_start=pos_val_df.index.min(),
            period_end=pos_val_df.index.max(),
            best_year = best_year,
            worst_yaer = worst_year,
            mean = mean,
            stddev = stddev,
            sharpe_ratio=res.analyzers.sharpe.get_analysis()['sharperatio'],
            mdd=res.analyzers.draw_down.get_analysis()["max"]["drawdown"],
            cagr=cagr,
        ),
        index=[index]
    )
