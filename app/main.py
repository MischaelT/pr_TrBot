from strategies.random_strategy import Random_strategy
from bot import CryptoBot

from exchange_managers.test_manager import TestManager

from models.user import User


user = User()
strategy = Random_strategy()
exchange_manager = TestManager()

bot = CryptoBot(user, strategy, exchange_manager)

if __name__ == '__main__':
    bot.run()
