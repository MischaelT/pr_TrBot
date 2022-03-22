class Order:

    def __init__(self, order_id, order_type, quantity,
                 asset_name, direction, order_execution_price, order_signal_price=0) -> None:

        self.order_id = order_id
        self.order_type = order_type
        self.quantity = quantity
        self.asset_name = asset_name
        self.direction = direction
        self.execution_price = order_execution_price
        self.signal_price = order_signal_price
        self.is_proceed = False
