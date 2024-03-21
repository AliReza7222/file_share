import os
import sqlite3

from colorama import Fore
from utils.output_input import _print


class DataBase:

    def __init__(self):
        self.name_db = 'sqlite3.db'

    def create_db(self):
        if not self.check_exists_db():
            _print(f'Database sqlite3 created ✔', Fore.GREEN)
            self.add_table()

    def check_exists_db(self):
        return os.path.exists(self.name_db)

    def talk_to_database(self, connect: bool = False, close: bool = False):
        if connect:
            self.connect_db = sqlite3.connect(self.name_db)
            return self.connect_db.cursor()
        elif close:
            if hasattr(self, 'connect_db'):
                self.connect_db.close()

    def create_table(self, table_name: str, columns: str):
        cursor = self.talk_to_database(connect=True)
        columns = 'id INTEGER PRIMARY KEY AUTOINCREMENT, ' + columns
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        )
        self.talk_to_database(close=True)

    def insert_data(self, table_name: str, columns: str, data: str):
        cursor = self.talk_to_database(connect=True)
        cursor.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES ({data})"
        )
        self.connect_db.commit()
        self.talk_to_database(close=True)

    def delete_data(self, table_name: str, data: str, column: str):
        cursor = self.talk_to_database(connect=True)
        cursor.execute(
            f"DELETE FROM {table_name} WHERE {column}=\'{data}\'"
        )
        self.connect_db.commit()
        self.talk_to_database(close=True)

    def select_data(self, table_name: str, column: str, condition: str = None):
        cursor = self.talk_to_database(connect=True)
        if condition:
            rows = cursor.execute(
                f"SELECT {column} FROM {table_name} WHERE {condition}"
            ).fetchall()
        else:
            rows = cursor.execute(
                f"SELECT {column} FROM {table_name}"
            ).fetchall()
        self.talk_to_database(close=True)
        return rows

    @staticmethod
    def tables():
        tables = {
            'black_list': 'ip TEXT',
            'media': 'name TEXT UNIQUE, file TEXT'
        }
        return tables

    def add_table(self):
        for table_name, columns in self.tables().items():
            self.create_table(table_name, columns)
            _print(f'Table {table_name} created ✔', Fore.GREEN)


db = DataBase()
db.create_db()
