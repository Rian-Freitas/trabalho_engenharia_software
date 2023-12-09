import sqlite3
import tkinter as tk
from tkinter import ttk

# Constants
DB_FILE = "testbase2.db"
APP_TITLE = "Search Records"

# Singleton
class DatabaseSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.conn = sqlite3.connect(DB_FILE)
        return cls._instance

    def get_connection(self):
        return self.conn

#Factory
class QueryFactory:
    @staticmethod
    def create_query(association_code, start_date, end_date, condition_field, condition_value):
        sql_query = f"""
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
    def __init__(self, target_class):
        self.target_class = target_class
        self.instance = None

    def __getattr__(self, name):
        if self.instance is None:
            self.instance = self.target_class()
        return getattr(self.instance, name)

# Facade
class DatabaseFacade:
    def __init__(self, db_singleton):
        self.db_singleton = db_singleton

    def search_records(self, association_code, start_date, end_date, result_text, sql_query, query_params):
        conn = self.db_singleton.get_connection()
        cursor = conn.cursor()

        cursor.execute(sql_query, query_params)

        results = cursor.fetchall()

        for row in results:
            result_text.insert(tk.END, f"{row}\n")

        
# Command
class SearchRecordsCommand:
    def __init__(self, db_facade, association_code, start_date, end_date, result_text):
        self.db_facade = db_facade
        self.association_code = association_code
        self.start_date = start_date
        self.end_date = end_date
        self.result_text = result_text

    def execute(self, sql_query, query_params):
        self.db_facade.search_records(self.association_code, self.start_date, self.end_date, self.result_text, sql_query, query_params)

# Client code
class Client:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title(APP_TITLE)

        # Input variables
        self.association_code_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()

        # Create instances using Proxy and Singleton
        self.db_proxy = LazyProxy(DatabaseSingleton)
        self.db_facade = DatabaseFacade(self.db_proxy)
        
        # Query selection variable
        self.query_type_var = tk.StringVar()
        self.query_type_var.set("query1")  # Default to the first query


        # GUI components

        # Radio buttons for query selection
        ttk.Radiobutton(self.app, text="Associação", variable=self.query_type_var, value="query1").grid(row=3, column=0, padx=5, pady=5)
        ttk.Radiobutton(self.app, text="Artista", variable=self.query_type_var, value="query2").grid(row=3, column=1, padx=5, pady=5)


        ttk.Label(self.app, text="Code:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self.app, textvariable=self.association_code_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.app, text="Start Date:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(self.app, textvariable=self.start_date_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.app, text="End Date:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self.app, textvariable=self.end_date_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.app, text="Search", command=self.search_records).grid(row=3, column=0, columnspan=2, pady=10)

        self.result_text = tk.Text(self.app, wrap=tk.WORD, width=50, height=10)
        self.result_text.grid(row=4, column=0, columnspan=2, pady=10)

    def search_records(self):
        # Retrieve input values
        association_code = self.association_code_var.get()
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()

        # Clear previous results
        self.result_text.delete(1.0, tk.END)

        # Determine which query to use based on the selected radio button
        selected_query = self.query_type_var.get()
        if selected_query == "query1":
            sql_query, query_params = QueryFactory.create_query(association_code, start_date, end_date, "a.associacao_cod_associacao", association_code)
        elif selected_query == "query2":
            sql_query, query_params = QueryFactory.create_query(association_code, start_date, end_date, "eo.artista_cod_artista", association_code)

        # Use the Command pattern to encapsulate the search functionality
        search_command = SearchRecordsCommand(self.db_facade, association_code, start_date, end_date, self.result_text)
        search_command.execute(sql_query, query_params)

    def run(self):
        self.app.mainloop()

# Run the client code
if __name__ == "__main__":
    client = Client()
    client.run()
