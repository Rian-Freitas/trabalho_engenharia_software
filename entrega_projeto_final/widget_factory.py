from tkinter import *
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk

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
    def create_button(frame, text, command, width=10, in_text=False):
        if not in_text:
            return Button(frame, text=text, width=width, bg="#fb6962", fg="#fff", border=0, font=("Microsoft Yahei UI Light", 11, "bold"), borderwidth=2, activebackground="#fff", activeforeground="#fb6962", command=command)
        else:
            return Button(frame, text=text, width=width, bg="#fff", fg="#fb6962", border=0, font=("Microsoft Yahei UI Light", 10, "bold"), cursor="hand2", command=command)

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
