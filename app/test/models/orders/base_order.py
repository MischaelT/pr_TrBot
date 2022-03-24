from abc import ABC, abstractmethod


class BaseOrder(ABC):

    def __init__(self, order_id, order_type, quantity,
                 asset_name,) -> None:

        self.order_id = order_id
        self.order_type = order_type
        self.quantity = quantity
        self.asset_name = asset_name

    @abstractmethod
    def cancel_order():
        pass
