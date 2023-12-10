# Constantes
DB_FILE = "testbase2.db"
APP_TITLE = "Search Records"

import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Singleton
class SistemaRelatoriosSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SistemaRelatoriosSingleton, cls).__new__(cls)
            cls._instance._conexao_bd = sqlite3.connect(":memory:")
            cls._instance._criar_tabela_rendimentos()
        return cls._instance

    def _criar_tabela_rendimentos(self):
        cursor = self._conexao_bd.cursor()
        cursor.execute('''CREATE TABLE rendimentos (
                            musicista_id INTEGER,
                            valor INTEGER,
                            data DATE
                         )''')
        self._conexao_bd.commit()

    def adicionar_rendimento(self, musicista_id, valor):
        data_atual = datetime.now().strftime("%Y-%m-%d")
        cursor = self._conexao_bd.cursor()
        cursor.execute("INSERT INTO rendimentos VALUES (?, ?, ?)", (musicista_id, valor, data_atual))
        self._conexao_bd.commit()

    def obter_rendimentos_mes_atual(self, musicista_id):
        cursor = self._conexao_bd.cursor()
        mes_atual = datetime.now().month
        cursor.execute("SELECT valor FROM rendimentos WHERE musicista_id = ? AND strftime('%m', data) = ?", (musicista_id, str(mes_atual)))
        return [row[0] for row in cursor.fetchall()]

# Proxy
class ProxyProtecaoRelatorio:
    def __init__(self, servico_real):
        self._servico_real = servico_real

    def solicitar_relatorio(self, musicista_id):
        # Lógica para verificar permissões
        if self._verificar_permissoes():
            return self._servico_real.solicitar_relatorio(musicista_id)
        else:
            return "Acesso negado. Permissões insuficientes."

    def _verificar_permissoes(self):
        # Lógica para verificar permissões
        return True

# Chain of Responsibility
class DescontoHandler:
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    def handle_request(self, rendimentos):
        # Lógica para calcular descontos
        desconto_ecad = 0.1 * sum(rendimentos)
        desconto_associacao = 0.05 * sum(rendimentos)
        return {
            'Desconto ECAD': desconto_ecad,
            'Desconto Associação': desconto_associacao
        }

    def set_next_handler(self, next_handler):
        self._next_handler = next_handler

    def process_request(self, rendimentos):
        descontos = self.handle_request(rendimentos)
        if self._next_handler:
            return {**descontos, **self._next_handler.process_request(rendimentos)}
        return descontos

# Cliente
class InterfaceUsuario:
    def __init__(self, sistema, proxy, chain_of_responsibility):
        self.sistema = sistema
        self.proxy = proxy
        self.chain_of_responsibility = chain_of_responsibility

        self.root = tk.Tk()
        self.root.title("Relatório de Recebimento para Musicista")

        self.nome_musicista = tk.Entry(self.root)
        self.nome_musicista.grid(row=0, column=1, padx=10, pady=10)
        self.label_nome = tk.Label(self.root, text="Nome do Musicista:")
        self.label_nome.grid(row=0, column=0, padx=10, pady=10)

        self.botao_gerar_relatorio = tk.Button(self.root, text="Gerar Relatório", command=self.gerar_relatorio)
        self.botao_gerar_relatorio.grid(row=1, column=0, columnspan=2, pady=10)

    def gerar_relatorio(self):
        nome_musicista = self.nome_musicista.get()
        if nome_musicista:
            musicista_id = 1  # Supondo que o ID do musicista seja 1
            rendimentos = self.sistema.obter_rendimentos_mes_atual(musicista_id)

            # Utilizando o Proxy para controlar o acesso ao serviço real
            relatorio_proxy = ProxyProtecaoRelatorio(self.sistema)
            relatorio = relatorio_proxy.solicitar_relatorio(musicista_id)

            # Utilizando Chain of Responsibility para calcular descontos
            descontos = self.chain_of_responsibility.process_request(rendimentos)
            relatorio += "\nCálculos detalhados:\n"
            for item, valor in descontos.items():
                relatorio += f"{item}: {valor}\n"

            messagebox.showinfo("Relatório Gerado", relatorio)
        else:
            messagebox.showwarning("Aviso", "Por favor, insira o nome do musicista.")

    def executar(self):
        self.root.mainloop()

if __name__ == "__main__":
    sistema_singleton = SistemaRelatoriosSingleton()
    proxy = ProxyProtecaoRelatorio(sistema_singleton)
    chain_of_responsibility = DescontoHandler()

    interface = InterfaceUsuario(sistema_singleton, proxy, chain_of_responsibility)
    interface.executar()