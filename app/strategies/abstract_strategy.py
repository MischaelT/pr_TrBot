from abc import ABC, abstractmethod

from data.postgres import Postgres_db


class Base_strategy(ABC):

    """
        A base class for all strategies.
        get_prediction method must be implemented
    """

    def __init__(self) -> None:
        self.db = Postgres_db()

    @abstractmethod
    def get_prediction():
        pass
