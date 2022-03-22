import numpy as np

import pandas as pd

from strategies.base_strategy import Base_strategy

import talib


class Rsi_strategy(Base_strategy):

    def __init__(self) -> None:
        super().__init__()

    def get_prediction(self, ticker: str, kline: str) -> str:

        date = kline[1]

        df = self.data_to_dataframe(ticker, date=date, timeframe='1h')
        prediction = self.get_predictions_by_data(df)

        return prediction

    def data_to_dataframe(self, ticker: str, timeframe: str, date: int) -> pd.DataFrame:

        query = """SELECT * FROM btc_usd
                    WHERE unix_time<%s
                    ORDER BY unix_time DESC
                    LIMIT 51"""

        params = (date,)

        data = self.db.get_data(query, params)

        df = self.db.query_to_dataframe(data)

        return df

    def get_predictions_by_data(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.iloc[::-1].reset_index(drop=True)

        df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9) # noqa
        df['rsi'] = talib.RSI(df['close'].values, 10)
        df["prediction"] = np.nan
        df['volume_change'] = np.nan

        for index, row in df.iterrows():
            volume_change = 0

            if index > 3:
                volume_change = row['volume'] / df.loc[index-3, 'volume']

            prediction_value = 0

            # if row['rsi'] > 40 and row['macdhist'] > 0 and df.loc[index-1, 'macdhist'] < 0 and df.loc[index-2, 'macdhist'] < 0 and df.loc[index-3, 'macdhist'] < 0:  # noqa
            #     prediction_value = 1

            # if row['rsi'] < 60 and row['macdhist'] < 0 and df.loc[index-1, 'macdhist'] > 0 and df.loc[index-2, 'macdhist'] > 0 and df.loc[index-3, 'macdhist'] > 0:  # noqa
            #     prediction_value = -1

            if row['rsi'] > 40:  # noqa
                prediction_value = 1

            if row['rsi'] < 60:  # noqa
                prediction_value = -1

            df.at[index, 'prediction'] = prediction_value
            df.at[index, 'volume_change'] = volume_change

            df.at[index, 'unix_time'] = pd.to_datetime(row['unix_time'], unit='s')

        df[['unix_time', 'rsi', 'prediction']].to_csv('prediction_file.csv')

        return int(df[['prediction']].iloc[50])
