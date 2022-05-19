from exchange_managers.abstract_manager import Exchange_manager

from tests.test_exchange.backtest_exchange import Test_exchange


class TestManager(Exchange_manager):

    """
        Class TestManager is exchange manager for testing and provides methods for interaction with TestExchange
    """

    def __init__(self) -> None:

        self.exchange = Test_exchange()

        super().__init__()

    def get_current_kline(self):
        return self.exchange.tick_generator()

    def check_connection(self):
        return True

    def place_limit_order(self, order_direction, symbol, quantity, price):
        self.exchange.place_limit_order(order_direction, symbol, quantity, price)

    def place_market_order(self, order_direction, symbol, quantity):
        self.exchange.place_market_order(order_direction=order_direction, ticker=symbol, quantity=quantity)

    def place_OCO_order(self):
        pass

    def place_stopLimit_order(self):
        self.exchange.place_stopLimit_order()

    def do_nothing(self):
        self.exchange.do_nothing()

    def cancel_order(self, order_id):
        self.cancel_order(order_id)

    def get_open_orders(self):
        pass

    def get_asset_balance(self):
        pass

    def get_statistics(self):

        """
        print user statistics for test
        """
        return self.exchange.get_statistics()
