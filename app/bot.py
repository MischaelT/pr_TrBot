import logging
from typing import Union

from binance.client import Client

from exchange_managers.binance_manager import BinanceManager
from exchange_managers.test_manager import TestManager

from models.user import User

from strategies.RSI_strategy import Rsi_strategy
from strategies.another_strategy import Another_strategy


class CryptoBot():

    def __init__(self, user: User, strategy: Union[Rsi_strategy, Another_strategy], manager: Union[BinanceManager, TestManager]) -> None:  # noqa

        self.__manager = manager
        self.__trading_list = user.trading_list
        self.__strategy = strategy

        self.__bot_is_active = True

        super().__init__()

    def run(self) -> None:

        while self.__bot_is_active:

            klines_gen = self.__manager.get_current_kline()

            try:
                for kline in klines_gen:

                    klines_gen = self.__manager.get_current_kline()
                    prediction = self.__strategy.get_prediction(ticker='', kline=kline)

                    self.trade(prediction)
                    self.__manager.get_statistics()

            except Exception as ex:
                logging.exception(ex)
                self.__bot_is_active = False

    def trade(self, prediction: str) -> None:
        prediction = -1

        if prediction == 1:
            logging.DEBUG('buy')
            self.__manager.place_buy_order(quantity=1, )

        elif prediction == -1:
            logging.DEBUG('sell')
            self.__manager.place_sell_order(quantity=1)

        else:
            logging.DEBUG('Do nothing')
            self.__manager.do_nothing()

    def get_historical_data(self):

        if self.__manager.check_connection():
            self.__manager.save_historical_data('BTCBUSD', Client.KLINE_INTERVAL_1DAY, to_date=	1611957600, from_date=1611957600)  # noqa
        else:
            logging.info('Thats not working')
