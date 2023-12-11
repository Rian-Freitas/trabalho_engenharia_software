import sqlite3
import tkinter as tk
from tkinter import ttk
from typing import Tuple, Any

# Constants
DB_FILE = "database.db"  # The database file name
APP_TITLE = "Search Records"  # Title for the application window

class DatabaseConnectionError(Exception):
    """Exception raised for errors in the database connection."""
    def __init__(self, message="Error connecting to the database"):
        self.message = message
        super().__init__(self.message)

#Initial version of DatabaseSingleton class

#class DatabaseSingleton:
#   instance.conn = sqlite3.connect(DB_FILE)
    # def get_connection(self) -> sqlite3.Connection:
    #     """Returns the established database connection."""
    #     return self.conn


class DatabaseSingleton:
    """
    Singleton class to ensure only one database connection is established.

    This class uses the Singleton design pattern to create a single instance of the database connection.

    >>> db_instance = DatabaseSingleton()
    >>> isinstance(db_instance.get_connection(), sqlite3.Connection)
    True
    
    """
    _instance = None

    def __new__(cls, *args, **kwargs) -> "DatabaseSingleton":
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            try:
                cls._instance.conn = sqlite3.connect(DB_FILE)
            except sqlite3.Error as e:
                raise DatabaseConnectionError(f"Database error: {e}")
        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        """Returns the established database connection."""
        return self.conn

#Initial version of QueryFactory:
#class Query:
# sql_query = f"""
#         SELECT
#             a.cod_artista,
#             a.nome_artista,
#             pr.data_pagamento,
#             SUM(pr.valor_arrecadado)  AS total_valor_liquido
#         FROM pagamento_rubrica pr
#         JOIN relacao_artista_obra eo ON pr.obra_cod_obra = eo.obra_cod_obra
#         JOIN artista a ON eo.artista_cod_artista = a.cod_artista
#         WHERE pr.data_pagamento BETWEEN ? AND ?
#         AND a.cod_artista = ?
#         GROUP BY a.cod_artista, a.nome_artista, pr.data_pagamento, eo.porcentagem_diretos;
#         """
#         return sql_query
#       


class QueryFactory:
    """
    Factory class for creating SQL queries.

    >>> QueryFactory.create_query_artist_deduction('1', '2023-01-01', '2023-12-31', 'a.associacao_cod_associacao', '1')
    ('\n        SELECT\n            a.cod_artista,\n            a.nome_artista,\n            pr.data_pagamento,\n            SUM(pr.valor_arrecadado) * 0.9 * (eo.porcentagem_diretos / 100.0) AS total_valor_liquido\n        FROM pagamento_rubrica pr\n        JOIN relacao_artista_obra eo ON pr.obra_cod_obra = eo.obra_cod_obra\n        JOIN artista a ON eo.artista_cod_artista = a.cod_artista\n        WHERE pr.data_pagamento BETWEEN ? AND ?\n        AND a.associacao_cod_associacao = ?\n        GROUP BY a.cod_artista, a.nome_artista, pr.data_pagamento, eo.porcentagem_diretos;\n        ', ('2023-01-01', '2023-12-31', '1'))
    >>> QueryFactory.create_query_artist_deduction('2', '2022-01-01', '2023-12-31', 'a.associacao_cod_associacao', '1')
    ('\n        SELECT\n            a.cod_artista,\n            a.nome_artista,\n            pr.data_pagamento,\n            SUM(pr.valor_arrecadado) * 0.9 * (eo.porcentagem_diretos / 100.0) AS total_valor_liquido\n        FROM pagamento_rubrica pr\n        JOIN relacao_artista_obra eo ON pr.obra_cod_obra = eo.obra_cod_obra\n        JOIN artista a ON eo.artista_cod_artista = a.cod_artista\n        WHERE pr.data_pagamento BETWEEN ? AND ?\n        AND a.associacao_cod_associacao = ?\n        GROUP BY a.cod_artista, a.nome_artista, pr.data_pagamento, eo.porcentagem_diretos;\n        ', ('2022-01-01', '2023-12-31', '1'))
    """

    @staticmethod
    def create_query_artist_deduction(association_code: str, start_date: str, end_date: str, condition_field: str, condition_value: str) -> Tuple[str, Tuple[str, str, str]]:
        """
        Creates a SQL query for artist deductions.

        Args:
            association_code: Code of the association.
            start_date: Start date for the query period.
            end_date: End date for the query period.
            condition_field: The field used for the condition.
            condition_value: The value of the condition field.

        Returns:
            A tuple containing the SQL query string and its parameters.
        """

        sql_query = f"""
        SELECT
            a.cod_artista,
            a.nome_artista,
            pr.data_pagamento,
            SUM(pr.valor_arrecadado) * 0.9 * (eo.porcentagem_diretos / 100.0) AS total_valor_liquido
        FROM pagamento_rubrica pr
        JOIN relacao_artista_obra eo ON pr.obra_cod_obra = eo.obra_cod_obra
        JOIN artista a ON eo.artista_cod_artista = a.cod_artista
        WHERE pr.data_pagamento BETWEEN ? AND ?
        AND {condition_field} = ?
        GROUP BY a.cod_artista, a.nome_artista, pr.data_pagamento, eo.porcentagem_diretos;
        """
        return sql_query, (start_date, end_date, condition_value)


class LazyProxySerie:
    """
    Lazy initialization proxy class.

    This class uses the Proxy pattern to delay the creation of an object until it is needed.
    """
    def __init__(self, target_class: Any):
         self.target_class = target_class
         self.instance = None

    def __getattr__(self, name: str) -> Any:
        if self.instance is None:
            self.instance = self.target_class()
        return getattr(self.instance, name)

class DatabaseFacade:
    """
    Facade class for database operations.

    This class provides a simplified interface for various database operations.
    """
    def __init__(self, db_singleton: DatabaseSingleton):
        self.db_singleton = db_singleton

    def search_records(self, association_code: str, start_date: str, end_date: str, result_text: tk.Text, sql_query: str, query_params: Tuple[str, str, str]):
        """
        Executes a search query and displays the results in the GUI.

        Args:
            association_code: Code of the association.
            start_date: Start date for the query period.
            end_date: End date for the query period.
            result_text: The tkinter Text widget to display results.
            sql_query: The SQL query to execute.
            query_params: The parameters for the SQL query.
        """
        conn = self.db_singleton.get_connection()
        cursor = conn.cursor()

        cursor.execute(sql_query, query_params)

        results = cursor.fetchall()

        for row in results:
            result_text.insert(tk.END, f"{row}\n")

        
class SearchRecordsCommand:
    """
    Command class to encapsulate the action of searching records in the database.

    This class follows the Command design pattern, encapsulating all the information needed to perform an action or trigger an event at a later time.
    """

    def __init__(self, db_facade: DatabaseFacade, association_code: str, start_date: str, end_date: str, result_text: tk.Text):
        """
        Initialize the SearchRecordsCommand with required parameters.

        Args:
            db_facade: An instance of DatabaseFacade for database operations.
            association_code: The association code for the query.
            start_date: The start date for the query.
            end_date: The end date for the query.
            result_text: The tkinter Text widget to display results.
        """
        self.db_facade = db_facade
        self.association_code = association_code
        self.start_date = start_date
        self.end_date = end_date
        self.result_text = result_text

    def execute(self, sql_query: str, query_params: Tuple[str, str, str]):
        """
        Execute the command to perform the search.

        Args:
            sql_query: The SQL query string to be executed.
            query_params: A tuple containing the parameters for the SQL query.
        """
        self.db_facade.search_records(self.association_code, self.start_date, self.end_date, self.result_text, sql_query, query_params)

class Client:
    """
    Client class for the application GUI.

    This class sets up the user interface and handles user interactions.
    """

    def __init__(self):
        """
        Initialize the Client application with tkinter GUI components.
        """
        self.app = tk.Tk()
        self.app.title(APP_TITLE)

        # Initialize input variables
        self.association_code_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()

        # Initialize database connection
        self.db_proxy = LazyProxySerie(DatabaseSingleton)
        self.db_facade = DatabaseFacade(self.db_proxy)

        # Initialize query selection variable
        self.query_type_var = tk.StringVar(value="query1")  # Default to the first query

        # Set up GUI components
        self.setup_gui()

    def setup_gui(self):
        """
        Set up the GUI components of the application.
        """
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
        """
        Handle the search records action triggered by the user.
        """
        association_code = self.association_code_var.get()
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()

        # Clear previous results
        self.result_text.delete(1.0, tk.END)

        # Determine the query based on user selection
        selected_query = self.query_type_var.get()
        if selected_query == "query1":
            sql_query, query_params = QueryFactory.create_query_artist_deduction(association_code, start_date, end_date, "a.associacao_cod_associacao", association_code)
        elif selected_query == "query2":
            sql_query, query_params = QueryFactory.create_query_artist_deduction(association_code, start_date, end_date, "eo.artista_cod_artista", association_code)

        # Execute the search command
        search_command = SearchRecordsCommand(self.db_facade, association_code, start_date, end_date, self.result_text)
        search_command.execute(sql_query, query_params)

    def run(self):
        """
        Run the tkinter main event loop.
        """
        self.app.mainloop()

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    client = Client()
    client.run()
    
