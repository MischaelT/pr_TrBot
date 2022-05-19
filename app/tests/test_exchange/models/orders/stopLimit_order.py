from tests.test_exchange.models.orders.base_order import BaseOrder


class StopLimitOrder(BaseOrder):

    def __init__(self, order_type, quantity,
                 asset_name, direction, execution_price, stop_price, blocked_balance) -> None:

        self.execution_price = execution_price
        self.stop_price = stop_price

        self.blocked_balance = blocked_balance

        super().__init__(order_type, quantity, asset_name, direction)

    def cancel_order(self):
        return self.order_id
