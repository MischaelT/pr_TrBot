from exchange_managers.manager import Manager
from binance.client import Client
import csv


class BinanceManager(Manager):

    def __init__(self, keys) -> None:

        self.client = Client(keys['binance_API_key'], keys['binance_API_key'])

    def save_historical_data(self, path, ticker='NEOBUSD', interval=Client.KLINE_INTERVAL_1DAY, from_date='4 month ago UTC'):  # noqa

        with open(path, 'w', newline='') as csvfile:
            candlestick_writer = csv.writer(csvfile, delimiter=',')

            candles = self.client.get_historical_klines(ticker, interval, from_date)

            for candle in candles:
                candlestick_writer.writerow(candle)
