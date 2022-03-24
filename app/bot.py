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
        self.__trading_list = ['']
        self.__strategy = strategy

        self.__bot_is_active = True

        super().__init__()

    def run(self) -> None:

        while self.__bot_is_active:

            klines_gen = self.__manager.get_current_kline()

            for coin in self.__trading_list:
                for kline in klines_gen:

                    logging.info(kline)
                    prediction = self.__strategy.get_prediction(ticker=coin, kline=kline)

                    self.trade(prediction, coin)

                self.__manager.get_statistics()

            break

    def trade(self, prediction: str, coin) -> None:

        if prediction == 1:

            self.__manager.place_market_order(order_direction='buy', symbol=coin, quantity=1)

        elif prediction == -1:

            self.__manager.place_market_order(order_direction='sell', symbol=coin, quantity=1)

        else:

            self.__manager.do_nothing()

    def get_historical_data(self):

        if self.__manager.check_connection():
            self.__manager.save_historical_data('BTCBUSD', Client.KLINE_INTERVAL_1DAY, to_date=	1611957600, from_date=1611957600)  # noqa
        else:
            logging.info('Thats not working')
