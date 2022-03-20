import pandas as pd
from pandas import DataFrame
from ta_managers.TA_manager import get_predictions_by_data
from strategies.base_strategy import Base_strategy


class Rsi_strategy(Base_strategy):

    def __init__(self) -> None:
        super().__init__()

    def get_test_prediction(self, ticker, index, timeframe:str) -> str:

        df = self.data_to_dataframe(ticker, timeframe, time_range=200)
        predictions = get_predictions_by_data(df)

        prediction = predictions["prediction"].iloc[index]

        return prediction

    def get_prediction(self, ticker:str, timeframe:str) -> str:

        df = self.data_to_dataframe(ticker, timeframe, time_range=200)
        predictions = get_predictions_by_data(df)

        prediction = predictions["prediction"].iloc[0]

        return prediction

    def data_to_dataframe(self, ticker:str, timeframe:str, time_range:int) -> DataFrame:

        cols_names = [
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

        df = pd.read_csv('app/data/view_managers/csv/BTCBUSD_1d_499 days ago UTC.csv', names=cols_names, keep_date_col=True)

        return df

