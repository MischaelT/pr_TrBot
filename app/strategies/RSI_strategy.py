from pandas import DataFrame

from strategies.base_strategy import Base_strategy

from ta_managers.TA_manager import get_predictions_by_data


class Rsi_strategy(Base_strategy):

    def __init__(self) -> None:
        super().__init__()

    def get_prediction(self, ticker: str, kline: str) -> str:

        date = kline[1]

        df = self.data_to_dataframe(ticker, date=date, timeframe='1h')
        predictions = get_predictions_by_data(df)

        prediction = predictions["prediction"].iloc[0]

        return prediction

    def data_to_dataframe(self, ticker: str, timeframe: str, date: int) -> DataFrame:

        query = """SELECT * FROM btc_usd
                    WHERE unix_time<%s
                    LIMIT 51"""

        params = (date,)

        data = self.db.get_data(query, params)

        df = self.db.query_to_dataframe(data)

        return df
