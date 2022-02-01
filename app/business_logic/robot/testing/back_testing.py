from itertools import compress
import backtrader as bt

class RSIStrategy(bt.Strategy):

    def __init__(self) -> None:
        self.rsi = bt.indicators.RSI(self.data, period = 30)
        self.macd = bt.indicators.MACD(self.data)


    def next(self):
        if self.rsi<30 and self.macd.lines.macd<self.macd.lines.signal and not self.position:
            self.buy(size = 4)
        if self.rsi>75 and self.macd.lines.macd>self.macd.lines.signal and self.position:
            self.close()

        super().__init__()

cerebro = bt.Cerebro()

data = bt.feeds.GenericCSVData(dataname = 'app/business_logic/archive/data/4H_NEOBUSD_historical_data.csv', dtformat = 2, compression = 5, timeframe = bt.TimeFrame.NoTimeFrame)

cerebro.adddata(data)

cerebro.broker.setcash(127.0)
cerebro.broker.setcommission(0.001)

cerebro.addstrategy(RSIStrategy)

cerebro.run()

cerebro.plot()
