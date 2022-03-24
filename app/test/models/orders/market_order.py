from test.models.orders.base_order import BaseOrder


class MarketOrder(BaseOrder):

    def __init__(self, order_id, direction, order_type, quantity,
                 asset_name,  execution_price) -> None:

        self.direction = direction

        self.execution_price = execution_price

        super().__init__(order_id, order_type, quantity, asset_name)

    def cancel_order(self):
        return self.order_id
