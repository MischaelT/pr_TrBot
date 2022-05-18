from test.models.orders.base_order import BaseOrder


class LimitOrder(BaseOrder):

    def __init__(self, order_type, quantity,
                 asset_name, direction, signal_price) -> None:


        self.signal_price = signal_price

        self.blocked_balance = 0

        super().__init__(order_type, quantity, asset_name, direction)

    def cancel_order(self):
        return self.order_id
