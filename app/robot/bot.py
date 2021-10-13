from robot.abstract_bot import TradingBot
from exchange_clients.binance_client import Client
import json


class CryptoBot(TradingBot):

    __trading_list = ['BTCBUSD', 'ETHBUSD']

    def __init__(self) -> None:

        # for testing only. Then it should be implemented as geting kesys from django server
        with open('app/keys.json') as f:
            keys = json.load(f)

        api_key_from_user = keys['binance_API_key']

        self.bot_is_active = True
        self.manager = Client(api_key_from_user)
        super().__init__()

    def main(self):
        while self.bot_is_active:
            for ticker in self.__trading_list:
                print(self.manager.get_price(ticker))
