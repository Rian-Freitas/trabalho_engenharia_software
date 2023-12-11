import unittest
from unittest.mock import Mock
from backend_adiantamento import DatabaseConnection, LazyProxyFacade, AdiantamentoHandler, ArtistaIdHandler, ObraIdHandler, ReceitaTotalHandler

class TestDatabaseConnection(unittest.TestCase):
    def test_singleton_instance(self):
        # Testa se duas instâncias compartilham a mesma conexão ao banco de dados
        database1 = DatabaseConnection("database.db")
        database2 = DatabaseConnection("database.db")
        self.assertEqual(database1, database2)

class TestLazyProxyFacade(unittest.TestCase):
    def setUp(self):
        # Configuração inicial para os testes
        self.mock_connection = Mock()
        self.facade = LazyProxyFacade("database.db")
        self.facade._conn = self.mock_connection

    def test_connection_property(self):
        # Testa se a propriedade 'connection' retorna a conexão correta
        connection = self.facade.connection
        self.assertEqual(connection, self.mock_connection)

    def test_executa_query(self):
        # Testa se a execução de uma query é feita corretamente
        query = "SELECT * FROM test_table"
        parameters = (1, 2, 3)
        cursor_mock = Mock()
        self.mock_connection.cursor.return_value = cursor_mock

        result = self.facade.executa_query(query, parameters)

        self.assertEqual(result, cursor_mock)
        self.mock_connection.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once_with(query, parameters)

if __name__ == '__main__':
    unittest.main()
