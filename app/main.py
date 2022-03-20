from exchange_managers.binance_manager import BinanceManager
from exchange_managers.test_manager import TestManager
from strategies.RSI_strategy import Rsi_strategy
from models.user import User
from bot import CryptoBot

user = User()
strategy = Rsi_strategy()
exchange_manager = BinanceManager(user.api_key, user.secret_key)
# exchange_manager = TestManager(path_to_data = 'app/data/view_managers/csv/BTCBUSD_1d_499 days ago UTC.csv',
#                                         account_balance=100000)

bot = CryptoBot(user, strategy, exchange_manager)

if __name__ == '__main__':
    bot.get_historical_data()
