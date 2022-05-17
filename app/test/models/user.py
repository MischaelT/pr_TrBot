import logging
from test.test_config import USER_BALANCE

import pandas as pd


class User():

    def __init__(self) -> None:

        self.account_balance = USER_BALANCE
        # self.asset_balance = {i: 0 for i in USER_ASSET_LIST}
        self.asset_balance = 0

        self.history_df: pd.DataFrame = self.initialize_history_df()

# TODO implement balances for different assets
    def initialize_history_df(self):

        history = pd.DataFrame(data=None, index=None, columns=['unix_time', 'account_balance'], dtype=None, copy=False)  # noqa
        history['unix_time'] = 0
        history['account_balance'] = 0
        history['asset_balance'] = 0

        history.at[0, 'account_balance'] = self.account_balance

        return history

    def get_statistics(self):
        logging.info(self.history_df)
