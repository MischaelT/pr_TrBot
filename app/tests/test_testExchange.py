from bot import CryptoBot

from exchange_managers.test_manager import TestManager

from models.user import User

from strategies.random_strategy import Random_strategy


# TODO Implement test exchange testing
def test_market_orders():

    strategy = Random_strategy()
    exchange_manager = TestManager()
    user = User()

    bot = CryptoBot(user, strategy, exchange_manager)

    bot.run()

    assert user.statistics['profit'] > 0
