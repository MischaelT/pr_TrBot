from test.models.orders.base_order import BaseOrder


class StopLossOrder(BaseOrder):

    def __init__(self, order_id, order_type, quantity,
                 asset_name, direction, execution_price, stop_price, blocked_amount) -> None:

        self.direction = direction

        self.execution_price = execution_price
        self.stop_price = stop_price
        self.blocked_asset_amount = blocked_amount

        super().__init__(order_id, order_type, quantity, asset_name)

    def cancel_order(self):
        return (self.order_id, self.blocked_asset_amount)
