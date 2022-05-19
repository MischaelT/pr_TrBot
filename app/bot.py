import logging
from typing import Union

from binance.client import Client

from exchange_managers.binance_manager import BinanceManager
from exchange_managers.test_manager import TestManager

from models.user import User

from strategies.RSI_strategy import Rsi_strategy
from strategies.random_strategy import Random_strategy
from strategies.test_strategy import Test_strategy


class CryptoBot():

    def __init__(self, user: User, strategy: Union[Rsi_strategy, Random_strategy, Test_strategy], manager: Union[BinanceManager, TestManager]) -> None:  # noqa

        self.__manager = manager
        self.__trading_list = user.trading_list
        self.__strategy = strategy
        self.user = user

        self.__bot_is_active = True

        super().__init__()

    def run(self) -> None:

        """
            Primary method, that takes a prediction from strategy and
            then call the method for placing orders to exchange.
        """

        while self.__bot_is_active:

            klines_gen = self.__manager.get_current_kline()

            for ticker in self.__trading_list:

                for kline in klines_gen:

                    logging.info(kline)

                    prediction = self.__strategy.get_prediction(ticker=ticker, kline=kline)

                    self.trade(prediction, ticker)

            break

        self.user.statistics = self.__manager.get_statistics()

    def trade(self, prediction: str, coin: str) -> None:

        """
        Method that place orders to exchange based on prediction
        -1 -- sell
        1 -- buy
        """

        if prediction == 1:

            logging.info('Buy')
            self.__manager.place_market_order(order_direction='buy', symbol=coin, quantity=1)

        elif prediction == -1:

            logging.info('Sell')
            self.__manager.place_market_order(order_direction='sell', symbol=coin, quantity=10)

        else:

            logging.info('Do nothing')
            self.__manager.do_nothing()

    def get_historical_data(self):

        """
            Method that extracts a trade data from binance. It will NOT WORK if manager is TestManager (main.py)
        """

        if self.__manager.check_connection():
            self.__manager.save_historical_data('BTCBUSD', Client.KLINE_INTERVAL_1DAY, to_date=	1611957600, from_date=1611957600)  # noqa
        else:
            logging.info('Thats not working')
