from bot import CryptoBot

from exchange_managers.test_manager import TestManager

from models.user import User

from strategies.RSI_strategy import Rsi_strategy
from strategies.random_strategy import Random_strategy


def test_Strategy():

    tested_strategy = Rsi_strategy()

    exchange_manager = TestManager()
    user = User()

    bot = CryptoBot(user, tested_strategy, exchange_manager)
    bot.run()

    strategy_profit = user.statistics['profit']

    assert strategy_profit > 0

    strategy = Random_strategy()

    bot = CryptoBot(user, strategy, exchange_manager)
    bot.run()

    randomStrategy_profit = user.statistics['profit']

    assert strategy_profit > randomStrategy_profit
