from strategies.abstract_strategy import Base_strategy


class Rsi_strategy(Base_strategy):

    def __init__(self) -> None:
        super().__init__()

    def get_prediction(self, ticker: str, kline: str) -> str:
        pass
