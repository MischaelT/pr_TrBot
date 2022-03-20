import numpy as np

import pandas as pd

import talib

# TODO Make choices
def get_predictions_by_data(df: pd.DataFrame) -> None:

    df = df.iloc[::-1].reset_index(drop=True)

    df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9) # noqa
    df['rsi'] = talib.RSI(df['close'].values, 50)
    df["prediction"] = np.nan
    df['volume_change'] = np.nan

    for index, row in df.iterrows():
        volume_change = 0

        if index>3:
            volume_change = row['volume'] / df.loc[index-3, 'volume']

        prediction_value = 0

        if row['rsi'] > 40 and row['macdhist'] > 0 and df.loc[index-1, 'macdhist'] < 0 and df.loc[index-2, 'macdhist'] < 0 and df.loc[index-3, 'macdhist'] < 0:  # noqa
            prediction_value = 1

        if row['rsi'] < 60 and row['macdhist'] < 0 and df.loc[index-1, 'macdhist'] > 0 and df.loc[index-2, 'macdhist'] > 0 and df.loc[index-3, 'macdhist'] > 0:  # noqa
            prediction_value = -1

        df.at[index, 'prediction'] = prediction_value
        df.at[index, 'volume_change'] = volume_change

        df.at[index, 'unix_time']  = pd.to_datetime(row['unix_time'], unit='s')

    # df.set_index('unix_time', inplace=True)
    # df['index'] = df.index
    df[['prediction',]].to_csv('prediction_file.csv')

    return df[['prediction']]
