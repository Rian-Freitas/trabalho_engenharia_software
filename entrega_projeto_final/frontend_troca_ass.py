import tkinter as tk
from tkinter import ttk, messagebox
from backend_troca_ass import conexaoFactory, FacadeDB

class LazyProxy:
    def __init__(self, classe_real, *args, **kwargs):
        self._classe_real = classe_real
        self.instancia_real = None
        self._args = args
        self._kwargs = kwargs

    def __getattr__(self, attr):
        if self.instancia_real is None:
            self.instancia_real = self._classe_real(*self._args, **self._kwargs)
        return getattr(self.instancia_real, attr)

# Classe para a aplicação principal
class TrocaAssociacaoApp:
    def __init__(self, root, info, database_facade):
        # Configurações iniciais da janela principal
        self.info = info
        self.root = root
        self.root.title("Solicitar Troca de Associação")

        # Label de título
        tk.Label(root, text="ECAD - Solicitar Troca de Associação", background='#fff', fg='#57a1f8', font=("Microsoft Yahei UI Light", 23, "bold")).place(x=400, y =0)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.configure(bg="white")

        # Atributos relacionados ao artista e à conexão com o banco de dados
        self.database_facade = database_facade
        
        # Label de boas-vindas
        label_boas_vindas = tk.Label(root, text="Bem vindo", fg="#000000", bg="#fff", font=("Microsoft Yahei UI Light", 17, "bold"))
        label_boas_vindas.place(x=625, y=60)

        # Criação dos widgets da interface gráfica
        self.cria_widgets()

    def cria_widgets(self):
        # Criação dos widgets, como Combobox e Botão
        ttk.Label(self.root, text="Selecione a nova associação:", background='#fff', font=("Microsoft Yahei UI Light", 17, "bold")).place(x=525, y=200)
        self.associacao_var = tk.StringVar()
        self.associacao_combobox = ttk.Combobox(self.root, textvariable=self.associacao_var, state='readonly')

        associacoes = self.obter_nomes_associacoes()
        self.associacao_combobox['values'] = associacoes

        self.associacao_combobox.place(x=625, y=250)

        tk.Button(self.root, text="Solicitar Troca", command=self.solicitar_troca, fg="#FF0000", bg="#fff", font=("Microsoft Yahei UI Light", 15, "bold")).place(x=625, y=600)

    def obter_nomes_associacoes(self):
        # Método para obter os nomes das associações disponíveis no banco de dados
        query = f"""
            SELECT nome_associacao 
            FROM associacao 
            WHERE cod_associacao != (
                SELECT associacao_cod_associacao 
                FROM artista 
                WHERE email_artista = '{self.info[0]}'
            )
        """
        resultado = self.database_facade.executa_query(query)
        associacoes = [row[0] for row in resultado]
        return associacoes

    def solicitar_troca(self):
        # Método para processar a solicitação de troca de associação
        nova_associacao = self.associacao_var.get()

        query_cod_associacao = f"""
            SELECT cod_associacao 
            FROM associacao 
            WHERE nome_associacao = '{nova_associacao}'
        """
        resultado = self.database_facade.executa_query(query_cod_associacao)
        novo_cod_associacao = resultado[0][0]

        query_atualizar_cod_associacao = f"""
            UPDATE artista 
            SET associacao_cod_associacao = {novo_cod_associacao} 
            WHERE email_artista = '{self.info[0]}'
        """
        self.database_facade.executa_update(query_atualizar_cod_associacao)

        messagebox.showinfo("Sucesso", "Atualização de associação realizada com sucesso!")

if __name__ == "__main__":   
    # Configuração inicial da aplicação
    email_artista = "artist1@email.com"
    factory_conexao = conexaoFactory('database.db')
    lazy_proxy = LazyProxy(FacadeDB, factory_conexao)

    root = tk.Tk()
    app = TrocaAssociacaoApp(root, email_artista, lazy_proxy)
    root.mainloop()
