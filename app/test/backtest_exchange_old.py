import logging

from test.models.asset import Asset
from app.test.models.user import User
from test.models.kline import Kline
from test.models.orders.limit_order import LimitOrder
from test.models.orders.market_order import MarketOrder
from test.models.orders.oco_order import Oco_Order
from test.models.orders.stopLoss_order import StopLossOrder
from typing import List, Union

from data.postgres import Postgres_db

import pandas as pd

from utils.config import COMISSION


class Test_exchange():

#TODO implement getting all information by date, not with DataFrames

    def __init__(self, start_date: int, account_balance: int, trade_assets:List) -> None:

        self.db = Postgres_db()

        self.orders_list: List[Union[StopLossOrder, MarketOrder, Oco_Order, LimitOrder]] = []
        self.assets: List[Asset] = []
        self.user = User(account_balance)
        self.history_df: pd.DataFrame = self.get_history_dataframe()

        self.start_date = start_date
        self.current_kline: Kline = None
        self.tick = 0

        self.comission = COMISSION

        self.initialise_assets(trade_assets)

    def initialise_assets(self, tickers: List):

        for ticker in tickers:

            asset = Asset(ticker=ticker)
            self.assets.append(asset)

    def get_curent_kline(self):

        klines_df = self.assets[0].get_asset_dataframe(self.start_date)

        for row in klines_df.itertuples():

            self.__manage_orders()

            self.tick += 1
            self.current_kline = Kline(tick=self.tick, open_price=row[1],
                                       high_price=row[2], low_price=row[3],
                                       close_price=row[4])

            yield row

    def get_asset_dataframe(self, start_date: str) -> pd.DataFrame:

        query = """SELECT * FROM btc_usd
                    WHERE (unix_time>%s)
                    ORDER BY unix_time ASC
                    """

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

    def place_market_order(self, order_direction, symbol, quantity):

        order_type = 'market'

        price = self.current_kline.get_average_price()

        trade = self.user.account_balance - quantity * self.history_df.at[self.tick, 'asset_price'] * (1-self.comission)

        if trade >= 0:
            order = MarketOrder(order_type=order_type,
                                quantity=quantity, asset_name=symbol,
                                execution_price=price, direction=order_direction)
            self.orders_list.append(order)
        else:
            logging.info('Not enought money')
            self.do_nothing()

    def place_limit_order(self, order_direction, symbol, quantity, price):

        order_type = 'limit'

        trade = self.user.account_balance - quantity * self.history_df.at[self.tick, 'asset_price'] * (1-self.comission)

        if trade >= 0:
            order = LimitOrder(order_type, quantity, symbol, signal_price=price, direction=order_direction)
            self.orders_list.append(order)

        else:
            logging.info('Not enought money')
            self.do_nothing()

# TODO Implement Stop loss orders
    def place_StopLoss_Order(self, order_type, direction, symbol, quantity, execution_price, stop_price):

        order_type = 'stopLoss'


        trade = self.user.account_balance - quantity * self.history_df.at[self.tick, 'asset_price']  # noqa

        if trade >= 0:

            order = StopLossOrder(quantity, symbol,
                                  execution_price=execution_price, stop_price=stop_price,
                                  direction=direction, order_type=order_type)

            self.orders_list.append(order)

        else:

            logging.info('Not enought money')
            self.do_nothing()

# TODO Implement OCO orders
    def place_OCO_order(self):
        pass

    def do_nothing(self):
        self.history_df.at[self.tick, 'asset_balance'] = self.user.asset_balance
        self.history_df.at[self.tick, 'account_balance'] = self.user.account_balance

    def get_statistics(self):

        self.history_df[['unix_time', 'asset_balance', 'account_balance']].to_csv('history.csv')
        logging.info(self.history_df.at[self.tick, 'account_balance'])

    def __manage_orders(self):

        for order in self.orders_list:

            if order.order_type == 'market':
                self.__process_market_order(order)

            elif order.order_type == 'limit':
                self.__process_limit_order(order)

            elif order.order_type == 'stop_loss':
                self.__process_StopLoss_order(order)

            elif order.order_type == 'OCO':
                self.__process_OCO_order(order)

    def __process_market_order(self, order: MarketOrder):

        self.__execute_order(order)

        self.orders_list.remove(order)

# TODO improve method
    def __process_limit_order(self, order: LimitOrder):

        if not order.is_proceed:

            if order.direction == 'sell':

                order.blocked_balance = order.quantity
                self.user.asset_balance -= order.blocked_balance

            elif order.direction == 'buy':

                blocked_balance = order.quantity * self.current_kline.get_average_price() * (1-self.comission)
                self.user.account_balance -= blocked_balance

            order.is_proceed = True

        is_executed = False

        if self.current_kline.get_average_price() > order.signal_price and order.direction == 'sell':

            self.user.asset_balance += order.blocked_balance

            market_order = MarketOrder(order.order_id, order.direction,
                                       order.quantity, order.asset_name,
                                       execution_price=order.signal_price, order_type='market')

            self.__execute_order(market_order)

            is_executed = True

        elif self.current_kline.get_average_price() < order.signal_price and order.direction == 'buy':

            self.user.account_balance += order.blocked_balance

            market_order = MarketOrder(order.order_id, order.direction, order.quantity,
                                       order.asset_name, execution_price=order.signal_price,
                                       order_type='market')

            self.__execute_order(market_order)

            is_executed = True

        if is_executed:
            self.orders_list.remove(order)

        return is_executed

# TODO implement method
    def __process_StopLoss_order(self, order: StopLossOrder):
        pass

# TODO implement method
    def __process_OCO_order(self, order: Oco_Order):
        pass

    def __execute_order(self, order: MarketOrder):

        if order.direction == 'buy':

            logging.info('Buy')
            trade = self.account_balance - order.quantity * self.history_df.at[self.tick, 'asset_price'] * (1-self.comission)  # noqa

            self.user.account_balance = trade
            self.history_df.at[self.tick, 'account_balance'] = round(self.account_balance, 2)

            self.user.asset_balance += order.quantity
            self.history_df.at[self.tick, 'asset_balance'] = round(self.asset_balance + order.quantity, 2)

        if order.direction == 'sell':

            logging.info('sell')
            trade = self.asset_balance - order.quantity

            self.user.asset_balance = trade
            self.history_df.at[self.tick, 'asset_balance'] = round(self.asset_balance, 2)

            self.user.account_balance += order.quantity * self.history_df.at[self.tick, 'asset_price'] * (1-self.comission)  # noqa
            self.history_df.at[self.tick, 'account_balance'] = round(self.account_balance, 2)
