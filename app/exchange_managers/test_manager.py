from test.backtest_exchange import Test_exchange
from exchange_managers.abstract_manager import Exchange_manager


class TestManager(Exchange_manager):

    def __init__(self, path_to_data:str, account_balance: int) -> None:

        self.exchange = Test_exchange(path_to_data=path_to_data, account_balance=account_balance)

        super().__init__()
    
    def get_current_kline(self):
        return self.exchange.klines_df.itertuples

    def check_connection(self):
        return True

    def place_buy_order(self, quantity):
        self.exchange.buy(quantity)
    
    def place_sell_order(self, quantity):
        self.exchange.sell(quantity)

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