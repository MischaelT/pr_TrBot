import requests


class Client():

    # Current URL is for test trading only. For real you should replace it by https://api.binance.com/api
    endpoint_url = 'https://testnet.binance.vision'

    def __init__(self, key) -> None:
        self.api_key = key

    # Нужна ли проверка? Она ощутимо замедляет работу.
    # Что лучше возвращать из функции?
    def get_price(self, symbol) -> str:

        test_connection_path = self.endpoint_url+'/api/v3/ping'

        if len(requests.get(test_connection_path).json()) == 0:
            path = '/api/v3/ticker/price'
            url = self.endpoint_url+path
            data = {'symbol': symbol}

            response = requests.get(url, params=data)
            response.raise_for_status()
        else:
            response = 'something is wrong with connection'

        return(response.json()['price'])

    def make_order(symbol, type, side, order_id):
        pass

    def cancel_order(symbol, orderId, order_id, all=False):
        pass

    def make_OCO_order(symbol, side, quantity, price, stop_price):
        pass

    def cancel_OCO_order(symbol, order_id):
        pass
