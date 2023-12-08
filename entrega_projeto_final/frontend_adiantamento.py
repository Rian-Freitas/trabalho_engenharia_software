import tkinter as tk
from backend_adiantamento import LazyProxyFacade, AdiantamentoHandler, ArtistaIdHandler, ObraIdHandler, ReceitaTotalHandler
from datetime import datetime, timedelta

class AdiantamentoApplication:
    def __init__(self, root, facade):
        self.root = root
        self.root.title("Solicitar Adiantamento")
        self.facade = facade

        # Valor máximo para retirada
        label_adiantamento_max = tk.Label(root, text="Valor Máximo para Adiantamento:")
        label_adiantamento_max.pack()

        self.valor_adiantamento_max = tk.StringVar()
        label_valor_adiantamento_max = tk.Label(root, textvariable=self.valor_adiantamento_max)
        label_valor_adiantamento_max.pack()

        # Seletor para escolher o valor do adiantamento
        label_valor_requerido = tk.Label(root, text="Valor Desejado:")
        label_valor_requerido.pack()

        self.valor_requerido = tk.StringVar()
        valor_entrada = tk.Entry(root, textvariable=self.valor_requerido)
        valor_entrada.pack()

        # Labels para exibir mensagens
        self.label_mensagens = tk.Label(root, text="")
        self.label_mensagens.pack()

        # Botão de envio
        botao_envio = tk.Button(root, text="Enviar Solicitação", command=self.solicitar_requerimento)
        botao_envio.pack()

        # Chamar a função para obter o valor máximo de adiantamento
        email_artista = "artist1@email.com"
        valor_adiantamento_max = self.obter_max_valor_adiantamento(email_artista)
        self.valor_adiantamento_max.set(str(valor_adiantamento_max))

    def solicitar_requerimento(self):
        valor_requerido_str = self.valor_requerido.get()

        try:
            valor_requerido = float(valor_requerido_str)
            valor_adiantamento_max = float(self.valor_adiantamento_max.get())

            if 0 <= valor_requerido <= valor_adiantamento_max:
                self.label_mensagens.config(text="A solicitação foi recebido e será avaliada.")
                # Chain of Responsibility
                handler_chain = AdiantamentoHandler(self.facade)
                id_atista = handler_chain.define_proximo_handler(ArtistaIdHandler(self.facade)).requerimento_handle("artist1@email.com")
                artworks = handler_chain.define_proximo_handler(ObraIdHandler(self.facade)).requerimento_handle(id_atista)
                receita_total = handler_chain.define_proximo_handler(ReceitaTotalHandler(self.facade)).requerimento_handle(id_atista, artworks)
            elif valor_requerido > valor_adiantamento_max:
                self.label_mensagens.config(text="O valor é superior ao limite permitido.")
            else:
                self.label_mensagens.config(text="Valor digitado é inválido.")

        except ValueError:
            self.label_mensagens.config(text="Valor digitado é inválido.")

    def obter_max_valor_adiantamento(self, artist_email):
        # Proxy (Lazy)
        cursor = self.facade.executa_query("SELECT cod_artista FROM artista WHERE email_artista = ?", (artist_email,))
        id_artista = cursor.fetchone()

        if id_artista:
            id_artista = id_artista[0]

            cursor = self.facade.executa_query("SELECT obra_cod_obra FROM relacao_artista_obra WHERE artista_cod_artista = ?", (id_artista,))
            artworks = cursor.fetchall()

            receita_total = 0

            for artwork in artworks:
                artwork_id = artwork[0]

                periodo_anual = datetime.now() - timedelta(days=365)
                cursor = self.facade.executa_query(
                    "SELECT SUM(valor_arrecadado) FROM pagamento_rubrica WHERE obra_cod_obra = ? AND data_pagamento >= ?",
                    (artwork_id, periodo_anual),
                )
                receita = cursor.fetchone()[0]

                if receita:
                    cursor = self.facade.executa_query(
                        "SELECT porcentagem_diretos FROM relacao_artista_obra WHERE artista_cod_artista = ? AND obra_cod_obra = ?",
                        (id_artista, artwork_id),
                    )
                    porcentagem = cursor.fetchone()[0]

                    receita_total += 0.95 * receita * (porcentagem / 100)

            return receita_total

        else:
            return 0

if __name__ == "__main__":
    facade = LazyProxyFacade('testbase2.db')
    root = tk.Tk()
    app = AdiantamentoApplication(root, facade)
    root.mainloop()
