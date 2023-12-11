from widget_factory import WidgetFactory
from datetime import datetime
from database import Database
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd

class consumerPage:
    """
    Página do consumidor.
    """
    def __init__(self, info: list) -> None:
        """
        Página do consumidor.

        info: list
            Lista contendo as informações do usuário logado."""
        self.info = info
        self.db = Database()
        self.db.cursor.execute("SELECT cod_proprietario FROM proprietario WHERE email_proprietario = ?", (self.info[0],))
        self.cod_proprietario = self.db.cursor.fetchone()[0]

        self.root = WidgetFactory.create_window("Página do consumidor", 925, 500)

        self.img_logo, __ = WidgetFactory.create_image(self.root, "entrega_projeto_final/figs/ecad_login.png", (150, 150))
        self.img_logo.place(x=-10, y=350)

        self.title = WidgetFactory.create_title(self.root, "É você quem faz a música acontecer!")
        self.title.place(x=100, y=70)

        self.text = WidgetFactory.create_text(self.root, "Através da sua contribuição, os artistas podem continuar produzindo e você pode continuar ouvindo.")
        self.text.place(x=100, y=120)

        self.button = WidgetFactory.create_button(self.root, "Cadastrar estabelecimento", self.register_establishment, width=25)
        self.button.place(x=325, y=250)

        self.button = WidgetFactory.create_button(self.root, "Ver estabelecimentos", self.show_establishments, width=25)
        self.button.place(x=325, y=300)

        self.button = WidgetFactory.create_button(self.root, "Pagar uso de música", self.pay_music, width=25)
        self.button.place(x=325, y=350)

    def register_establishment(self) -> None:
        """
        Página de cadastro de um estabelecimento.
        """
        self.root_2 = WidgetFactory.create_popup("Cadastro de estabelecimento", 650, 550)

        self.img_logo, __ = WidgetFactory.create_image(self.root_2, "entrega_projeto_final/figs/ecad_login.png", (150, 150))
        self.img_logo.place(x=-10, y=400)

        self.title = WidgetFactory.create_title(self.root_2, "Cadastro de estabelecimento")
        self.title.place(x=100, y=70)

        self.text = WidgetFactory.create_text(self.root_2, "Preencha os campos abaixo para cadastrar um estabelecimento.")
        self.text.place(x=100, y=120)

        self.nome, self.nome_bar = WidgetFactory.create_entry(self.root_2, "Razão Social")
        self.nome.place(x=100, y=170)
        self.nome_bar.place(x=100, y=200)

        self.cnpj, self.cnpj_bar = WidgetFactory.create_cnpj(self.root_2)
        self.cnpj.place(x=100, y=240)
        self.cnpj_bar.place(x=100, y=270)

        self.option_list = ["Bar/Restaurante", "Rádio", "TV"]
        self.tipo = WidgetFactory.create_option_menu(self.root_2, "Selecione o tipo de estabelecimento", self.option_list, width=35)
        self.tipo.place(x=100, y=290)

        self.num_ambientes, self.num_ambientes_bar = WidgetFactory.create_entry(self.root_2, "N° de ambientes")
        self.num_ambientes.place(x=100, y=350)
        self.num_ambientes_bar.place(x=100, y=380)

        self.button = WidgetFactory.create_button(self.root_2, "Cadastrar", self.register, width=25)
        self.button.place(x=175, y=450)

    def register(self) -> None:
        """
        Cadastra um estabelecimento no banco de dados.
        """
        self.db = Database()

        self.nome = self.nome.get()
        self.cnpj = self.cnpj.get()
        self.tipo = self.tipo.cget("text")
        self.num_ambientes = self.num_ambientes.get()

        if self.nome == "" or self.cnpj == "" or self.tipo == "" or self.num_ambientes == "":
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        self.db.cursor.execute("SELECT COUNT (*) FROM estabelecimento WHERE cnpj_estabelecimento = ?", (self.cnpj,))
        self.result = self.db.cursor.fetchone()

        if self.result[0] > 0:
            messagebox.showerror("Erro", "Estabelecimento já cadastrado!")
            return
        
        self.db.cursor.execute("SELECT COUNT (*) FROM estabelecimento ")
        self.n = self.db.cursor.fetchone()  
        self.n = self.n[0] + 1
        
        self.db.cursor.execute("INSERT INTO estabelecimento VALUES (?, ?, ?, ?, ?, ?)", (self.n, self.cnpj, self.nome, self.tipo, self.num_ambientes, self.cod_proprietario))
        self.db.conn.commit()

        messagebox.showinfo("Sucesso", "Estabelecimento cadastrado com sucesso!")
        self.root_2.destroy()

    def show_establishments(self) -> None:
        """
        Página de visualização dos estabelecimentos cadastrados.
        """
        self.root_2 = WidgetFactory.create_popup("Estabelecimentos", 650, 550)

        self.img_logo, __ = WidgetFactory.create_image(self.root_2, "entrega_projeto_final/figs/ecad_login.png", (150, 150))
        self.img_logo.place(x=-10, y=400)

        self.title = WidgetFactory.create_title(self.root_2, "Estabelecimentos")
        self.title.place(x=100, y=70)

        self.text = WidgetFactory.create_text(self.root_2, "Selecione um estabelecimento para ver suas informações.")
        self.text.place(x=100, y=120)

        self.db = Database()

        self.db.cursor.execute("SELECT COUNT (*) FROM estabelecimento WHERE proprietario_cod_proprietario = ?", (self.cod_proprietario,))
        self.n = self.db.cursor.fetchone()[0]

        self.db.cursor.execute("SELECT razao_social FROM estabelecimento WHERE proprietario_cod_proprietario = ?", (self.cod_proprietario,))
        self.estabelecimentos = self.db.cursor.fetchall()

        self.option_list = []
        for i in range(self.n):
            self.option_list.append(self.estabelecimentos[i][0])

        self.estabelecimento = WidgetFactory.create_option_menu(self.root_2, "Selecione o estabelecimento", self.option_list, width=35)
        self.estabelecimento.place(x=100, y=170)

        self.button = WidgetFactory.create_button(self.root_2, "Ver", self.show, width=25)
        self.button.place(x=175, y=250)

    def show(self) -> None:
        """
        Mostra as informações de um estabelecimento.
        """
        self.db = Database()

        self.estabelecimento = self.estabelecimento.cget("text")

        self.db.cursor.execute("SELECT * FROM estabelecimento WHERE razao_social = ?", (self.estabelecimento,))
        self.result = self.db.cursor.fetchone()

        self.root_3 = WidgetFactory.create_popup("Informações do estabelecimento", 650, 550)

        self.img_logo, __ = WidgetFactory.create_image(self.root_3, "entrega_projeto_final/figs/ecad_login.png", (150, 150))
        self.img_logo.place(x=-10, y=400)

        self.title = WidgetFactory.create_title(self.root_3, "Informações do estabelecimento")
        self.title.place(x=100, y=70)

        self.text = WidgetFactory.create_text(self.root_3, "Veja abaixo as informações do estabelecimento selecionado.")
        self.text.place(x=100, y=120)

        self.text = WidgetFactory.create_text(self.root_3, f"Razão social: {self.result[2]}")
        self.text.place(x=100, y=170)

        self.text = WidgetFactory.create_text(self.root_3, f"CNPJ: {self.result[1]}")
        self.text.place(x=100, y=200)

        self.text = WidgetFactory.create_text(self.root_3, f"Tipo: {self.result[3]}")
        self.text.place(x=100, y=230)

        self.text = WidgetFactory.create_text(self.root_3, f"N° de ambientes: {self.result[4]}")
        self.text.place(x=100, y=260)

        self.text = WidgetFactory.create_text(self.root_3, f"Código do proprietário: {self.result[5]}")
        self.text.place(x=100, y=290)

    def pay_music(self) -> None:
        """
        Página de pagamento de uso de música.
        """
        self.root_2 = WidgetFactory.create_popup("Pagamento de uso de música", 650, 450)

        self.img_logo, __ = WidgetFactory.create_image(self.root_2, "entrega_projeto_final/figs/ecad_login.png", (150, 150))
        self.img_logo.place(x=-10, y=400)

        self.title = WidgetFactory.create_title(self.root_2, "Pagamento de uso de música")
        self.title.place(x=100, y=70)

        self.text = WidgetFactory.create_text(self.root_2, "Selecione um estabelecimento para pagar o uso de música.")
        self.text.place(x=100, y=120)

        self.db = Database()

        self.db.cursor.execute("SELECT COUNT (*) FROM estabelecimento WHERE proprietario_cod_proprietario = ?", (self.cod_proprietario,))
        self.n = self.db.cursor.fetchone()[0]

        self.db.cursor.execute("SELECT razao_social FROM estabelecimento WHERE proprietario_cod_proprietario = ?", (self.cod_proprietario,))
        self.estabelecimentos = self.db.cursor.fetchall()

        self.option_list = []
        for i in range(self.n):
            self.option_list.append(self.estabelecimentos[i][0])

        self.estabelecimento = WidgetFactory.create_option_menu(self.root_2, "Selecione o estabelecimento", self.option_list, width=35)
        self.estabelecimento.place(x=100, y=170)

        self.button_browse = WidgetFactory.create_button(self.root_2, "Escolher arquivo", self.open_file, width=25)
        self.button_browse.place(x=175, y=250)

        self.button_pay = WidgetFactory.create_button(self.root_2, "Pagar", self.pay, width=25)
        self.button_pay.place(x=175, y=300)

    def open_file(self) -> None:
        """
        Abre o arquivo de músicas.
        """
        self.file = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("Excel files", "*.xlsx"), ("all files", "*.*")))
        self.df = pd.read_excel(self.file)
        self.df.columns = ["Título da música", "Nome do artista"]
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates()
        self.df = self.df[["Título da música", "Nome do artista"]]

    def pay(self) -> None:
        """
        Paga o uso de música.
        """
        self.valores_por_musica = {
            "Bar/Restaurante": 4.5,
            "Rádio": 13.5,
            "TV": 22.5
        }

        self.db = Database()
        self.db.cursor.execute("SELECT tipo_estabelecimento, numero_ambientes FROM estabelecimento WHERE razao_social = ?", (self.estabelecimento.cget("text"),))
        self.result = self.db.cursor.fetchone()
        self.tipo_estabelecimento = self.result[0]
        self.numero_ambientes = self.result[1]

        self.valor_total = len(self.df) * self.valores_por_musica[self.tipo_estabelecimento] * self.numero_ambientes

        self.root_3 = WidgetFactory.create_popup("Pagamento de uso de música", 650, 350)

        self.img_logo, __ = WidgetFactory.create_image(self.root_3, "entrega_projeto_final/figs/ecad_login.png", (150, 150))
        self.img_logo.place(x=-10, y=400)

        self.title = WidgetFactory.create_title(self.root_3, "Pagamento de uso de música")
        self.title.place(x=100, y=70)

        self.text = WidgetFactory.create_text(self.root_3, f"Valor total a ser pago: R$ {self.valor_total}")
        self.text.place(x=100, y=120)

        self.button_confirm = WidgetFactory.create_button(self.root_3, "Confirmar pagamento", self.confirm, width=25)
        self.button_confirm.place(x=175, y=250)

    def confirm(self) -> None:
        """
        Confirma o pagamento de uso de música e insere os dados no banco de dados.
        """
        self.db = Database()
        self.db.cursor.execute("SELECT COUNT (*) FROM pagamento_rubrica")
        self.n = self.db.cursor.fetchone()[0] + 1

        self.db.cursor.execute("SELECT cod_estabelecimento FROM estabelecimento WHERE razao_social = ?", (self.estabelecimento.cget("text"),))
        self.cod_estabelecimento = self.db.cursor.fetchone()[0]

        self.lista_musicas = []
        for i in range(len(self.df)):
            self.lista_musicas.append((self.df.iloc[i, 0], self.df.iloc[i, 1]))

        for i in range(len(self.lista_musicas)):
            self.cod_musica = int(self.lista_musicas[i][0])
            self.db.cursor.execute("SELECT artista_cod_artista FROM relacao_artista_obra WHERE obra_cod_obra = ?", (self.cod_musica,))
            try:
                self.cod_artista = self.db.cursor.fetchone()[0]
                self.db.cursor.execute("SELECT associacao_cod_associacao FROM artista WHERE cod_artista = ?", (self.cod_artista,))
                self.cod_associacao = self.db.cursor.fetchone()[0]
                self.db.cursor.execute("INSERT INTO pagamento_rubrica VALUES (?, ?, ?, ?, ?, ?)", (self.n + i, self.cod_musica, self.cod_associacao, self.cod_estabelecimento, datetime.now().strftime(format="%Y-%m-%d"), self.valor_total/len(self.df)))
                self.db.conn.commit()
            except TypeError:
                continue

        messagebox.showinfo("Sucesso", "Pagamento realizado com sucesso!")
        self.root_3.destroy()
        self.root_2.destroy()