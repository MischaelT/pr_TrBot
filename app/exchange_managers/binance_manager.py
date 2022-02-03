from numpy import double
from data.storage.csv_manager import Csv_manager
from exchange_managers.manager import Manager
from binance.client import Client

from binance.exceptions import BinanceAPIException, BinanceRequestException


# TODO Make exception handling
class BinanceManager(Manager):

    def __init__(self, api_key, secret_key) -> None:

        self.__client = Client(api_key=api_key, api_secret=secret_key)
        # self.__manager = Db_manager()
        self.__manager = Csv_manager()

    def check_status(self) -> bool:

        status = self.__client.get_system_status()

        if status == 1:
            return False

        return True

    def save_historical_data(self, ticker: str, interval: str, from_date: str, file_name) -> None:  # noqa

        for kline in self.__client.get_historical_klines_generator(ticker, interval, from_date):
            kline[0] = int(kline[0]/1000)
            self.__manager.push_data(kline, file_name)

# TODO Make method simplier
    def place_an_order(self, order_type: str, order_direction: str, ticker: str, quantity: double,  price: str) -> bool:

        if order_type == 'market':

            if order_direction == 'buy':

                self.__client.order_market_buy(symbol=ticker, quantity=quantity, price=price)
                return True

            self.__client.order_market_sell(symbol=ticker, quantity=quantity, price=price)
            return True

        elif order_type == 'limit':

            if order_direction == 'buy':

                self.__client.order_limit_buy(symbol=ticker, quantity=quantity, price=price)
                return True

            self.__client.order_limit_sell(symbol=ticker, quantity=quantity, price=price)
            return True

        else:
            return False

    def place_OCO_order(self, order_direction: str, ticker: str, quantity: double, price: str, stop_price: str) -> None:

        try:
            self.__client.create_oco_order(
                symbol=ticker,
                side=order_direction,
                stopLimitTimeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=quantity,
                stopPrice=stop_price,
                price=price
            )

        except BinanceRequestException:
            return False

        except BinanceAPIException:
            return False

        return True

    def cancel_an_order(self, ticker: str, OrderId: int) -> None:
        self.__client.cancel_order(
                                symbol=ticker,
                                orderId=OrderId
                            )

    def get_open_orders(self, ticker) -> list:
        return self.__client.get_open_orders(symbol=ticker)

    """Account functions"""

    def get_asset_balance(self, ticker: str = 'All') -> dict:
        account = self.__client.get_account()

        balances = account.popitem('balances')

        if ticker == 'All':
            return balances

        for item in balances.get('balances'):
            if item.get('asset') == ticker:
                return item
            else:
                return {}
