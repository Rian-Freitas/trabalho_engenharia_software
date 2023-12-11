import unittest
from unittest.mock import Mock
from backend_troca_ass import conexaoFactory, FacadeDB

class TestConexaoFactory(unittest.TestCase):
    def test_singleton_instance(self):
        # Testa se duas instâncias compartilham a mesma conexão ao banco de dados
        factory1 = conexaoFactory("database.db")
        factory2 = conexaoFactory("database.db")
        self.assertEqual(factory1, factory2)

    def test_get_conexao(self):
        # Testa se o método get_conexao retorna a conexão correta
        factory = conexaoFactory("database.db")
        conexao = factory.get_conexao()
        self.assertIsNotNone(conexao)

class TestFacadeDB(unittest.TestCase):
    def setUp(self):
        # Configuração inicial para os testes
        self.factory_mock = Mock()
        self.facade = FacadeDB(self.factory_mock)

    def test_executa_query(self):
        # Testa se o método executa_query executa a query corretamente
        query = "SELECT * FROM test_table"
        conexao_mock = Mock()
        cursor_mock = Mock()
        self.factory_mock.get_conexao.return_value = conexao_mock
        conexao_mock.cursor.return_value = cursor_mock

        result = self.facade.executa_query(query)

        self.assertEqual(result, cursor_mock.fetchall())
        conexao_mock.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once_with(query)
        cursor_mock.close.assert_called_once()

    def test_executa_update(self):
        # Testa se o método executa_update executa o update corretamente
        query = "UPDATE test_table SET column = value"
        conexao_mock = Mock()
        cursor_mock = Mock()
        self.factory_mock.get_conexao.return_value = conexao_mock
        conexao_mock.cursor.return_value = cursor_mock

        self.facade.executa_update(query)

        conexao_mock.commit.assert_called_once()
        cursor_mock.execute.assert_called_once_with(query)
        cursor_mock.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
