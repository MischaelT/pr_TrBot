from bot import CryptoBot

from exchange_managers.test_manager import TestManager

from models.user import User

from strategies.RSI_strategy import Rsi_strategy

user = User()
strategy = Rsi_strategy()
exchange_manager = TestManager(account_balance=10000000, start_date=1599436800)

bot = CryptoBot(user, strategy, exchange_manager)

if __name__ == '__main__':
    bot.run()
