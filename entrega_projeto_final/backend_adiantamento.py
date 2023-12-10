import sqlite3
from datetime import datetime, timedelta

class DatabaseConnection:
    _instance = None

    def __new__(cls, database):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect(database)
        return cls._instance.connection

class LazyProxyFacade:
    def __init__(self, database):
        self.database = database
        self._conn = None

    @property
    def connection(self):
        if not self._conn:
            self._conn = DatabaseConnection(self.database)
        return self._conn

    def executa_query(self, query, parametros=None):
        cursor = self.connection.cursor()
        cursor.execute(query, parametros)
        return cursor

class AdiantamentoHandler:
    def __init__(self, facade=None):
        self.facade = facade
        self.proximo_handler = None

    def define_proximo_handler(self, handler):
        self.proximo_handler = handler
        return handler

    def requerimento_handle(self, *args, **kwargs):
        if self.proximo_handler:
            return self.proximo_handler.requerimento_handle(*args, **kwargs)

class ArtistaIdHandler(AdiantamentoHandler):
    def requerimento_handle(self, email_artista):
        if self.facade:
            cursor = self.facade.executa_query("SELECT cod_artista FROM artista WHERE email_artista = ?", (email_artista,))
            id_artista = cursor.fetchone()
            if id_artista:
                return id_artista[0]
        return None

class ObraIdHandler(AdiantamentoHandler):
    def requerimento_handle(self, id_artista):
        if self.facade:
            cursor = self.facade.executa_query("SELECT obra_cod_obra FROM relacao_artista_obra WHERE artista_cod_artista = ?", (id_artista,))
            artworks = cursor.fetchall()
            return [artwork[0] for artwork in artworks]

class ReceitaTotalHandler(AdiantamentoHandler):
    def requerimento_handle(self, id_artista, artworks):
        if self.facade:
            receita_total = 0
            for artwork_id in artworks:
                periodo_anual = datetime.now() - timedelta(days=365)
                cursor = self.facade.executa_query(
                    "SELECT SUM(valor_arrecadado) FROM pagamento_rubrica WHERE obra_cod_obra = ? AND data_pagamento >= ?",
                    (artwork_id, periodo_anual),
                )
                receita = cursor.fetchone()[0]

                if receita:
                    cursor = self.facade.executa_query(
                        "SELECT porcentagem_diretos FROM relacao_artista_obra WHERE artista_cod_artista = ? AND obra_cod_obra = ?",
                        (id_artista, artwork_id),
                    )
                    porcentagem = cursor.fetchone()[0]

                    receita_total += 0.95 * receita * (porcentagem / 100)

            return receita_total

        else:
            return 0
