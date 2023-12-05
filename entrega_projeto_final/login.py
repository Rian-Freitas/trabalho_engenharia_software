from tkinter import *
from tkinter import messagebox
import sqlite3
import os

# Cria a janela de login
class Login:
    def __init__(self):
        self.root = Tk()
        self.root.title("Login")
        self.root.geometry("925x500")
        self.root.resizable(False, False)
        self.root.configure(background="#f7f7f2")
        self.root.iconbitmap(os.path.join(os.path.dirname(__file__), "figs\icone.ico"))

        # Imagem da lateral
        self.img = PhotoImage(file=os.path.join(os.path.dirname(__file__), r"figs\Nova_logomarca_do_Ecad.png")).subsample(4,4)
        self.lbl_img = Label(self.root, image=self.img, bg="#f7f7f2")
        self.lbl_img.place(x=-100, y=-70)

        # Conecta ao banco de dados
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

        # Cria os widgets
        self.widgets()

        # Inicia a janela
        self.root.mainloop()
    
    # Cria os widgets
    def widgets(self):
        # Cria o frame
        self.frame = Frame(self.root, bd=1, bg="#dde", highlightbackground="#999", highlightthickness=1)
        self.frame.place(x=600, y=100)

        # Cria o label de usuário
        self.lbl_usuario = Label(self.frame, text="Usuário:", bg="#dde", fg="#009", font=("Century Gothic", 12))
        self.lbl_usuario.pack()

        # Cria a caixa de texto de usuário
        self.txt_usuario = Entry(self.frame, font=("Century Gothic", 12))
        self.txt_usuario.pack()

        # Cria o label de senha
        self.lbl_senha = Label(self.frame, text="Senha:", bg="#dde", fg="#009", font=("Century Gothic", 12))
        self.lbl_senha.pack()

        # Cria a caixa de texto de senha
        self.txt_senha = Entry(self.frame, font=("Century Gothic", 12), show="*")
        self.txt_senha.pack()

        # Cria o botão de login
        self.btn_login = Button(self.frame, text="Login", font=("Century Gothic", 12), command=self.login)
        self.btn_login.pack(pady=10)

        # Cria o botão de cadastro
        self.btn_cadastro = Button(self.frame, text="Cadastro", font=("Century Gothic", 12), command=self.cadastro)
        self.btn_cadastro.pack()

    # Função de login
    def login(self):
        # Pega os dados do usuário e senha
        usuario = self.txt_usuario.get()
        senha = self.txt_senha.get()

        # Verifica se os campos estão vazios
        if (usuario == "" or senha == ""):
            messagebox.showerror("Erro", "Preencha todos os campos!")
        else:
            # Verifica se o usuário existe
            self.cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
            self.conn.commit()
            usuario = self.cursor.fetchone()

            # Se o usuário existir, entra no sistema
            if (usuario != None):
                self.root.destroy()
                # from home import Home
                # Home()
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    # Função de cadastro
    def cadastro(self):
        # Pega os dados do usuário e senha
        usuario = self.txt_usuario.get()
        senha = self.txt_senha.get()

        # Verifica se os campos estão vazios
        if (usuario == "" or senha == ""):
            messagebox.showerror("Erro", "Preencha todos os campos!")
        else:
            # Verifica se o usuário existe
            self.cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
            self.conn.commit()
            usuario = self.cursor.fetchone()

            # Se o usuário existir, mostra um erro
            if (usuario != None):
                messagebox.showerror("Erro", "Usuário já existe!")
            else:
                # Cadastra o usuário
                self.cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.root.destroy()

# Inicia o programa
if (__name__ == "__main__"):
    Login()    