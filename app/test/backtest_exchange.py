import numpy as np
from data.postgres import Postgres_db
from exchange_managers.abstract_manager import Exchange_manager
import pandas as pd

class Test_exchange():

    def __init__(self, path_to_data:str, account_balance: int) -> None:

        self.db = Postgres_db()
        self.path = path_to_data

        self.account_balance = account_balance
        self.asset_amount = 0

        self.comission = 0.001
        self.klines_df = self.get_asset_dataframe(path_to_data)
        self.history_df = self.get_history_dataframe()

        self.tick = -1


    def get_asset_dataframe(self, path: str) -> pd.DataFrame:

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

        df = pd.read_csv(path, names=cols_names, keep_date_col=True)

        return df[['unix_time', 'open','high', 'low', 'close', 'volume']]

    def get_history_dataframe(self):

        history = pd.DataFrame(data=None, index=None, columns=['datetime', 'asset_balance', 'asset_price'], dtype=None, copy=False)
        history['index'] = history.index
        history['datetime'] = self.klines_df['unix_time']
        history['asset_balance'] = np.nan
        history['account_balance'] = np.nan
        history['asset_price'] = (self.klines_df['high']+self.klines_df['low'])/2

        return history

    def buy(self, quantity):
        self.history.at[self.day, 'asset_balance'] += quantity
        self.history.at[self.day, 'account_balance'] -= quantity*self.history.at[self.day, 'asset_price']
    
    def sell(self, quantity):
        self.history.at[self.day, 'asset_balance'] -= quantity
        self.history.at[self.day, 'account_balance'] += quantity*self.history.at[self.day, 'asset_price']*(1-self.comission)

    def do_nothing(self):
        self.history.at[self.day, 'asset_balance'] = self.history.at[self.day-1, 'asset_balance']
        self.history.at[self.day, 'account_balance'] = self.history.at[self.day-1, 'account_balance']

    def get_statistics(self):
        print(self.history.at[0, 'account_balance'])
        print(self.history.at[self.day, 'account_balance'])
