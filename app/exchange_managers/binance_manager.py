from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from data.postgres import Postgres_db

from exchange_managers.abstract_manager import Exchange_manager

from numpy import double


# TODO Make exception handling
class BinanceManager(Exchange_manager):

    """
        That class implements abstract class Manager and provides methods for interactions with Binance API
    """

    def __init__(self, api_key, secret_key) -> None:

        """
            That method initialize an object for class BinanceManager.
            Both api keys: public and secret must be provided.
            API key can be received via your Binance acccount.

        Args:
            api_key (str): That is string that represents public key for binance API
            secret_key (str): That is string that represents private key for Binance API
        """

        self.__client = Client(api_key=api_key, api_secret=secret_key)
        self.__manager = Postgres_db()

    def check_connection(self) -> bool:

        """
            Method that implements abstract method check_connection() from base class Manager.
            It tries to connect to Binance Api.

        Returns:
            [bool]: True if connection is succesful, False if not
        """

        status = self.__client.get_system_status()

        if status == 1:
            return False

        return True

    def save_historical_data(self, symbol: str, timeframe: str, from_date: int, to_date: int) -> None:  # noqa

        """
            Connects to API, get historical data by given symbol for given period of time, and save it in storage

        Args:
            symbol (str): represents name of asset
            timeframe (str): timeframe of data (15m, 1h, 1d, 1w etc)
            from_date (int): timetamps in seconds
            to_date (int): timestamp in seconds
        """

        from_date *= 1000
        to_date *= 1000

        klines_gen = self.__client.get_historical_klines_generator(symbol, timeframe, start_str=from_date, end_str=to_date)  # noqa

        for kline in klines_gen:

            kline[0] = int(kline[0]/1000)

            for i in range(1, 6):
                kline[i] = round(float(kline[i]), 2)

            params = (kline[0], kline[1], kline[2], kline[3], kline[4], kline[5], timeframe,)

            query = '''INSERT INTO btc_usd (unix_time, open_price, high, low, close_price, volume, timeframe)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    '''

            # self.__manager.push_data(kline, file_name)  FOR CSV
            self.__manager.push_data(query, params)

    def place_buy_order(self, order_type: str, symbol: str, quantity: double,  price: str):

        if order_type == 'market':
            self.__client.order_market_buy(symbol=symbol, quantity=quantity, price=price)
        else:
            self.__client.order_limit_buy(symbol=symbol, quantity=quantity, price=price)

    def place_sell_order(self, order_type: str, symbol: str, quantity: double,  price: str):

        if order_type == 'market':
            self.__client.order_market_sell(symbol=symbol, quantity=quantity, price=price)
        else:
            self.__client.order_limit_sell(symbol=symbol, quantity=quantity, price=price)

    def place_OCO_order(self, order_direction: str, symbol: str, quantity: float, price: str, stop_price: str) -> bool:

        """
            Places OCO (one-cancel-other) order for given asset

        Args:
            order_direction (str): buy/sell
            symbol (str): name of desired asset
            quantity (float): size of order
            price (str): desired price for order
            stop_price (str): desired stop price for order

        Returns:
            [bool]: True if order was placed, false if method raized an exception
        """

        try:
            self.__client.create_oco_order(
                symbol=symbol,
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

    # TODO implement receiving an orderID inside method
    def cancel_order(self, symbol: str, OrderId: int) -> bool:

        """
            Cancel an order by given symbol

        Args:
            symbol (str): desired symbol
            OrderId (int): deprecated

        Returns:
            bool: True if cancel was succesful and False if request raised exception
        """

        try:
            self.__client.cancel_order(
                                    symbol=symbol,
                                    orderId=OrderId
                                )
        except BinanceRequestException:
            return False

        except BinanceAPIException:
            return False

        return True

    def get_open_orders(self, symbol: str) -> list:

        """
           Get all open orders for given symbol

        Args:
            symbol (str): a name of desired symbol

        Returns:
            list: list of all open orders by given symbol for account
        """

        return self.__client.get_open_orders(symbol=symbol)

    """Account functions"""
    # TODO Make function return several balanses
    def get_asset_balance(self, symbol: str = 'All') -> dict:

        """
            Gives an asset balance for given symbol

        Returns:
            [dict]: dict with balance of given symbols
        """

        account = self.__client.get_account()

        balances = account.popitem('balances')

        if symbol == 'All':
            return balances

        for item in balances.get('balances'):
            if item.get('asset') == symbol:
                return item
            else:
                return {}

    def get_statistics():
        pass
