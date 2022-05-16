from abc import ABC, abstractmethod

from data.postgres import Postgres_db


class Base_strategy(ABC):

    def __init__(self) -> None:
        self.db = Postgres_db()

    @abstractmethod
    def get_prediction():
        pass
