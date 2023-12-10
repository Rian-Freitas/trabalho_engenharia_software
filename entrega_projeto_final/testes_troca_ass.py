import unittest
from unittest.mock import MagicMock
from backend_troca_ass import conexaoFactory, FacadeDB

class TestFacadeDB(unittest.TestCase):
    def setUp(self):
        # Configuração inicial para cada teste
        # Cria um mock para a fábrica de conexões e instancia o objeto FacadeDB para teste
        self.factory_mock = MagicMock(spec=conexaoFactory)
        self.facade = FacadeDB(self.factory_mock)

    def test_executa_query(self):
        # Teste para o método executa_query
        query = "SELECT * FROM tabela"

        # Criação de mocks para objetos simulados de cursor e conexão
        cursor_mock = MagicMock()
        conexao_mock = MagicMock()
        conexao_mock.cursor.return_value = cursor_mock
        self.factory_mock.get_conexao.return_value = conexao_mock

        # Chamada ao método sendo testado
        self.facade.executa_query(query)

        # Verificações de chamadas esperadas
        conexao_mock.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once_with(query)
        cursor_mock.fetchall.assert_called_once()

    def test_executa_update(self):
        # Teste para o método executa_update
        query = "UPDATE tabela SET coluna = valor"

        # Criação de mocks para objetos simulados de cursor e conexão
        cursor_mock = MagicMock()
        conexao_mock = MagicMock()
        conexao_mock.cursor.return_value = cursor_mock
        self.factory_mock.get_conexao.return_value = conexao_mock

        # Chamada ao método sendo testado
        self.facade.executa_update(query)

        # Verificações de chamadas esperadas
        conexao_mock.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once_with(query)
        conexao_mock.commit.assert_called_once()

if __name__ == "__main__":
    # Executa os testes quando o script é executado diretamente
    unittest.main()
