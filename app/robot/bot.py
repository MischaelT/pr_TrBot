from exchange_managers.binance_manager import BinanceManager
from robot.abstract_bot import TradingBot
import config
from binance.client import Client


class CryptoBot(TradingBot):

    @classmethod
    def get_predictions_by_data(data):
        pass

    def __init__(self) -> None:

        self.__bot_is_active = True
        self.__manager = BinanceManager(config.API_KEY, config.SECRET_KEY)

        self.__trading_list = config.TRADING_LIST

        super().__init__()

    def main(self) -> None:

        while self.__bot_is_active:
            pass

    def get_historical_data(self):

        if self.__manager.check_status:
            file_name = 'NEOBUSD' + '_' + Client.KLINE_INTERVAL_4HOUR + '_' + '3 year ago UTC'
            self.__manager.save_historical_data('NEOBUSD', Client.KLINE_INTERVAL_1DAY, '3 year ago UTC', file_name=file_name)  # noqa
        else:
            print('Thats not working')
