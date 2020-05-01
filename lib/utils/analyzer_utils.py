import pandas as pd


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