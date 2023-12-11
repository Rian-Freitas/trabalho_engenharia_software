import tkinter as tk
from tkinter import ttk
from SerieHistorica import DatabaseSingleton, DatabaseFacade, LazyProxySerie, QueryFactory, SearchRecordsCommand
from backend_adiantamento import LazyProxyFacade
from frontend_adiantamento import AdiantamentoApplication
from frontend_troca_ass import TrocaAssociacaoApp, LazyProxy
from backend_troca_ass import conexaoFactory, FacadeDB


APP_TITLE = "Página da Associação"  # Change to your desired title
DB_FILE = "database.db"

class ClientArtista:
    """
    Client class for the application GUI.
    This class sets up the user interface and handles user interactions.
    """

    def __init__(self, info):
        """
        Initialize the Client application with tkinter GUI components.
        """
        self.app = tk.Tk()
        self.info = info
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
        ttk.Button(self.app, text="Open Adiantamento Screen", command=lambda: self.open_adiantamento_screen(self.info)).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(self.app, text="Open Troca Screen", command=lambda: self.open_troca_screen(self.info)).grid(row=6, column=0, columnspan=2, pady=10)


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

    def open_adiantamento_screen(self, info):
    # Create a new top-level window
        adiantamento_window = tk.Toplevel(self.app)

        # Initialize the AdiantamentoApplication with the new top-level window
        facade = LazyProxyFacade('database.db')
        AdiantamentoApplication(adiantamento_window, facade, info)

    def open_troca_screen(self, info):
    # Create a new top-level window
        root = tk.Toplevel(self.app)
        factory_conexao = conexaoFactory('database.db')
        lazy_proxy = LazyProxy(FacadeDB, factory_conexao)
        TrocaAssociacaoApp(root, info, lazy_proxy)


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