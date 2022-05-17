from random import randint

from strategies.abstract_strategy import Base_strategy


class Random_strategy(Base_strategy):

    """
        Strategy, that randomly makes prediction to sell or buy
    """

    def __init__(self) -> None:
        super().__init__()

    def get_prediction(self, ticker, kline):
        prediction = randint(-1, 1)
        return prediction
