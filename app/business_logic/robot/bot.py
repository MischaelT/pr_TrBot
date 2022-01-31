from exchange_managers.binance_manager import BinanceManager
from robot.abstract_bot import TradingBot
from archive.ta_archive_manager import clean_data

import json


class CryptoBot(TradingBot):

    __trading_list = ['BTCBUSD', 'ETHBUSD']

    def __init__(self) -> None:

        # for testing only. Then it should be implemented as geting kesys from django server
        with open('app/keys.json') as f:
            keys = json.load(f)

        self.bot_is_active = True
        self.manager = BinanceManager(keys)
        super().__init__()

    def main(self):
        path_to_data = 'app/business_logic/archive/data/4H_NEOBUSD_historical_data.csv'
        self.manager.save_historical_data(path_to_data)
        
