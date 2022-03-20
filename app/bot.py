import logging
from typing import Union

from binance.client import Client
from exchange_managers.test_manager import TestManager
from strategies.RSI_strategy import Rsi_strategy
from strategies.another_strategy import Another_strategy
from models.user import User

from exchange_managers.binance_manager import BinanceManager


class CryptoBot():

    def __init__(self, user: User, strategy: Union[Rsi_strategy, Another_strategy], manager: Union[BinanceManager, TestManager]) -> None:

        self.__manager = manager
        self.__trading_list = user.trading_list
        self.__strategy = strategy

        self.__bot_is_active = True

        super().__init__()


    def run(self) -> None:

        # prediction = self.__strategy.get_prediction(ticker = '', timeframe='1h')


        klines_gen = self.__manager.get_current_kline()

        for kline in klines_gen():
            print(kline[1])

        while self.__bot_is_active:
            pass
            

    def trade(self, prediction: str) -> None:

        if prediction == 'buy':
            self.__manager.place_buy_order(quantity=1)

        elif prediction == 'sell':
            self.__manager.place_sell_order(quantity=1)

        else:
            self.__manager.do_nothing() 


    def get_historical_data(self):

        if self.__manager.check_connection():
            file_name = 'BTCBUSD' + '_' + Client.KLINE_INTERVAL_1DAY + '_' + '499 days ago UTC'
            self.__manager.save_historical_data('BTCBUSD', Client.KLINE_INTERVAL_1DAY, '499 days ago UTC', file_name=file_name)  # noqa
        else:
            logging.info('Thats not working')
