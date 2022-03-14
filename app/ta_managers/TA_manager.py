import numpy as np

import pandas as pd

import talib


def get_predictions_by_data(data: str = ''):

    cols_names = cols_names = [
                                'unix_time', 'open',
                                'high', 'low',
                                'close', 'volume',
                                'unix_close_time',
                                'Quote asset volume',
                                'Number_of_trades',
                                'base asset volume',
                                'Taker buy quote asset volume',
                                'Ignore'
                                ]

    df = pd.read_csv('app/ta_managers/BTCBUSD_1d_499 days ago UTC.csv', names=cols_names, keep_date_col=True)

    df = df.iloc[::-1].reset_index(drop=True)

    df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9) # noqa
    df['rsi'] = talib.RSI(df['close'].values, 50)
    df["prediction"] = np.nan

    for index, row in df.iterrows():

        prediction_value = 0

        if row['rsi'] > 40 and row['macdhist'] > 0 and df.loc[index-1, 'macdhist'] < 0 and df.loc[index-2, 'macdhist'] < 0 and df.loc[index-3, 'macdhist'] < 0:  # noqa
            prediction_value = 1

        if row['rsi'] < 60 and row['macdhist'] < 0 and df.loc[index-1, 'macdhist'] > 0 and df.loc[index-2, 'macdhist'] > 0 and df.loc[index-3, 'macdhist'] > 0:  # noqa
            prediction_value = -1

        df.at[index, 'prediction'] = prediction_value

        # df['unix_time'] = pd.to_datetime(df['unix_time'])
        # df.set_index('unix_time', inplace=True)

    df[['unix_time', 'prediction']].to_csv('prediction_file.csv')


get_predictions_by_data()
