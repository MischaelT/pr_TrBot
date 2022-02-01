from exchange_managers.binance_manager import BinanceManager
from robot.abstract_bot import TradingBot
from business_logic import config

import json


class CryptoBot(TradingBot):

    def __init__(self) -> None:

        self.__bot_is_active = True
        self.__manager = BinanceManager(config.API_KEY, config.SECRET_KEY)
        
        self.__trading_list = config.TRADING_LIST

        super().__init__()

    def main(self):
        while self.__bot_is_active:
            pass
        
