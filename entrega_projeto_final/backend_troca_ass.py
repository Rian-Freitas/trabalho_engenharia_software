import sqlite3

class conexaoFactory:
    _instance = None

    def __new__(cls, nome_database):
        if cls._instance is None:
            cls._instance = super(conexaoFactory, cls).__new__(cls)
            cls._instance._conexao = sqlite3.connect(nome_database)
            cls._instance._cursor = cls._instance._conexao.cursor()
        return cls._instance

    def get_conexao(self):
        return self._conexao

class FacadeDB:
    def __init__(self, factory_conexao):
        self._factory_conexao = factory_conexao

    def executa_query(self, query):
        conexao = self._factory_conexao.get_conexao()
        cursor = conexao.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado

    def executa_update(self, query):
        conexao = self._factory_conexao.get_conexao()
        cursor = conexao.cursor()
        cursor.execute(query)
        conexao.commit()
        cursor.close()
