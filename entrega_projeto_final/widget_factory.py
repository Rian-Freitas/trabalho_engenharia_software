from tkinter import *
from PIL import Image
from PIL import ImageTk

class WidgetFactory:
    """
    Classe responsável por criar os widgets da aplicação.
    """
    @staticmethod
    def create_window(title: str, width: int, height: int, icon: str=None, bg: str="#fff") -> Tk:
        """
        Cria uma janela.

        :param title: Título da janela.
        :param width: Largura da janela.    
        :param height: Altura da janela.
        :param icon: Ícone da janela.
        :param bg: Cor de fundo da janela.

        :return: Janela criada.
        """
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
    def create_popup(title: str, width: int, height: int, icon: str=None, bg: str="#fff") -> Tk:
        """
        Cria uma janela popup.

        :param title: Título da janela.
        :param width: Largura da janela.
        :param height: Altura da janela.
        :param icon: Ícone da janela.
        :param bg: Cor de fundo da janela.

        :return: Janela criada.
        """
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
    def create_frame(root: Tk, width: int, height: int, bg: str="#fff") -> Frame:
        """
        Cria um frame.

        :param root: Janela onde o frame será criado.
        :param width: Largura do frame.
        :param height: Altura do frame.
        :param bg: Cor de fundo do frame.

        :return: Frame criado.
        """
        return Frame(root, width=width, height=height, bg=bg)

    @staticmethod
    def format_cpf(e: Event) -> None:
        """
        Formata o CPF digitado pelo usuário.

        :param e: Evento que disparou a função.
        """
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
    def format_cnpj(e: Event) -> None:
        """
        Formata o CNPJ digitado pelo usuário.

        :param e: Evento que disparou a função.
        """
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
    def entry_on_enter(e: Event, field: str, password: bool=False) -> None:
        """
        Evento disparado quando o usuário clica em um campo de entrada.

        :param e: Evento que disparou a função.
        :param field: Texto do campo de entrada.
        :param password: Se o campo de entrada é de senha ou não.
        """
        entry = e.widget
        if entry.get() == field:
            entry.delete(0, END)
            entry.config(fg="#000")
            if password:
                entry.config(show="*")

    @staticmethod
    def entry_on_leave(e: Event, field: str, password: bool=False) -> None:
        """ 
        Evento disparado quando o usuário sai de um campo de entrada.
        
        :param e: Evento que disparou a função.
        :param field: Texto do campo de entrada.
        :param password: Se o campo de entrada é de senha ou não.
        """
        entry = e.widget
        if entry.get() == "":
            entry.insert(0, field)
            entry.config(show="" if password else None, fg="#000")

    @staticmethod
    def create_text(frame: Frame, text: str) -> Label:
        """
        Cria um texto.

        :param frame: Frame onde o texto será criado.
        :param text: Texto a ser criado.

        :return: Texto criado.
        """
        return Label(frame, text=text, bg="#fff", fg="#000", font=("Microsoft Yahei UI Light", 11))

    @staticmethod
    def create_title(frame: Frame, text: str) -> Label:
        """
        Cria um título.

        :param frame: Frame onde o título será criado.
        :param text: Texto do título.

        :return: Título criado.
        """ 
        return Label(frame, text=text, fg="#57a1f8", bg="#fff", font=("Microsoft Yahei UI Light", 23, "bold"))

    @staticmethod
    def create_entry(frame: Frame, text: str, password: bool=False) -> tuple[Entry, Frame]:
        """
        Cria um campo de entrada.

        :param frame: Frame onde o campo de entrada será criado.
        :param text: Texto do campo de entrada.
        :param password: Se o campo de entrada é de senha ou não.

        :return: Campo de entrada criado.
        """
        entry = Entry(frame, width=25, bg="#fff", fg="#000", border=0, font=("Microsoft Yahei UI Light", 11))
        bar_entry = Frame(frame, width=295, height=2, bg="#000")

        entry.insert(0, text)

        entry.bind("<FocusIn>", lambda e: WidgetFactory.entry_on_enter(e, text, password))
        entry.bind("<FocusOut>", lambda e: WidgetFactory.entry_on_leave(e, text, password))
        return entry, bar_entry

    @staticmethod
    def create_button(frame: Frame, text: str, width: int, command: callable, in_text: bool=False) -> Button:
        """
        Cria um botão.

        :param frame: Frame onde o botão será criado.
        :param text: Texto do botão.
        :param width: Largura do botão.
        :param command: Função que será executada quando o botão for clicado.
        :param in_text: Se o botão está dentro de um texto ou não.

        :return: Botão criado.
        """
        if not in_text:
            return Button(frame, text=text, width=width, bg="#fb6962", fg="#fff", border=0, font=("Microsoft Yahei UI Light", 11, "bold"), borderwidth=2, activebackground="#fff", activeforeground="#fb6962", command=command)
        else:
            return Button(frame, text=text, width=width, bg="#fff", fg="#fb6962", border=0, font=("Microsoft Yahei UI Light", 10, "bold"), cursor="hand2", command=command)

    @staticmethod
    def create_option_menu(frame: Frame, text: str, option_list: list, width: int) -> OptionMenu:
        """
        Cria um menu de opções.

        :param frame: Frame onde o menu de opções será criado.
        :param text: Texto do menu de opções.
        :param option_list: Lista de opções do menu.
        :param width: Largura do menu de opções.

        :return: Menu de opções criado.
        """
        base_variable = StringVar()
        base_variable.set(text)
        option_menu = OptionMenu(frame, base_variable, *option_list)
        option_menu.config(width=width, bg="white", fg="black", border=1, font=("Microsoft Yahei UI Light", 11), activebackground="#a89157", activeforeground="#fff")
        return option_menu
    
    @staticmethod
    def create_image(frame: Frame, path: str, size: tuple[int, int]) -> tuple[Label, ImageTk.PhotoImage]:
        """
        Cria uma imagem.

        :param frame: Frame onde a imagem será criada.
        :param path: Caminho da imagem.
        :param size: Tamanho da imagem.

        :return: Imagem criada.
        """
        image = ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
        return Label(frame, image=image, bg="#fff"), image
    
    @staticmethod
    def create_cpf(frame : Frame) -> tuple[Entry, Frame]:
        """
        Cria um campo de entrada para CPF.

        :param frame: Frame onde o campo de entrada será criado.

        :return: Campo de entrada criado.
        """
        cpf = Entry(frame, width=25, bg="#fff", fg="#000", border=0, font=("Microsoft Yahei UI Light", 11))
        bar_cpf = Frame(frame, width=295, height=2, bg="#000")

        cpf.insert(0, "CPF")

        cpf.bind("<FocusIn>", lambda e: WidgetFactory.entry_on_enter(e, field="CPF"))
        cpf.bind("<FocusOut>", lambda e: WidgetFactory.entry_on_leave(e, field="CPF"))
        cpf.bind("<KeyRelease>", WidgetFactory.format_cpf)
        return cpf, bar_cpf
    
    @staticmethod
    def create_cnpj(frame : Frame) -> tuple[Entry, Frame]:
        """
        Cria um campo de entrada para CNPJ.

        :param frame: Frame onde o campo de entrada será criado.

        :return: Campo de entrada criado.
        """
        cnpj = Entry(frame, width=25, bg="#fff", fg="#000", border=0, font=("Microsoft Yahei UI Light", 11))
        bar_cnpj = Frame(frame, width=295, height=2, bg="#000")

        cnpj.insert(0, "CNPJ")

        cnpj.bind("<FocusIn>", lambda e: WidgetFactory.entry_on_enter(e, field="CNPJ"))
        cnpj.bind("<FocusOut>", lambda e: WidgetFactory.entry_on_leave(e, field="CNPJ"))
        cnpj.bind("<KeyRelease>", WidgetFactory.format_cnpj)
        return cnpj, bar_cnpj