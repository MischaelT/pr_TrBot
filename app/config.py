from environs import Env

env = Env()
env.read_env()

API_KEY = env.str('API_KEY')
SECRET_KEY = env.str('SECRET_KEY')
TRADING_LIST = env.list('TRADING_LIST')
