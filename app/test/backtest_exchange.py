import logging
import uuid
from test.order import Order
from typing import List

from data.postgres import Postgres_db

import pandas as pd


class Test_exchange():

    def __init__(self, start_date: int, account_balance: int) -> None:

        self.db = Postgres_db()

        self.account_balance = account_balance
        self.asset_balance = 0

        self.comission = 0.001
        self.klines_df = self.get_asset_dataframe(start_date)

        self.history_df: pd.DataFrame = self.get_history_dataframe()

        self.tick = 0
        self.orders_list: List[Order] = []

    def get_curent_kline(self):

        for row in self.klines_df.itertuples():

            self.__manage_orders()

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
        history['unix_time'] = self.klines_df['unix_time']
        history['asset_balance'] = 0
        history['account_balance'] = 0
        history['asset_price'] = (self.klines_df['high']+self.klines_df['low'])/2

        history.at[0, 'account_balance'] = self.account_balance
        return history

    def place_buy_order(self, order_type, symbol, quantity, price):

        order_id = uuid.uuid4()

        trade = round(self.account_balance - quantity * self.history_df.at[self.tick, 'asset_price'] * (1-self.comission), 2)  # noqa

        if trade >= 0:

            order = Order(order_id, order_type, quantity, symbol, order_execution_price=price, direction='buy')
            self.orders_list.append(order)

        else:
            logging.info('DN')
            logging.info('Not enought money')
            self.do_nothing()

    def place_sell_order(self, order_type, symbol, quantity, price):

        order_id = uuid.uuid4()
        trade = round(self.asset_balance - quantity, 2)

        if trade >= 0:

            order = Order(order_id, order_type, quantity, symbol, order_execution_price=price, direction='sell')
            self.orders_list.append(order)

        else:
            logging.info('DN')
            logging.info('Not enought money')
            self.do_nothing()

# TODO Implement OCO orders
    def place_OCO_order(self):
        pass

    def do_nothing(self):
        self.history_df.at[self.tick, 'asset_balance'] = self.asset_balance
        self.history_df.at[self.tick, 'account_balance'] = self.account_balance

    def get_statistics(self):

        self.history_df[['unix_time', 'asset_balance', 'account_balance']].to_csv('history.csv')
        logging.info(self.history_df.at[self.tick, 'account_balance'])

# TODO Implement blocking balances in limit orders
    def __manage_orders(self):

        for order in self.orders_list:

            if order.order_type == 'market':
                self.__execute_order(order)
                self.orders_list.remove(order)

            elif order.order_type == 'limit':

                if not order.is_proceed:

                    if order.order_type == 'sell':
                        self.asset_balance -= order.quantity
                    elif order.order_type == 'buy':
                        pass

                is_executed = self.__process_limit_order(order)

                if is_executed:
                    self.orders_list.remove(order)

            elif order.order_type == 'OCO':
                pass

    def __process_limit_order(self, order: Order):

        order.is_proceed = True

        is_executed = False

        if self.history_df.at[self.tick, 'asset_price'] > order.signal_price:
            self.__execute_order(order)

        return is_executed

    def __execute_order(self, order: Order):

        if order.direction == 'buy':
            logging.info('Buy')
            trade = round(self.account_balance - order.quantity * self.history_df.at[self.tick, 'asset_price'] * (1-self.comission), 2)  # noqa

            self.account_balance = trade
            self.history_df.at[self.tick, 'account_balance'] = self.account_balance

            self.asset_balance += order.quantity
            self.history_df.at[self.tick, 'asset_balance'] = self.asset_balance + order.quantity

        if order.direction == 'sell':
            logging.info('sell')
            trade = round(self.asset_balance - order.quantity, 2)

            self.asset_balance = trade
            self.history_df.at[self.tick, 'asset_balance'] = self.asset_balance

            self.account_balance += round(order.quantity * self.history_df.at[self.tick, 'asset_price'] * (1-self.comission), 2)  # noqa
            self.history_df.at[self.tick, 'account_balance'] = self.account_balance
