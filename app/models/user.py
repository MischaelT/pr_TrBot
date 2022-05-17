import utils.config as config


class User():
    def __init__(self) -> None:

        self.trading_list = config.TRADING_LIST
        self.api_key = config.API_KEY
        self.secret_key = config.SECRET_KEY
