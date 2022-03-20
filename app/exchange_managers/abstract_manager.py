from abc import ABC, abstractmethod


class Exchange_manager(ABC):

    """
        That is base class for all types of exchanges (stocks, crypto etc.). And provides several abstract methods.
    """

    @abstractmethod
    def check_connection():
        pass

    @abstractmethod
    def place_buy_order():
        pass

    @abstractmethod
    def place_sell_order():
        pass

    @abstractmethod
    def cancel_order():
        pass

    @abstractmethod
    def get_open_orders():
        pass

    @abstractmethod
    def get_asset_balance():
        pass