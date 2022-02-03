from tradingview_ta.main import TA_Handler

exchange_ = 'binance'
screener_ = 'crypto'


def get_indicators(ticker, interval, indicators=[]):

    handler = TA_Handler(
        symbol=ticker,
        exchange=exchange_,
        screener=screener_,
        interval=interval,
        timeout=None
    )

    indicators = handler.get_indicators(indicators)
