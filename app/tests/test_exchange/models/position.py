from typing import List

from tests.test_exchange.models.kline import Kline


class Position():

    def __init__(self) -> None:

        self.klines: List[Kline] = []
        self.amounts: List[float] = 0
