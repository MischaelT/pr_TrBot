from abc import ABC, abstractclassmethod


class TradingBot(ABC):

    @abstractclassmethod
    def get_predictions_by_data():
        pass
