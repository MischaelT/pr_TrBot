from strategies.abstract_strategy import Base_strategy


class Test_strategy(Base_strategy):

    """
        Strategy class for testing test exchange
    """

    def __init__(self, test_mode) -> None:

        super().__init__()

    def get_prediction(self, ticker: str, kline: str) -> str:

        pass
