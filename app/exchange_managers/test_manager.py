from test.backtest_exchange import Test_exchange

from exchange_managers.abstract_manager import Exchange_manager


class TestManager(Exchange_manager):

    def __init__(self, account_balance: int, start_date: int) -> None:

        self.exchange = Test_exchange(start_date=start_date, account_balance=account_balance)

        super().__init__()

    def get_current_kline(self):
        return self.exchange.get_curent_kline()

    def check_connection(self):
        return True

    def place_limit_order(self, order_direction, symbol, quantity, price):
        self.exchange.place_limit_order(order_direction, symbol, quantity, price)

    def place_market_order(self, order_direction, symbol, quantity):
        self.exchange.place_market_order(order_direction=order_direction, symbol=symbol, quantity=quantity)

    def place_OCO_order():
        pass

    def place_StopLoss_order():
        pass

    def do_nothing(self):
        self.exchange.do_nothing()

    def get_statistics(self):
        self.exchange.get_statistics()

    def cancel_order():
        pass

    def get_open_orders():
        pass

    def get_asset_balance():
        pass
