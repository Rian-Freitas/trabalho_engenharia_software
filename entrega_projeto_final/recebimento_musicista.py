import sqlite3
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from typing import Tuple, List

# Constantes
DB_FILE: str = "database.db"
APP_TITLE: str = "Search Records"


# Singleton
class Database:
    """Classe para conexão com o banco de dados."""

    _instance = None

    def __new__(cls) -> 'Database':
        """Cria uma nova instância da classe ou retorna a instância existente."""
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.conn: sqlite3.Connection = sqlite3.connect(DB_FILE)
        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        """Retorna a conexão com o banco de dados."""
        return self.conn


# Factory
class Query:
    """Classe para criar consultas SQL."""

    @staticmethod
    def create_query(association_code: str, start_date: str, end_date: str, condition_field: str,
                     condition_value: str) -> Tuple[str, Tuple[str, str, str]]:
        """Cria uma consulta SQL com base nos parâmetros fornecidos."""
        sql_query: str = f"""
        SELECT
            a.cod_artista,
            a.nome_artista,
            pr.data_pagamento,
            SUM(pr.valor_arrecadado) AS total_valor_arrecadado
        FROM pagamento_rubrica pr
        JOIN relacao_artista_obra eo ON pr.obra_cod_obra = eo.obra_cod_obra
        JOIN artista a ON eo.artista_cod_artista = a.cod_artista
        WHERE pr.data_pagamento BETWEEN ? AND ?
        AND {condition_field} = ?
        GROUP BY a.cod_artista, a.nome_artista, pr.data_pagamento;
        """

        return sql_query, (start_date, end_date, condition_value)


# Proxy
class LazyProxy:
    """Classe Proxy que atrasa a criação da instância real."""

    def __init__(self, target_class: type) -> None:
        self.target_class: type = target_class
        self.instance: type = None

    def __getattr__(self, name: str) -> type:
        """Obtém um atributo da instância real quando necessário."""
        if self.instance is None:
            self.instance = self.target_class()
        return getattr(self.instance, name)


# Facade
class DatabaseInteraction:
    """Classe para interagir com o banco de dados."""

    def __init__(self, database: Database) -> None:
        self.database: Database = database

    def search_records(self, association_code: str, start_date: str, end_date: str, result_text: tk.Text,
                       sql_query: str, query_params: Tuple[str, str, str]) -> None:
        """Executa uma consulta no banco de dados e exibe os resultados em um widget de texto."""
        conn: sqlite3.Connection = self.database.get_connection()
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(sql_query, query_params)

        results: List[Tuple] = cursor.fetchall()

        for row in results:
            result_text.insert(tk.END, f"{row}\n")


# Commands
class SearchRecords:
    """Comando para executar uma busca de registros."""

    def __init__(self, db_facade: DatabaseInteraction, association_code: str, start_date: str, end_date: str,
                 result_text: tk.Text) -> None:
        self.db_facade: DatabaseInteraction = db_facade
        self.association_code: str = association_code
        self.start_date: str = start_date
        self.end_date: str = end_date
        self.result_text: tk.Text = result_text

    def execute(self, sql_query: str, query_params: Tuple[str, str, str]) -> None:
        """Executa o comando de busca."""
        self.db_facade.search_records(self.association_code, self.start_date, self.end_date, self.result_text, sql_query, query_params)


# Cliente
class Client:
    """Classe principal que inicia a aplicação."""

    def __init__(self) -> None:
        self.app: tk.Tk = tk.Tk()
        self.app.title(APP_TITLE)

        # Variáveis de entrada
        self.association_code_var: tk.StringVar = tk.StringVar()
        self.start_date_var: tk.StringVar = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        self.end_date_var: tk.StringVar = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        # Cria instâncias usando Proxy e Singleton
        self.db_proxy: LazyProxy = LazyProxy(Database)
        self.db_facade: DatabaseInteraction = DatabaseInteraction(self.db_proxy)

        # Variável de seleção de consulta
        self.query_type_var: tk.StringVar = tk.StringVar()
        self.query_type_var.set("query1")  # Padrão para a primeira consulta

        # Componentes da GUI
        ttk.Radiobutton(self.app, text="Associação", variable=self.query_type_var, value="query1").grid(row=3, column=0, padx=5, pady=5)
        ttk.Radiobutton(self.app, text="Artista", variable=self.query_type_var, value="query2").grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.app, text="Code:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self.app, textvariable=self.association_code_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.app, text="Start Date:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(self.app, textvariable=self.start_date_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.app, text="End Date:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self.app, textvariable=self.end_date_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.app, text="Search", command=self.search_records).grid(row=3, column=0, columnspan=2, pady=10)

        self.result_text: tk.Text = tk.Text(self.app, wrap=tk.WORD, width=50, height=10)
        self.result_text.grid(row=4, column=0, columnspan=2, pady=10)

    def search_records(self) -> None:
        """Executa uma busca de registros com base nos parâmetros fornecidos."""
        association_code: str = self.association_code_var.get()
        start_date: str = self.start_date_var.get()
        end_date: str = self.end_date_var.get()
        self.result_text.delete(1.0, tk.END)

        selected_query: str = self.query_type_var.get()
        if selected_query == "query1":
            sql_query, query_params = Query.create_query(association_code, start_date, end_date,
                                                               "a.associacao_cod_associacao", association_code)
        elif selected_query == "query2":
            sql_query, query_params = Query.create_query(association_code, start_date, end_date,
                                                               "eo.artista_cod_artista", association_code)

        search_command: SearchRecords = SearchRecords(self.db_facade, association_code, start_date,
                                                                    end_date, self.result_text)
        search_command.execute(sql_query, query_params)

    def run(self) -> None:
        """Inicia a aplicação."""
        self.app.mainloop()


# Execute o código do cliente
if __name__ == "__main__":
    client: Client = Client()
    client.run()
