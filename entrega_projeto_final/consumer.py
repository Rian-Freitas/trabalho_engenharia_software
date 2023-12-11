from widget_factory import WidgetFactory
from database import Database
from tkinter import *
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk

class consumerPage:
    def __init__(self, info: list) -> None:
        self.info = info
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

    def register_establishment(self):
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

    def register(self):
        self.db = Database()

        self.nome = self.nome.get()
        self.cnpj = self.cnpj.get()
        self.tipo = self.tipo.cget("text")
        self.num_ambientes = self.num_ambientes.get()

        if self.nome == "" or self.cnpj == "" or self.tipo == "" or self.num_ambientes == "":
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        self.db.cursor.execute("SELECT COUNT(*) FROM estabelecimento WHERE cnpj_estabelecimento = ?", (self.cnpj,))
        self.result = self.db.cursor.fetchone()
        print(self.result)

        if self.result[0] > 0:
            messagebox.showerror("Erro", "Estabelecimento já cadastrado!")
            return
        
        self.db.cursor.execute("INSERT INTO estabelecimentos VALUES (?, ?, ?, ?)", (self.nome, self.cnpj, self.tipo, self.num_ambientes))

    def show_establishments(self):
        pass

    def pay_music(self):
        pass