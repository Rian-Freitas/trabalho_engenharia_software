import unittest
from unittest.mock import  patch
from tkinter import Tk
from backend_adiantamento import LazyProxyFacade, ArtistaIdHandler, ObraIdHandler, ReceitaTotalHandler
from frontend_adiantamento import AdiantamentoApplication

class TestAdiantamentoApplication(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.facade = LazyProxyFacade('testbase2.db')
        self.app = AdiantamentoApplication(self.root, self.facade)

    def tearDown(self):
        self.root.destroy()

    @patch.object(LazyProxyFacade, 'executa_query')
    def teste_valor_abaixo(self, mock_execute_query):
    # Configurando o valor máximo para retirada
        self.app.valor_adiantamento_max.set("500")

        # Configurando o valor desejado
        self.app.valor_requerido.set("300")

        # Chamando a função a ser testada
        with patch.object(self.app, 'label_mensagens') as mock_label_mensagens:
            self.app.solicitar_requerimento()

        # Verificando se a mensagem é a esperada
        mock_label_mensagens.config.assert_called_with(text="A solicitação foi recebida e será avaliada.")

    @patch.object(LazyProxyFacade, 'executa_query')
    def teste_valor_acima(self, mock_execute_query):
        # Configurando o valor máximo para retirada
        self.app.valor_adiantamento_max.set("500")

        # Configurando um valor desejado maior que o máximo permitido
        self.app.valor_requerido.set("600")

        # Chamando a função a ser testada
        with patch.object(self.app, 'label_mensagens') as mock_label_mensagens:
            self.app.solicitar_requerimento()

        # Verificando se a mensagem é a esperada
        mock_label_mensagens.config.assert_called_with(text="O valor é superior ao limite permitido.")

    def teste_valor_invalido(self):
        # Configurando o valor máximo para retirada
        self.app.valor_adiantamento_max.set("500")

        # Configurando um valor desejado inválido
        self.app.valor_requerido.set("abc")

        # Chamando a função a ser testada
        with patch.object(self.app, 'label_mensagens') as mock_label_mensagens:
            self.app.solicitar_requerimento()

        # Verificando se a mensagem é a esperada
        mock_label_mensagens.config.assert_called_with(text="Valor digitado é inválido.")

if __name__ == '__main__':
    unittest.main()
