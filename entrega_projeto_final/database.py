import sqlite3

class Database:
    _instance = None

    def __new__(cls):
        if Database._instance is None:
            Database._instance = object.__new__(cls)
        return Database._instance

    def __init__(self):
        self.conn = sqlite3.connect("entrega_projeto_final\database.db")
        self.cursor = self.conn.cursor()

