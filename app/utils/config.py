from environs import Env

env = Env()
env.read_env()

API_KEY = env.str('API_KEY')
SECRET_KEY = env.str('SECRET_KEY')
TRADING_LIST = env.list('TRADING_LIST')

POSTGRES_DB = env.str('POSTGRES_DB')
POSTGRES_HOST = env.str('POSTGRES_HOST')
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')
POSTGRES_PORT = env.str('POSTGRES_PORT')
POSTGRES_USER = env.str('POSTGRES_USER')
