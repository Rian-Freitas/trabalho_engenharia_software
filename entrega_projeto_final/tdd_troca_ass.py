import unittest
from unittest.mock import MagicMock
from backend_troca_ass import conexaoFactory, FacadeDB

class TestFacadeDB(unittest.TestCase):
    def setUp(self):
        self.factory_mock = MagicMock(spec=conexaoFactory)
        self.facade = FacadeDB(self.factory_mock)

    def test_executa_query(self):
        query = "SELECT * FROM tabela"
        cursor_mock = MagicMock()
        conexao_mock = MagicMock()
        conexao_mock.cursor.return_value = cursor_mock
        self.factory_mock.get_conexao.return_value = conexao_mock

        self.facade.executa_query(query)

        conexao_mock.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once_with(query)
        cursor_mock.fetchall.assert_called_once()

    def test_executa_update(self):
        query = "UPDATE tabela SET coluna = valor"
        cursor_mock = MagicMock()
        conexao_mock = MagicMock()
        conexao_mock.cursor.return_value = cursor_mock
        self.factory_mock.get_conexao.return_value = conexao_mock

        self.facade.executa_update(query)

        conexao_mock.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once_with(query)
        conexao_mock.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
