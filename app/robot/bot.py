import logging

from binance.client import Client

import config

from exchange_managers.binance_manager import BinanceManager

from robot.abstract_bot import TradingBot


class CryptoBot(TradingBot):

    def __init__(self) -> None:

        self.__bot_is_active = True
        self.__manager = BinanceManager(config.API_KEY, config.SECRET_KEY)

        self.__trading_list = config.TRADING_LIST

        super().__init__()

    def main(self) -> None:

        while self.__bot_is_active:
            pass

    def get_historical_data(self):

        if self.__manager.check_connection():
            file_name = 'BTCBUSD' + '_' + Client.KLINE_INTERVAL_1DAY + '_' + '499 days ago UTC'
            self.__manager.save_historical_data('BTCBUSD', Client.KLINE_INTERVAL_1DAY, '499 days ago UTC', file_name=file_name)  # noqa
        else:
            logging.info('Thats not working')
