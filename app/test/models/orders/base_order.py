from abc import ABC, abstractmethod
import uuid


class BaseOrder(ABC):

    def __init__(self, order_type, quantity,
                 asset_name,) -> None:

        self.order_id = uuid.uuid4()
        self.order_type = order_type
        self.quantity = quantity
        self.asset_name = asset_name

    @abstractmethod
    def cancel_order():
        pass
