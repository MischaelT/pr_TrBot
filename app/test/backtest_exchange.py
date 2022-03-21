from data.postgres import Postgres_db

import pandas as pd


class Test_exchange():

    def __init__(self, start_date: int, account_balance: int) -> None:

        self.db = Postgres_db()

        self.account_balance = account_balance
        self.asset_amount = 0

        self.comission = 0.001
        self.klines_df = self.get_asset_dataframe(start_date)

        self.history_df = self.get_history_dataframe()

        self.tick = 0

    def get_curent_kline(self):

        for row in self.klines_df.itertuples():
            self.tick += 1
            yield row

    def get_asset_dataframe(self, start_date: str) -> pd.DataFrame:

        query = """SELECT * FROM btc_usd
                    WHERE (unix_time>%s)
                    ORDER BY unix_time ASC"""

        params = (start_date,)

        querry_result = self.db.get_data(query, params)

        df = self.db.query_to_dataframe(querry_result)

        return df[['unix_time', 'open', 'high', 'low', 'close', 'volume']]

    def get_history_dataframe(self):

        history = pd.DataFrame(data=None, index=None, columns=['datetime', 'asset_balance', 'asset_price'], dtype=None, copy=False)  # noqa
        history['datetime'] = self.klines_df['unix_time']
        history['asset_balance'] = 0
        history['account_balance'] = 0
        history['asset_price'] = (self.klines_df['high']+self.klines_df['low'])/2

        history.at[0, 'account_balance'] = self.account_balance
        return history

    def place_buy_order(self, quantity):
        self.history_df.at[self.tick, 'asset_balance'] = self.history_df.at[self.tick-1, 'asset_balance'] + quantity
        self.history_df.at[self.tick, 'account_balance'] = self.history_df.at[self.tick-1, 'account_balance'] - quantity*self.history_df.at[self.tick, 'asset_price']*(1-self.comission)  # noqa

    def place_sell_order(self, quantity):
        self.history_df.at[self.tick, 'asset_balance'] = self.history_df.at[self.tick-1, 'asset_balance'] - quantity
        self.history_df.at[self.tick, 'account_balance'] = self.history_df.at[self.tick-1, 'account_balance'] + quantity*self.history_df.at[self.tick, 'asset_price']*(1-self.comission)  # noqa

    def do_nothing(self):
        self.history_df.at[self.tick, 'asset_balance'] = self.history_df.at[self.tick-1, 'asset_balance']
        self.history_df.at[self.tick, 'account_balance'] = self.history_df.at[self.tick-1, 'account_balance']

    def get_statistics(self):
        pass
