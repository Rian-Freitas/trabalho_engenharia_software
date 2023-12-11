from tkinter import *
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import sqlite3
import os

class Database:
    _instance = None

    def __new__(cls):
        if Database._instance is None:
            Database._instance = object.__new__(cls)
        return Database._instance

    def __init__(self):
        self.conn = sqlite3.connect("entrega_projeto_final\database.db")
        self.cursor = self.conn.cursor()

class WidgetFactory:

    @staticmethod
    def create_window(title, width, height, icon=None, bg="#fff"):
        window = Tk()
        window.title(title)
        window.geometry(f"{width}x{height}+300+200")
        window.configure(background=bg)
        window.resizable(False, False)

        if icon:
            img = ImageTk.PhotoImage(Image.open(icon).resize((250, 250), Image.LANCZOS))
            window.iconphoto(False, img)
        return window
    
    @staticmethod
    def create_popup(title, width, height, icon=None, bg="#fff"):
        popup = Toplevel()
        popup.title(title)
        popup.geometry(f"{width}x{height}+300+200")
        popup.configure(background=bg)
        popup.resizable(False, False)

        if icon:
            img = ImageTk.PhotoImage(Image.open(icon).resize((250, 250), Image.LANCZOS))
            popup.iconphoto(False, img)
        return popup

    @staticmethod
    def create_frame(root, width, height, bg="#fff"):
        return Frame(root, width=width, height=height, bg=bg)

    @staticmethod
    def format_cpf(e):
        entry = e.widget
        text = entry.get().replace(".", "").replace("-", "")[:11]
        new_text = ""

        if e.keysym.lower() == "backspace": return
        
        for index in range(len(text)):
            
            if not text[index] in "0123456789": continue
            if index in [2, 5]: new_text += text[index] + "."
            elif index == 8: new_text += text[index] + "-"
            else: new_text += text[index]

        entry.delete(0, "end")
        entry.insert(0, new_text)

    @staticmethod
    def format_cnpj(e):
        entry = e.widget
        text = entry.get().replace(".", "").replace("-", "").replace("/", "")[:14]
        new_text = ""

        if e.keysym.lower() == "backspace": return
        
        for index in range(len(text)):
            
            if not text[index] in "0123456789": continue
            if index in [1, 4]: new_text += text[index] + "."
            elif index == 7: new_text += text[index] + "/"
            elif index == 11: new_text += text[index] + "-"
            else: new_text += text[index]

        entry.delete(0, "end")
        entry.insert(0, new_text)

    @staticmethod
    def entry_on_enter(e, field, password=False):
        entry = e.widget
        if entry.get() == field:
            entry.delete(0, END)
            entry.config(fg="#000")
            if password:
                entry.config(show="*")

    @staticmethod
    def entry_on_leave(e, field, password=False): 
        entry = e.widget
        if entry.get() == "":
            entry.insert(0, field)
            entry.config(show="" if password else None, fg="#000")

    @staticmethod
    def create_text(frame, text):
        return Label(frame, text=text, bg="#fff", fg="#000", font=("Microsoft Yahei UI Light", 11))

    @staticmethod
    def create_title(frame, text):
        return Label(frame, text=text, fg="#57a1f8", bg="#fff", font=("Microsoft Yahei UI Light", 23, "bold"))

    @staticmethod
    def create_entry(frame, text, password=False):
        entry = Entry(frame, width=25, bg="#fff", fg="#000", border=0, font=("Microsoft Yahei UI Light", 11))
        bar_entry = Frame(frame, width=295, height=2, bg="#000")

        entry.insert(0, text)

        entry.bind("<FocusIn>", lambda e: WidgetFactory.entry_on_enter(e, text, password))
        entry.bind("<FocusOut>", lambda e: WidgetFactory.entry_on_leave(e, text, password))
        return entry, bar_entry

    @staticmethod
    def create_button(frame, text, command, in_text=False):
        if not in_text:
            return Button(frame, text=text, width=10, bg="#fb6962", fg="#fff", border=0, font=("Microsoft Yahei UI Light", 11, "bold"), borderwidth=2, activebackground="#fff", activeforeground="#fb6962", command=command)
        else:
            return Button(frame, text=text, width=10, bg="#fff", fg="#fb6962", border=0, font=("Microsoft Yahei UI Light", 10, "bold"), cursor="hand2", command=command)

    @staticmethod
    def create_option_menu(frame, text, option_list, width=25):
        base_variable = StringVar()
        base_variable.set(text)
        option_menu = OptionMenu(frame, base_variable, *option_list)
        option_menu.config(width=width, bg="white", fg="black", border=1, font=("Microsoft Yahei UI Light", 11), activebackground="#a89157", activeforeground="#fff")
        return option_menu
    
    @staticmethod
    def create_image(frame, path, size):
        image = ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
        return Label(frame, image=image, bg="#fff"), image
    
    @staticmethod
    def create_cpf(frame):
        cpf = Entry(frame, width=25, bg="#fff", fg="#000", border=0, font=("Microsoft Yahei UI Light", 11))
        bar_cpf = Frame(frame, width=295, height=2, bg="#000")

        cpf.insert(0, "CPF")

        cpf.bind("<FocusIn>", lambda e: WidgetFactory.entry_on_enter(e, field="CPF"))
        cpf.bind("<FocusOut>", lambda e: WidgetFactory.entry_on_leave(e, field="CPF"))
        cpf.bind("<KeyRelease>", WidgetFactory.format_cpf)
        return cpf, bar_cpf
    
    @staticmethod
    def create_cnpj(frame):
        cnpj = Entry(frame, width=25, bg="#fff", fg="#000", border=0, font=("Microsoft Yahei UI Light", 11))
        bar_cnpj = Frame(frame, width=295, height=2, bg="#000")

        cnpj.insert(0, "CNPJ")

        cnpj.bind("<FocusIn>", lambda e: WidgetFactory.entry_on_enter(e, field="CNPJ"))
        cnpj.bind("<FocusOut>", lambda e: WidgetFactory.entry_on_leave(e, field="CNPJ"))
        cnpj.bind("<KeyRelease>", WidgetFactory.format_cnpj)
        return cnpj, bar_cnpj

class Handler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, fields: list) -> bool:
        handled = self._handle(fields)
        if not handled and self._successor:
            return self._successor.handle(fields)
        



    def _handle(self, fields: list) -> bool:
        return True

# Classe a seguir foi feita a partir de TDD

# class EmptyFieldsHandler(Handler):
#     def _handle(self, name, password) -> bool:
#         pass

# class EmptyFieldsHandler(Handler):
#     def _handle(self, usuario, senha) -> bool:
#         if usuario == "" or senha == "":
#             messagebox.showerror("Erro", "Preencha todos os campos!")
#             return True
#         return False
    
# Versão final da classe EmptyFieldsHandler
class EmptyFieldsHandler(Handler):
    
    def _handle(self, fiedls: list) -> bool:
        if any(field == "" for field in fiedls):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return True
        return False
        
# A classe a seguir foi feita a partir de TDD

# class UserExistsHandler(Handler):
#     def _handle(self, usuario, senha) -> bool:
#         pass

# class UserExistsHandler(Handler):
#     def _handle(self, usuario, senha) -> bool:
#         db = Database()
#         db.cursor.execute("SELECT * FROM artista WHERE nome_artista = ?", (usuario,))
#         db.conn.commit()
#         user = db.cursor.fetchone()

#         if user is not None:
#             messagebox.showerror("Erro", "Usuário já cadastrado!")
#             return True
#         return False

# Versão final da classe UserExistsHandler
class UserExistsHandler(Handler):
    def __init__(self, successor=None, db=None, root=None):
        super().__init__(successor)
        self._db = db

    def _handle(self, fields: list) -> bool:
        self.table_names = {
            "Para artistas": "artista",
            "Para associações": "associacao",
            "Para consumidores": "proprietario"
        }

        self.colmun_names = {
            "Para artistas": "cpf",
            "Para associações": "cnpj",
            "Para consumidores": "cpf"
        }

        self._db.cursor.execute(f"SELECT * FROM {self.table_names[fields[5]]} WHERE {self.colmun_names[fields[5]] + '_' + self.table_names[fields[5]]} = ?", (fields[2],))
        self._db.conn.commit()
        user =  self._db.cursor.fetchone()

        if user is not None:
            messagebox.showerror("Erro", "Usuário já cadastrado!")
            return True
        return False
    
class AssociationNotFoundHandler(Handler):
    def __init__(self, successor=None, db=None, root=None):
        super().__init__(successor)
        self._db = db
        self._root = root

    def _handle(self, fields: list) -> bool:
        if fields[5] != "Para artistas": return False

        self._db.cursor.execute(f"SELECT * FROM associacao WHERE nome_associacao = ?", (fields[4],))
        self._db.conn.commit()
        association = self._db.cursor.fetchone()

        if association is None:
            messagebox.showerror("Erro", "Associação não encontrada!")
            return True
        return False
    
class PasswordsDontMatchHandler(Handler):
    def __init__(self, successor=None, db=None, root=None):
        super().__init__(successor)
        self._db = db
        self._root = root

    def _handle(self, fields: list) -> bool:
        if fields[2] != fields[6]:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return True
        return False

class LoginHandler(Handler):
    def __init__(self, successor=None, db=None, root=None):
        super().__init__(successor)
        self._db = db
        self._root = root

        self.table_names = {
            "Para artistas": "artista",
            "Para associações": "associacao",
            "Para consumidores": "consumidor"
        }



    def _handle(self, fields: list) -> bool:
        self.table_names = {
            "Para artistas": "artista",
            "Para associações": "associacao",
            "Para consumidores": "proprietario"
        }

        usuario = fields[0]
        senha = fields[1]
        tipo_usuario = fields[2]

        self._db.cursor.execute(f"SELECT * FROM {self.table_names[tipo_usuario]} WHERE {'email_' + self.table_names[tipo_usuario]} = ? AND {'senha_' + self.table_names[tipo_usuario]} = ?", (usuario, senha))
        self._db.conn.commit()
        user = self._db.cursor.fetchone()
        
        if user is None:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
            return True
        
        self._root.destroy()
        return False
    
class SignUpHandler(Handler):
    def __init__(self, successor=None, db=None, root=None):
        super().__init__(successor)
        self._db = db
        self._root = root

    def _handle(self, fields: list):
        self.table_names = {
            "Para artistas": "artista",
            "Para associações": "associacao",
            "Para consumidores": "proprietario"
        }

        self.colmun_names = {
            "Para artistas": "cpf",
            "Para associações": "cnpj",
            "Para consumidores": "cpf"
        }

        self._db.cursor.execute(f"SELECT COUNT(*) FROM {self.table_names[fields[5]]}")
        self._db.conn.commit()
        count = self._db.cursor.fetchone()[0]
        n = count + 1

        if "Para artistas" in fields:
            self._db.cursor.execute(f"SELECT cod_associacao FROM associacao WHERE nome_associacao = ?", (fields[4],))
            self._db.conn.commit()
            cod_associacao = self._db.cursor.fetchone()[0]
            
            self._db.cursor.execute(f"INSERT INTO artista VALUES (?, ?, ?, ?, ?, ?)", (n, fields[0], fields[1], fields[2], fields[3], cod_associacao))

        elif "Para associações" in fields:
            self._db.cursor.execute(f"INSERT INTO associacao VALUES (?, ?, ?, ?, ?)", (n, fields[0], fields[1], fields[2], fields[3]))

        else:
            self._db.cursor.execute(f"INSERT INTO proprietario VALUES (?, ?, ?, ?, ?)", (n, fields[3], fields[0], fields[1], fields[2]))

        self._db.conn.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self._root.destroy()
    
class SignUp:
    def __init__(self):
        self.root_2 = WidgetFactory.create_popup("Cadastro", 525, 250)

        self.frame_2 = WidgetFactory.create_frame(self.root_2, 350, 600)
        self.frame_2.place(x=80, y=20)

        self.heading_2 = WidgetFactory.create_title(self.root_2, "Faça parte do Ecad")
        self.heading_2.place(x=100, y=30)

        self.option_list_2 = ["Para artistas", "Para associações", "Para consumidores"]
        self.option_menu_2 = WidgetFactory.create_option_menu(self.frame_2, "Selecione o tipo de usuário", self.option_list_2)
        self.option_menu_2.place(x=50, y=80)

        self.button_2 = WidgetFactory.create_button(self.frame_2, "Selecionar", self.select_option)
        self.button_2.place(x=120, y=150)

        self.root_2.mainloop()

    def select_option(self):
        self.option = self.option_menu_2.cget("text")
        if self.option == "Para artistas":
            self.artist()
        elif self.option == "Para associações":
            self.association()
        else:
            self.consumer()

    def artist(self):
        self.root_2.geometry("525x600+300+200")
        self.option_menu_2.destroy()
        self.button_2.destroy()

        self.name, self.bar_name = WidgetFactory.create_entry(self.frame_2, "Nome completo")
        self.name.place(x=30, y=120)
        self.bar_name.place(x=25, y=147)

        self.email, self.bar_email = WidgetFactory.create_entry(self.frame_2, "E-mail")
        self.email.place(x=30, y=180)
        self.bar_email.place(x=25, y=207)

        self.cpf, self.bar_cpf = WidgetFactory.create_cpf(self.frame_2)
        self.cpf.place(x=30, y=240)
        self.bar_cpf.place(x=25, y=267) 

        self.association, self.bar_association = WidgetFactory.create_entry(self.frame_2, "Associação")
        self.association.place(x=30, y=300)
        self.bar_association.place(x=25, y=327)

        self.senha, self.bar_senha = WidgetFactory.create_entry(self.frame_2, "Senha", password=True)
        self.senha.place(x=30, y=360)
        self.bar_senha.place(x=25, y=387)

        self.senha_confirm, self.bar_senha_confirm = WidgetFactory.create_entry(self.frame_2, "Confirmar senha", password=True)
        self.senha_confirm.place(x=30, y=420)
        self.bar_senha_confirm.place(x=25, y=447)

        self.button_3 = WidgetFactory.create_button(self.frame_2, "Cadastrar", self.sign_up)
        self.button_3.place(x=120, y=500)

    def association(self):
        self.root_2.geometry("525x540+300+200")
        self.option_menu_2.destroy()
        self.button_2.destroy()

        self.name, self.bar_name = WidgetFactory.create_entry(self.frame_2, "Razão social")
        self.name.place(x=30, y=120)
        self.bar_name.place(x=25, y=147)

        self.association = None

        self.email, self.bar_email = WidgetFactory.create_entry(self.frame_2, "E-mail da associação")
        self.email.place(x=30, y=180)
        self.bar_email.place(x=25, y=207)

        self.cnpj, self.bar_cnpj = WidgetFactory.create_cnpj(self.frame_2)
        self.cnpj.place(x=30, y=240)
        self.bar_cnpj.place(x=25, y=267)
        self.cpf = None

        self.senha, self.bar_senha = WidgetFactory.create_entry(self.frame_2, "Senha", password=True)
        self.senha.place(x=30, y=300)
        self.bar_senha.place(x=25, y=327)

        self.senha_confirm, self.bar_senha_confirm = WidgetFactory.create_entry(self.frame_2, "Confirmar senha", password=True)
        self.senha_confirm.place(x=30, y=360)
        self.bar_senha_confirm.place(x=25, y=387)

        self.button_3 = WidgetFactory.create_button(self.frame_2, "Cadastrar", self.sign_up)
        self.button_3.place(x=120, y=440)

    def consumer(self):
        self.root_2.geometry("525x540+300+200")
        self.option_menu_2.destroy()
        self.button_2.destroy()

        self.name, self.bar_name = WidgetFactory.create_entry(self.frame_2, "Nome completo")
        self.name.place(x=30, y=120)
        self.bar_name.place(x=25, y=147)

        self.email, self.bar_email = WidgetFactory.create_entry(self.frame_2, "E-mail")
        self.email.place(x=30, y=180)
        self.bar_email.place(x=25, y=207)

        self.association = None

        self.cpf, self.bar_cpf = WidgetFactory.create_cpf(self.frame_2)
        self.cpf.place(x=30, y=240)
        self.bar_cpf.place(x=25, y=267)

        self.senha, self.bar_senha = WidgetFactory.create_entry(self.frame_2, "Senha", password=True)
        self.senha.place(x=30, y=300)
        self.bar_senha.place(x=25, y=327)

        self.senha_confirm, self.bar_senha_confirm = WidgetFactory.create_entry(self.frame_2, "Confirmar senha", password=True)
        self.senha_confirm.place(x=30, y=360)
        self.bar_senha_confirm.place(x=25, y=387)

        self.button_3 = WidgetFactory.create_button(self.frame_2, "Cadastrar", self.sign_up)
        self.button_3.place(x=120, y=440)

    def sign_up(self):
        name = self.name.get()
        email = self.email.get()
        senha = self.senha.get()
        senha_confirm = self.senha_confirm.get()
        
        codigo = self.cpf.get() if self.cpf else self.cnpj.get()
        associacao = self.association.get() if self.association else None
        tipo_usuario = self.option

        info = [name, email, senha, codigo, associacao, tipo_usuario, senha_confirm]

        db = Database()
        empty_fields_handler = EmptyFieldsHandler()
        user_exists_handler = UserExistsHandler(db=db, root=self.root_2)
        passwords_dont_match_handler = PasswordsDontMatchHandler(db=db, root=self.root_2)
        association_not_found_handler = AssociationNotFoundHandler(db=db, root=self.root_2)
        sign_up_handler = SignUpHandler(db=db, root=self.root_2)

        empty_fields_handler._successor = user_exists_handler
        user_exists_handler._successor = passwords_dont_match_handler
        passwords_dont_match_handler._successor = association_not_found_handler
        association_not_found_handler._successor = sign_up_handler

        empty_fields_handler.handle(info)
class Login:
    def __init__(self):
        self.root = WidgetFactory.create_window("Login", 925, 500)

        self.img_logo, __ = WidgetFactory.create_image(self.root, "entrega_projeto_final/figs/ecad_login.png", (150, 150))
        self.img_logo.place(x=-10, y=350)

        self.img_illustration, _ = WidgetFactory.create_image(self.root, "entrega_projeto_final/figs/illustration_login.png", (380, 380))
        self.img_illustration.place(x=480, y=40)

        self.frame = WidgetFactory.create_frame(self.root, 350, 350)
        self.frame.place(x=80, y=20)


        self.heading = WidgetFactory.create_title(self.root, "Bem-vindo ao Ecad")
        self.heading.place(x=100, y=70)

        self.user, self.bar_user = WidgetFactory.create_entry(self.frame, "Login")
        self.user.place(x=30, y=120)
        self.bar_user.place(x=25, y=147)

        self.password, self.bar_password = WidgetFactory.create_entry(self.frame, "Senha", password=True)
        self.password.place(x=30, y=180)
        self.bar_password.place(x=25, y=207)

        self.option_list = ["Para artistas", "Para associações", "Para consumidores"]
        self.option_menu = WidgetFactory.create_option_menu(self.frame, "Selecione o tipo de usuário", self.option_list)
        self.option_menu.place(x=50, y=240)

        self.enter_button = WidgetFactory.create_button(self.frame, "Entrar", self.login)
        self.enter_button.place(x=120, y=310)

        self.frame_sign_up = WidgetFactory.create_frame(self.root, 350, 30)
        self.frame_sign_up.place(x=480, y=420)

        self.sign_up_text = WidgetFactory.create_text(self.frame_sign_up, "Não tem uma conta?")
        self.sign_up_text.place(x=75, y=0)

        self.sign_up_button = WidgetFactory.create_button(self.frame_sign_up, "Cadastre-se", SignUp, in_text=True)
        self.sign_up_button.place(x=220, y=-2)

        self.root.mainloop()

    def login(self):
        usuario = self.user.get()
        senha = self.password.get()
        tipo_usuario = self.option_menu.cget("text")
        
        info = [usuario, senha, tipo_usuario]

        db = Database()
        empty_fields_handler = EmptyFieldsHandler()
        login_handler = LoginHandler(db=db, root=self.root)

        empty_fields_handler._successor = login_handler

        empty_fields_handler.handle(info)


if __name__ == "__main__":
    login = Login()




# # Cria a janela de login
# root = Tk()
# root.title("Login")
# root.geometry("925x500+300+200")
# root.configure(background="#fff")
# root.resizable(False, False)

# def on_enter(e):
#     entry = e.widget
#     if entry.get() == "Login" or entry.get() == "Senha":
#         entry.delete(0, END)
#         entry.config(fg="#000")

# def on_leave(e):
#     entry = e.widget
#     if entry.get() == "":
#         entry.insert(0, "Login" if entry == user else "Senha")
#         entry.config(fg="#000")

# img_logo = ImageTk.PhotoImage(Image.open("entrega_projeto_final/figs/ecad_login.png").resize((150, 150), Image.LANCZOS))
# Label(root, image=img_logo, bg="#fff").place(x=-10, y=350)

# img_illustration = ImageTk.PhotoImage(Image.open("entrega_projeto_final/figs/illustration_login.png").resize((380, 380), Image.LANCZOS))
# Label(root, image=img_illustration, bg="#fff").place(x=480, y=40)

# frame = Frame(root, width=350, height=350, bg="#fff")
# frame.place(x=80, y=20)

# heading = Label(root, text="Bem-vindo ao Ecad", fg="#57a1f8", bg="#fff", font=("Microsoft Yahei UI Light", 23, "bold"))
# heading.place(x=100, y=70)

# user = Entry(frame, width=25, bg="#fff", fg="#000", border=0, font=("Microsoft Yahei UI Light", 11))
# user.place(x=30, y=120)
# user.insert(0, "Login")
# user.bind("<FocusIn>", on_enter)
# user.bind("<FocusOut>", on_leave)

# password = Entry(frame, width=25, bg="#fff", fg="#000", border=0, font=("Microsoft Yahei UI Light", 11))
# password.place(x=30, y=180)
# password.insert(0, "Senha")
# password.bind("<FocusIn>", on_enter)
# password.bind("<FocusOut>", on_leave)

# Frame(frame, width=295, height=2, bg="#000").place(x=25, y=147)
# Frame(frame, width=295, height=2, bg="#000").place(x=25, y=207)

# option_list = ["Para artistas", "Para associações", "Para consumidores"]
# base_variable = StringVar()
# base_variable.set("Selecione o tipo de usuário")

# option_menu = OptionMenu(frame, base_variable, *option_list)
# option_menu.config(width=25, bg="white", fg="black", border=1, font=("Microsoft Yahei UI Light", 11), activebackground="#a89157", activeforeground="#fff")
# option_menu.place(x=50, y=240)

# button = Button(frame, text="Entrar", width=10, bg="#fb6962", fg="#fff", border=0, font=("Microsoft Yahei UI Light", 11, "bold"), borderwidth=2, activebackground="#fff", activeforeground="#fb6962")
# button.place(x=120, y=310)

# frame_sign_up = Frame(root, width=350, height=30, bg="#fff")
# frame_sign_up.place(x=480, y=420)

# sign_up_text = Label(frame_sign_up, text="Não tem uma conta?", fg="#000", bg="#fff", font=("Microsoft Yahei UI Light", 11))
# sign_up_text.place(x=75, y=0)

# sign_up_button = Button(frame_sign_up, text="Cadastre-se", width=10, bg="#fff", fg="#fb6962", border=0, font=("Microsoft Yahei UI Light", 10, "bold"), cursor="hand2")
# sign_up_button.place(x=220, y=-2)

# root.mainloop()