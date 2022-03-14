from abc import ABC, abstractmethod


class Manager(ABC):

    """
        That is base class for all types of exchanges (stocks, crypto etc.). And provides several abstract methods.
    """

    @abstractmethod
    def check_connection():
        pass
