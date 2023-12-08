from tkinter import *
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import sqlite3
import os

# Cria a janela de login
root = Tk()
root.title("Login")
root.geometry("925x500+300+200")
root.configure(background="#fff")
root.resizable(False, False)

def on_enter(e):
    entry = e.widget
    if entry.get() == "Login" or entry.get() == "Senha":
        entry.delete(0, END)
        entry.config(fg="#000")

def on_leave(e):
    entry = e.widget
    if entry.get() == "":
        entry.insert(0, "Login" if entry == user else "Senha")
        entry.config(fg="#000")

img_logo = ImageTk.PhotoImage(Image.open("entrega_projeto_final/figs/ecad_login.png").resize((150, 150), Image.LANCZOS))
Label(root, image=img_logo, bg="#fff").place(x=-10, y=350)

img_illustration = ImageTk.PhotoImage(Image.open("entrega_projeto_final/figs/illustration_login.png").resize((380, 380), Image.LANCZOS))
Label(root, image=img_illustration, bg="#fff").place(x=480, y=40)

frame = Frame(root, width=350, height=350, bg="#fff")
frame.place(x=80, y=20)

heading = Label(root, text="Bem-vindo ao Ecad", fg="#57a1f8", bg="#fff", font=("Microsoft Yahei UI Light", 23, "bold"))
heading.place(x=100, y=70)

user = Entry(frame, width=25, bg="#fff", fg="#000", border=0, font=("Microsoft Yahei UI Light", 11))
user.place(x=30, y=120)
user.insert(0, "Login")
user.bind("<FocusIn>", on_enter)
user.bind("<FocusOut>", on_leave)

password = Entry(frame, width=25, bg="#fff", fg="#000", border=0, font=("Microsoft Yahei UI Light", 11))
password.place(x=30, y=180)
password.insert(0, "Senha")
password.bind("<FocusIn>", on_enter)
password.bind("<FocusOut>", on_leave)

Frame(frame, width=295, height=2, bg="#000").place(x=25, y=147)
Frame(frame, width=295, height=2, bg="#000").place(x=25, y=207)

option_list = ["Para artistas", "Para associações", "Para consumidores"]
base_variable = StringVar()
base_variable.set("Selecione o tipo de usuário")

option_menu = OptionMenu(frame, base_variable, *option_list)
option_menu.config(width=25, bg="white", fg="black", border=1, font=("Microsoft Yahei UI Light", 11), activebackground="#a89157", activeforeground="#fff")
option_menu.place(x=50, y=240)

button = Button(frame, text="Entrar", width=10, bg="#fb6962", fg="#fff", border=0, font=("Microsoft Yahei UI Light", 11, "bold"), borderwidth=2, activebackground="#fff", activeforeground="#fb6962")
button.place(x=120, y=310)

frame_sign_up = Frame(root, width=350, height=30, bg="#fff")
frame_sign_up.place(x=480, y=420)

sign_up_text = Label(frame_sign_up, text="Não tem uma conta?", fg="#000", bg="#fff", font=("Microsoft Yahei UI Light", 11))
sign_up_text.place(x=75, y=0)

sign_up_button = Button(frame_sign_up, text="Cadastre-se", width=10, bg="#fff", fg="#fb6962", border=0, font=("Microsoft Yahei UI Light", 10, "bold"), cursor="hand2")
sign_up_button.place(x=220, y=-2)

root.mainloop()