import unittest
from unittest.mock import Mock
from datetime import datetime, timedelta
from tkinter import Text
from recebimento_musicista import Database, Query, DatabaseInteraction, SearchRecords, Client

class TestDatabaseInteraction(unittest.TestCase):
    def test_search_records(self):
        # Mock do Database para evitar a dependência do banco de dados real
        mock_database = Mock(spec=Database)
        db_interaction = DatabaseInteraction(mock_database)

        # Mock dos parâmetros da consulta
        association_code = "1"
        start_date = "2023-01-01"
        end_date = "2023-01-31"
        result_text = Text()
        sql_query, query_params = Query.create_query(association_code, start_date, end_date,
                                                    "a.associacao_cod_associacao", association_code)

        # Mock do cursor
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [(1, "Artista1", "2023-01-01", 100.0)]
        mock_database.get_connection.return_value.cursor.return_value = mock_cursor

        # Executa o método que queremos testar
        db_interaction.search_records(association_code, start_date, end_date, result_text, sql_query, query_params)

        # Verifica se o método do cursor foi chamado corretamente
        mock_cursor.execute.assert_called_once_with(sql_query, query_params)

        # Verifica se o método do result_text foi chamado corretamente
        self.assertEqual(result_text.get(1.0, "end-1c"), "(1, 'Artista1', '2023-01-01', 100.0)\n")

class TestSearchRecords(unittest.TestCase):
    def test_execute(self):
        # Mock da DatabaseInteraction para evitar a dependência do banco de dados real
        mock_db_interaction = Mock(spec=DatabaseInteraction)
        search_records = SearchRecords(mock_db_interaction, "123", "2023-01-01", "2023-01-31", Text())

        # Mock dos parâmetros da consulta
        sql_query = "SELECT * FROM pagamento_rubrica;"
        query_params = ("2023-01-01", "2023-01-31", "1")

        # Executa o método que queremos testar
        search_records.execute(sql_query, query_params)

        # Verifica se o método da DatabaseInteraction foi chamado corretamente
        mock_db_interaction.search_records.assert_called_once_with("123", "2023-01-01", "2023-01-31", mock_db_interaction, sql_query, query_params)

class TestClient(unittest.TestCase):
    def test_search_records(self):
        # Mock do SearchRecords para evitar a dependência da interação real com a GUI
        mock_search_records = Mock(spec=SearchRecords)
        
        # Configuração do Client
        client = Client()
        client.search_records = mock_search_records  # Substitui o método original pelo mock

        # Simula a interação do usuário
        client.association_code_var.set("123")
        client.start_date_var.set((datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        client.end_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        client.query_type_var.set("query1")

        # Executa o método que queremos testar
        client.search_records()

        # Verifica se o método do SearchRecords foi chamado corretamente
        mock_search_records.assert_called_once()

if __name__ == '__main__':
    unittest.main()
