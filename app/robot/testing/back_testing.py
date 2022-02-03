import backtrader as bt
from bot_indicator import Bot_indicator


class RSIStrategy(bt.Strategy):

    def __init__(self) -> None:
        self.rsi = bt.indicators.RSI(self.data.close, period=21)
        self.macd = bt.indicators.MACD(self.data)
        self.macdcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        if not self.position:
            if self.rsi[0] < 55 and self.macdcross[0] > 0.0:
                self.buy(size=10)
        else:
            if self.rsi[0] > 60 and self.macdcross[0] < 0.0:
                self.close()


class BotStrategy(bt.Strategy):
    def __init__(self) -> None:
        self.bot_advise = Bot_indicator()

    def next(self):

        if not self.position:
            if self.bot_advise[0] == 1:
                self.buy(size=120)

        elif not self.position:
            if self.bot_advise == 2:

                # Do short buy
                pass

        elif self.position:
            if self.bot_advise == -1:
                self.close()


if __name__ == '__main__':

    cerebro = bt.Cerebro()
    cerebro.addstrategy(RSIStrategy)

    data = bt.feeds.GenericCSVData(dataname='app/robot/testing/NEOBUSD_4h_1 year ago UTC.csv', dtformat=1, compression=5, timeframe=bt.TimeFrame.Days)  # noqa
    cerebro.adddata(data)

    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(0.001)

    cerebro.run()

    cerebro.plot()
