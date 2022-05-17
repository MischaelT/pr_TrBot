import logging

import pandas as pd

import psycopg2

from utils.config import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                          POSTGRES_PORT, POSTGRES_USER)


class Postgres_db:

    """
        Class provides access to postgres database
    """

    def __init__(self) -> None:

        super().__init__()

        self.__create_table_BtcUsd()

    def get_data(self, request_text: str, params: tuple) -> list:

        """
            Method returns data from database

        Returns:
            list(tuple): requested data
        """

        return self._read(request_text, params)

    def push_data(self, query: str, params: tuple) -> None:

        """
            Method pushes data to database
        """

        self._write(query, params)

    def query_to_dataframe(self, query_result) -> pd.DataFrame:

        """
        Returns pandas dataframe from query result

        """

        columns = ('open', 'high', 'low', 'close', 'volume', 'timeframe', 'unix_time')
        df = pd.DataFrame(query_result, columns=columns)

        return df

    def __create_table_BtcUsd(self) -> None:

        """
            Method create table btc_usd if it is not exists
        """

        connection = self._make_connection()

        try:

            cursor = connection.cursor()

            create_table_query = '''CREATE TABLE IF NOT EXISTS sfdfhehdh (
                                OPEN            REAL                         NOT NULL,
                                HIGH            REAL                         NOT NULL,
                                LOW             REAL                         NOT NULL,
                                CLOSE           REAL                         NOT NULL,
                                VOLUME          REAL                         NOT NULL,
                                TIMEFRAME       TEXT                         NOT NULL,
                                UNIX_TIME       SERIAL                       NOT NULL
                                ); '''

            cursor.execute(create_table_query)

            connection.commit()

            logging.info('Table succesfully created')

        except (Exception) as exception:
            logging.exception(f'There was a problem during creating table : {str(exception)}')

        finally:
            if connection:
                cursor.close()
                connection.close()

    def _make_connection(self):

        """
            Method connecting to database using autentication data from config.py

        Returns:
           connection: Connection object
        """

        try:
            connection = psycopg2.connect(
                                        user=POSTGRES_USER,
                                        password=POSTGRES_PASSWORD,
                                        host=POSTGRES_HOST,
                                        port=POSTGRES_PORT,
                                        database=POSTGRES_DB
                                        )

        except (Exception) as exception:
            logging.exception(f'There was a problem during creating connection: {str(exception)}')

        return connection

    def _write(self, query: str, params: tuple) -> None:

        """
        Method writes data to database.

        Args:
            query (str): SQL query
            params (tuple): parameters for inserting to query
        """

        connection = self._make_connection()

        try:

            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()

        except Exception as exception:
            logging.exception(f'There was a problem during writing: {str(exception)}')

        finally:
            if connection:
                cursor.close()
                connection.close()

    def _read(self, query: str, params: tuple) -> list:

        """
            Method receives data from database

        Returns:
            list: list of tuples with requested data
        """

        connection = self._make_connection()

        record = []

        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            record = cursor.fetchall()

        except Exception as exception:
            logging.exception(f'There was a problem during reading: {str(exception)}')

        finally:
            if connection:
                cursor.close()
                connection.close()

        return record
