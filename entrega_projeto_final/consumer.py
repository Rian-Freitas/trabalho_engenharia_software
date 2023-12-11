from widget_factory import WidgetFactory
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
        self.root_2 = WidgetFactory.create_popup("Cadastro de estabelecimento", 700, 500)

        self.img_logo, __ = WidgetFactory.create_image(self.root_2, "entrega_projeto_final/figs/ecad_login.png", (150, 150))
        self.img_logo.place(x=-10, y=350)

        self.title = WidgetFactory.create_title(self.root_2, "Cadastro de estabelecimento")
        self.title.place(x=100, y=70)

        self.text = WidgetFactory.create_text(self.root_2, "Preencha os campos abaixo para cadastrar um estabelecimento.")
        self.text.place(x=100, y=120)


    def show_establishments(self):
        pass

    def pay_music(self):
        pass