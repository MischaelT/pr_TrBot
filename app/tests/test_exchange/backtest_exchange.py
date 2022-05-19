from typing import List, Union

from data.postgres import Postgres_db

from tests.configs.config import (COMISSION, TICS_NUMBER, TIMEFRAME,
                                  USER_ASSET_LIST)
from tests.test_exchange.models.asset import Asset
from tests.test_exchange.models.kline import Kline
from tests.test_exchange.models.orders.limit_order import LimitOrder
from tests.test_exchange.models.orders.market_order import MarketOrder
from tests.test_exchange.models.orders.oco_order import Oco_Order
from tests.test_exchange.models.orders.stopLimit_order import StopLimitOrder
from tests.test_exchange.models.user import User

from utils.logging import logger


class Test_exchange():

    """
        Class that imitates flow of exchange on historacal data from database

    """

    # TODO implement trading with different assets

    def __init__(self) -> None:

        self.db: Postgres_db = Postgres_db()

        self.orders_list: List[Union[StopLimitOrder, MarketOrder, Oco_Order, LimitOrder]] = []
        self.assets: List[Asset] = []

        self.user = User()

        self.one_tick = 0
        self.current_time = 0
        self.current_kline: Kline = None
        self.tick_number = 0

        self.comission = COMISSION

        # Function call order matters
        self.__initialize_timeframe()
        self.__initialize_assets()
        self.__initialize_start_date()

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

    def place_market_order(self, order_direction, ticker, quantity):

        order_type = 'market'

        price = self.current_kline.get_average_price()

        not_null_balance = self.__is_not_null_balance(ticker, direction=order_direction, quantity=quantity, price=price)

        if not_null_balance:

            order = MarketOrder(order_type=order_type,
                                quantity=quantity, asset_name=ticker,
                                execution_price=price, direction=order_direction)
            self.orders_list.append(order)

        else:
            logger.info('Not enought money')
            self.do_nothing()

    def place_limit_order(self, order_direction, ticker, quantity, price):

        order_type = 'limit'

        not_null_balance = self.__is_not_null_balance(ticker, direction=order_direction, quantity=quantity)

        if not_null_balance:
            order = LimitOrder(order_type, quantity, ticker, signal_price=price, direction=order_direction)
            self.__block_balance(order)
            self.orders_list.append(order)

        else:
            logger.info('Not enought money')
            self.do_nothing()

    def place_stopLimit_order(self, order_type, direction, ticker, quantity, execution_price, stop_price):

        order_type = 'stopLoss'

        not_null_balance = self.__is_not_null_balance(ticker, direction=direction, quantity=quantity, price=execution_price)  # noqa

        if not_null_balance:

            order = StopLimitOrder(quantity, ticker,
                                   execution_price=execution_price, stop_price=stop_price,
                                   direction=direction, order_type=order_type)

            self.__block_balance(order)

            self.orders_list.append(order)

        else:

            logger.info('Not enought money')
            self.do_nothing()

# TODO Implement OCO orders
    def place_OCO_order(self):
        pass

    def do_nothing(self):
        self.user.history_df.at[self.tick_number, 'asset_balance'] = self.user.asset_balance
        self.user.history_df.at[self.tick_number, 'account_balance'] = self.user.account_balance

# TODO implement cancelling OCO order
    def cancel_order(self, order_id):

        for order in self.orders_list:

            if order.order_id == order_id:
                self.__unblock_balance(order)
                self.orders_list.remove(order)
                cancelled_order_id = order.cancel_order()

            logger.info(cancelled_order_id)

    def get_statistics(self):
        statistics = {}
        statistics['profit'] = self.user.get_profit()
        return statistics

    def __initialize_timeframe(self):

        if TIMEFRAME == '1H':
            self.one_tick = 3600
        elif TIMEFRAME == '4H':
            self.one_tick = 3600*4
        elif TIMEFRAME == '1D':
            self.one_tick = 3600*24

    def __initialize_assets(self):

        trade_assets = USER_ASSET_LIST

        for ticker in trade_assets:

            asset = Asset(ticker=ticker, db=self.db)
            self.assets.append(asset)

# TODO Fix time getting system
    def __initialize_start_date(self):

        query = ''' SELECT unix_time FROM btc_usd
                    ORDER BY unix_time DESC
                    LIMIT 1'''

        current_time = self.db.get_data(query, params=())

        current_time = 1647820800

        self.current_time = current_time - self.one_tick*(TICS_NUMBER-1)

    def __is_not_null_balance(self, ticker, direction, quantity, price) -> bool:

        """
            Method checks if it is possible to buy or sell asset.

        Returns:
            bool: True if balance after deal>0, False if balance<0
        """

        if direction == 'buy':
            balance = self.user.account_balance - quantity * price * (1+self.comission)
        elif direction == 'sell':
            balance = self.user.asset_balance - quantity

        if balance > 0:
            return True

        return False

    def __manage_orders(self):

        for order in self.orders_list:

            if order.order_type == 'market':
                self.__process_market_order(order)

            elif order.order_type == 'limit':
                self.__process_limit_order(order)

            elif order.order_type == 'stop_loss':
                self.__process_stopLimit_order(order)

            elif order.order_type == 'OCO':
                self.__process_OCO_order(order)

    def __block_balance(self, order: Union[LimitOrder, StopLimitOrder, Oco_Order]):

        if order.direction == 'sell':

            order.blocked_balance = order.quantity
            self.user.asset_balance -= order.blocked_balance

        elif order.direction == 'buy':

            order.blocked_balance = order.quantity * self.current_kline.get_average_price() * (1-self.comission)
            self.user.account_balance -= order.blocked_balance

    def __unblock_balance(self, order: Union[LimitOrder, StopLimitOrder, Oco_Order]):

        if order.direction == 'sell':

            self.user.asset_balance += order.blocked_balance

        elif order.direction == 'buy':

            self.user.account_balance += order.blocked_balance

    def __process_market_order(self, order: MarketOrder):

        self.__execute_order(order)

        self.orders_list.remove(order)

    def __process_limit_order(self, order: LimitOrder):

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

    def __process_stopLimit_order(self, order: StopLimitOrder):

        is_executed = False

        if self.current_kline.get_average_price() > order.stop_price and order.direction == 'sell':

            limit_order = LimitOrder(order_type='limit', quantity=order.quantity, asset_name=order.asset_name,
                                     direction='sell', signal_price=order.execution_price)

            self.orders_list.append(limit_order)

            is_executed = True

        elif self.current_kline.get_average_price() < order.stop_price and order.direction == 'buy':

            limit_order = LimitOrder(order_type='limit', quantity=order.quantity, asset_name=order.asset_name,
                                     direction='buy', signal_price=order.execution_price)

            self.orders_list.append(limit_order)

            is_executed = True

        if is_executed:
            self.orders_list.remove(order)

        return is_executed

# TODO implement method
    def __process_OCO_order(self, order: Oco_Order):
        pass

    def __execute_order(self, order: MarketOrder):

        price = self.current_kline.get_average_price()

        if order.direction == 'buy':

            logger.info('Buy')
            trade = self.user.account_balance - order.quantity * price * (1+self.comission)  # noqa

            self.user.account_balance = trade
            self.user.history_df.at[self.tick_number, 'account_balance'] = round(self.user.account_balance, 2)

            self.user.asset_balance += order.quantity
            self.user.history_df.at[self.tick_number, 'asset_balance'] = round(self.user.asset_balance + order.quantity, 2)  # noqa

        if order.direction == 'sell':

            logger.info('sell')
            trade = self.user.asset_balance - order.quantity

            self.user.asset_balance = trade
            self.user.history_df.at[self.tick_number, 'asset_balance'] = round(self.user.asset_balance, 2)

            self.user.account_balance += order.quantity * price * (1-self.comission)  # noqa
            self.user.history_df.at[self.tick_number, 'account_balance'] = round(self.user.account_balance, 2)
