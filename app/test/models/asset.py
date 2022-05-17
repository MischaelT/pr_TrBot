from test.models.position import Position

from data.postgres import Postgres_db

import pandas as pd


class Asset():

    def __init__(self, ticker: str, db: Postgres_db) -> None:

        self.ticker = ticker

        self.db = db

        self.position: Position = None

    def get_asset_dataframe(self, start_date: str) -> pd.DataFrame:

        query = """SELECT * FROM btc_usd
                    WHERE (unix_time>%s)
                    ORDER BY unix_time ASC
                    """

        params = (start_date,)

        query_result = self.db.get_data(query, params)

        df = self.db.query_to_dataframe(query_result)

        return df[['unix_time', 'open', 'high', 'low', 'close', 'volume']]
