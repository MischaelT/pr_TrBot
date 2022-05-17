import logging
from test.models.asset import Asset
from test.models.kline import Kline
from test.models.orders.limit_order import LimitOrder
from test.models.orders.market_order import MarketOrder
from test.models.orders.oco_order import Oco_Order
from test.models.orders.stopLoss_order import StopLossOrder
from test.models.user import User
from test.test_config import COMISSION, TICS_NUMBER, TIMEFRAME, USER_ASSET_LIST
from typing import List, Union

from data.postgres import Postgres_db


class Test_exchange():

    # TODO implement trading with different assets

    def __init__(self) -> None:

        self.db: Postgres_db = Postgres_db()

        self.orders_list: List[Union[StopLossOrder, MarketOrder, Oco_Order, LimitOrder]] = []
        self.assets: List[Asset] = []

        self.user = User()

        self.one_tick = 0
        self.current_time = 0
        self.current_kline: Kline = None
        self.tick_number = 0

        self.comission = COMISSION

        # Function call order matters
        self.initialize_timeframe()
        self.initialize_assets()
        self.initialize_start_date()

    def initialize_timeframe(self):

        if TIMEFRAME == '1H':
            self.one_tick = 3600
        elif TIMEFRAME == '4H':
            self.one_tick = 3600*4
        elif TIMEFRAME == '1D':
            self.one_tick = 3600*24

    def initialize_assets(self):

        trade_assets = USER_ASSET_LIST

        for ticker in trade_assets:

            asset = Asset(ticker=ticker, db=self.db)
            self.assets.append(asset)

    # TODO Fix getting time system
    def initialize_start_date(self):

        query = ''' SELECT unix_time FROM btc_usd
                    ORDER BY unix_time DESC
                    LIMIT 1'''

        current_time = self.db.get_data(query, params=())

        current_time = 1647820800

        self.current_time = current_time - self.one_tick*(TICS_NUMBER-1)

    def tick_generator(self):

        while (self.tick_number < TICS_NUMBER):

            self.__manage_orders()

            query = """SELECT * FROM btc_usd
                        WHERE (unix_time=%s)
                        ORDER BY unix_time ASC
                        """

            params = (self.current_time,)

            row = self.db.get_data(query, params)[0]

            self.current_kline = Kline(tick=self.tick_number, open_price=row[0],
                                       high_price=row[1], low_price=row[2],
                                       close_price=row[3])

            yield row

            self.tick_number += 1
            self.current_time += self.one_tick

    # TODO Fix checking user balances
    def place_market_order(self, order_direction, symbol, quantity):

        order_type = 'market'

        price = self.current_kline.get_average_price()

        trade = self.user.account_balance - quantity * price * (1+self.comission)

        if order_direction == 'buy':
            trade = self.user.account_balance - quantity * price * (1+self.comission)
        elif order_direction == 'sell':
            trade = self.user.asset_balance - quantity

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

        price = self.current_kline.get_average_price()

        trade = self.user.account_balance - quantity * price * (1+self.comission)

        if trade >= 0:
            order = LimitOrder(order_type, quantity, symbol, signal_price=price, direction=order_direction)
            self.orders_list.append(order)

        else:
            logging.info('Not enought money')
            self.do_nothing()

# TODO Implement Stop loss orders
    def place_StopLoss_Order(self, order_type, direction, symbol, quantity, execution_price, stop_price):

        order_type = 'stopLoss'


        trade = self.user.account_balance - quantity * self.user.history_df.at[self.tick_number, 'asset_price']  # noqa

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
        self.user.history_df.at[self.tick_number, 'asset_balance'] = self.user.asset_balance
        self.user.history_df.at[self.tick_number, 'account_balance'] = self.user.account_balance

    def get_statistics(self):
        self.user.get_statistics()

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

        price = self.current_kline.get_average_price()

        if order.direction == 'buy':

            logging.info('Buy')
            trade = self.user.account_balance - order.quantity * price * (1+self.comission)  # noqa

            self.user.account_balance = trade
            self.user.history_df.at[self.tick_number, 'account_balance'] = round(self.user.account_balance, 2)

            self.user.asset_balance += order.quantity
            self.user.history_df.at[self.tick_number, 'asset_balance'] = round(self.user.asset_balance + order.quantity, 2)  # noqa

        if order.direction == 'sell':

            logging.info('sell')
            trade = self.user.asset_balance - order.quantity

            self.user.asset_balance = trade
            self.user.history_df.at[self.tick_number, 'asset_balance'] = round(self.user.asset_balance, 2)

            self.user.account_balance += order.quantity * price * (1-self.comission)  # noqa
            self.user.history_df.at[self.tick_number, 'account_balance'] = round(self.user.account_balance, 2)
