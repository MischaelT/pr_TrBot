import backtrader as bt

from ..bot import CryptoBot


class Bot_indicator():
    
    """
    This class represents a backtrader indicator,based on class Crypto bot
    """

    lines = ('advise',)

    def __init__(self) -> None:

        path_to_data = ''
        self.lines.advise = CryptoBot.get_predictions_by_data(path_to_data)
