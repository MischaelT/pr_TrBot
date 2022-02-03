import sqlite3
from sqlite3.dbapi2 import Error

from data.storage.storage_manager import storage_Manager


class Db_manager(storage_Manager):

    def get_data(self) -> list:
        return self._read()

    def push_data(self, data):
        self._validate(data)
        self._write(data)

    def _write(self, data):

        try:
            con = sqlite3.connect('vacancies.db')
        except Error as e:
            pass

        cur = con.cursor()

        data_to_db = []

        for value in data.values():
            data_to_db.append(value)

        cur.execute("INSERT INTO Vacancies(title, city, info, link, remote) VALUES (?,?,?,?,?)", data_to_db)

        con.commit()

        con.close()

    def _read(self):

        try:
            con = sqlite3.connect('vacancies.db')
        except Error as _:
            pass

        cur = con.cursor()

        cur.execute("SELECT * FROM Vacancies")

        data = cur.fetchall()

        return data
