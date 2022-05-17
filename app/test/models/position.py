from test.models.kline import Kline
from typing import List


class Position():

    def __init__(self) -> None:

        self.klines: List[Kline] = []
        self.amounts: List[float] = 0
