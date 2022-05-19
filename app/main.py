from bot import CryptoBot

from exchange_managers.binance_manager import BinanceManager

from models.user import User

from strategies.random_strategy import Random_strategy

from utils.config import API_KEY, SECRET_KEY

user = User()
strategy = Random_strategy()


exchange_manager = BinanceManager(api_key=API_KEY, secret_key=SECRET_KEY)

bot = CryptoBot(user, strategy, exchange_manager)

if __name__ == '__main__':

    '''DO NOT call bot.run() if exchange_manager = Binance manager'''

    bot.get_historical_data()
