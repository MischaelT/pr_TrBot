from utils.logging import logger
from bot import CryptoBot

from exchange_managers.test_manager import TestManager

from models.user import User

from strategies.random_strategy import Random_strategy

user = User()
strategy = Random_strategy()
exchange_manager = TestManager()

bot = CryptoBot(user, strategy, exchange_manager)

if __name__ == '__main__':
    logger.warning('Begins')

    logger.debug('Begins')
    bot.run()
