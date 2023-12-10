import tkinter as tk
from backend_adiantamento import LazyProxyFacade, AdiantamentoHandler, ArtistaIdHandler, ObraIdHandler, ReceitaTotalHandler
from datetime import datetime, timedelta
from PIL import Image, ImageTk

class AdiantamentoApplication:
    def __init__(self, root, facade):
        self.root = root
        self.root.title("Solicitar Adiantamento")
        self.facade = facade

        label_solicitar_adiantamento = tk.Label(root, text="ECAD - Solicitar Adiantamento", fg="#57a1f8", bg="#fff", font=("Microsoft Yahei UI Light", 23, "bold"))
        label_solicitar_adiantamento.place(x=500, y=0)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.configure(bg="white")

        # Adiciona Logo
        image = Image.open("figs/login.jpg")
        image = image.resize((100, 100), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)

        # Valor máximo para retirada
        label_adiantamento_max = tk.Label(root, text="Valor Máximo para Adiantamento em Reais:", fg="#000000", bg="#fff", font=("Microsoft Yahei UI Light", 17, "bold"))
        label_adiantamento_max.place(x=50, y=200)

        self.valor_adiantamento_max = tk.StringVar()
        label_adiantamento_max_valor = tk.Label(root, textvariable=self.valor_adiantamento_max, fg="#000000", bg="#fff", font=("Microsoft Yahei UI Light", 17, "bold"))
        label_adiantamento_max_valor.place(x=550, y=200)

        # Seletor para escolher o valor do adiantamento
        label_valor_requerido = tk.Label(root, text="Valor Desejado para Retirada (apenas números):", fg="#000000", bg="#fff", font=("Microsoft Yahei UI Light", 17, "bold"))
        label_valor_requerido.place(x=50, y=400)

        self.valor_requerido = tk.StringVar()
        valor_entrada = tk.Entry(root, textvariable=self.valor_requerido)
        valor_entrada.place(x=650, y=410)

        # Labels para exibir mensagens
        self.label_mensagens = tk.Label(root, text="", fg="#000000", bg="#fff", font=("Microsoft Yahei UI Light", 13, "bold"))
        self.label_mensagens.place(x=600, y=450)

        # Botão de envio
        botao_envio = tk.Button(root, text="Enviar Solicitação", command=self.solicitar_requerimento, fg="#FF0000", bg="#fff", font=("Microsoft Yahei UI Light", 15, "bold"))
        botao_envio.place(x=625, y=600)

        #label boas vindas
        label_boas_vindas = tk.Label(root, text="Bem vindo,", fg="#000000", bg="#fff", font=("Microsoft Yahei UI Light", 17, "bold"))
        label_boas_vindas.place(x=650, y=60)

        # Label para nome do artista
        self.nome_artista = tk.StringVar()
        label_nome_artista = tk.Label(root, textvariable=self.nome_artista, fg="#000000", bg="#fff", font=("Microsoft Yahei UI Light", 17, "bold"))
        label_nome_artista.place(x=675, y=100)

        # Chamar a função para obter o valor máximo de adiantamento
        email_artista = "artist1@email.com"
        valor_adiantamento_max = self.obter_max_valor_adiantamento(email_artista)
        self.valor_adiantamento_max.set(str(valor_adiantamento_max))
        nome_artista = self.desc_nome_artista(email_artista)
        self.nome_artista.set(nome_artista)

    def desc_nome_artista(self, email_artista):
        # Método para obter o nome do artista a partir do banco de dados
        cursor = self.facade.executa_query("SELECT nome_artista FROM artista WHERE email_artista = ?", (email_artista,))
        nome_artista = cursor.fetchone()
        if nome_artista:
            return nome_artista[0]
        return None

    def solicitar_requerimento(self):
        # Método de solicitação do valor
        valor_requerido_str = self.valor_requerido.get()

        try:
            valor_requerido = float(valor_requerido_str)
            valor_adiantamento_max = float(self.valor_adiantamento_max.get())

            if 0 <= valor_requerido <= valor_adiantamento_max:
                self.label_mensagens.config(text="A solicitação foi recebida e será avaliada.")
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

    def obter_max_valor_adiantamento(self, email_artista):
        # Método para obter o valor máximo de adiantamento
        # Proxy (Lazy)
        cursor = self.facade.executa_query("SELECT cod_artista FROM artista WHERE email_artista = ?", (email_artista,))
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
    # Configuração inicial da aplicação
    facade = LazyProxyFacade('testbase2.db')
    root = tk.Tk()
    app = AdiantamentoApplication(root, facade)
    root.mainloop()
