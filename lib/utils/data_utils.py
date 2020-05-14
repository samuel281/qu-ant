from functools import reduce
from os  import makedirs
from os.path import join, dirname, exists

import pandas as pd
import pandas_datareader.data as web

from datetime import datetime, timedelta, date


def get_data_dir():
    """
    Get price data dir
    :return: data dir string
    """
    return join(f'{dirname(__file__)}/../../data/daily')


def get_data_path(symbol):
    """
    Get price data path
    :param symbol: security symbol
    :return:
    """
    return join(get_data_dir(), f'{symbol}.csv')


def fetch_data(symbol, start_date, end_date):
    """
    Fetch Yahoo Finance Data, Load them as Pandas DF and reset the column order to be compatible
    with the BackTrader package.
    :param symbol: Yahoo Finance Security symbol (ex. GOOG, 005930.KS, ...)
    :param start_date: start date of the price data
    :param end_date: end date of the price data
    :return: Pandasd DF
    """
    df = web.DataReader(symbol, 'yahoo', start_date, end_date)
    return df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]


def save_data(df, symbol):
    df.to_csv(get_data_path(symbol))


def download_data(symbol, start_date, end_date):
    """
    Download Yahoo Finance Data and save it as CSV file.
    :param symbol: Yahoo Finance Security symbol (ex. GOOG, 005930.KS, ...)
    :param start_date: start date of the price data
    :param end_date: end date of the price data
    :return:
    """
    df = fetch_data(symbol, start_date, end_date)
    if not exists(get_data_dir()):
        makedirs(get_data_dir(),  exist_ok=True)

    save_data(df, symbol)
    return df


def expand_data(df, symbol, start_date, end_date):
    """
    Expanding the price DataFrame by the given start/end date.
    It compares the min/max dates in the DF with provided start/end dates.

    Assuming that there's no missing price data between min and max date of the DF.
    :param df: price data DF
    :param symbol: Yahoo Finance Security symbol (ex. GOOG, 005930.KS, ...)
    :param start_date: start date of the price data
    :param end_date: end date of the price data
    :return: expanded DF
    """
    min_date = df.index.min().date()
    max_date = df.index.max().date()

    if min_date > start_date:
        incr_df = fetch_data(symbol, start_date, min_date)
        df = pd.concat([incr_df, df]).drop_duplicates()

    if max_date < end_date - timedelta(days=2):
        incr_df = fetch_data(symbol, max_date, end_date)
        df = pd.concat([df, incr_df]).drop_duplicates()

    return df


def restore_data(symbol):
    """
    Read Yahoo Finance CSV Data from data dir and reset Date index.
    :param symbol: Yahoo Finance Security symbol (ex. GOOG, 005930.KS, ...)
    :return: Pandas DataFrame
    """
    df = pd.read_csv(get_data_path(symbol))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index("Date")

    return df


def load_data(symbol, start_date=date(1997, 7, 1), end_date=datetime.today().date(), auto_adjust_vals=True):
    """
    Load Yahoo Finance CSV Data as Pandas Dataframe.
    If the price data of the symbol is not stored locally yet, download the data from Yahoo finance as well.
    :param symbol: Yahoo Finance Security symbol (ex. GOOG, 005930.KS, ...)
    :param start_date: start date of the price data
    :param end_date: end date of the price data
    :param auto_adjust_vals: Whether to adjust open, high, low, close based on the adjust_close automatically.
    :return: Pandas DataFrame
    """

    if not exists(get_data_path(symbol)):
        df = download_data(symbol, start_date, end_date)
    else:
        df = restore_data(symbol)
        exp_df = expand_data(df, symbol, start_date, end_date)
        if df.size != exp_df.size:
            df = exp_df
            save_data(df, symbol)

    df = df[(df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))]

    if auto_adjust_vals:
        adj_factor = df['Adj Close'] / df['Close']
        new_df = pd.DataFrame()
        new_df['Open'] = df['Open'] * adj_factor
        new_df['High'] = df['High'] * adj_factor
        new_df['Low'] = df['Low'] * adj_factor
        new_df['Close'] = df['Adj Close']
        new_df['Volume'] = df['Volume']
        df = new_df

    return df


def sync_market_days(df, *dfs):
    """
    Get common market days across DataFrames and adjust given DataFrames to have only common market days.
    This is useful when you want to deal with securities from different stock market.
    ex. KOSPI + S&P500
    :param df: pandas df
    :param dfs: vargs pandas df
    :return: adjusted df
    """
    idxs = map(lambda d: d.index, dfs)
    common_idx = reduce(lambda pidx, cidx: pidx & cidx, idxs, df.index)
    return (df.loc[common_idx], *[d.loc[common_idx] for d in dfs])


