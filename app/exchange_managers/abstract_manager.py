from abc import ABC, abstractmethod


class Exchange_manager(ABC):

    """
        That is base class for all types of exchanges (stocks, crypto etc.). And provides several abstract methods.
    """

    @abstractmethod
    def check_connection():
        pass

    @abstractmethod
    def place_limit_order():
        pass

    @abstractmethod
    def place_market_order():
        pass

    @abstractmethod
    def place_OCO_order():
        pass

    @abstractmethod
    def place_stopLimit_order():
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
