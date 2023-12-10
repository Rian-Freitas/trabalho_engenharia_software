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

class TrocaAssociacaoApp:
    def __init__(self, root, usuario_logado, database_facade):
        self.root = root
        self.root.title("Solicitar Troca de Associação")

        self.usuario_logado = usuario_logado
        self.database_facade = database_facade

        self.cria_widgets()

    def cria_widgets(self):
        ttk.Label(self.root, text="Selecione a nova associação:").grid(row=0, column=0, padx=10, pady=10)

        self.associacao_var = tk.StringVar()
        self.associacao_combobox = ttk.Combobox(self.root, textvariable=self.associacao_var, state='readonly')

        associacoes = self.obter_nomes_associacoes()
        self.associacao_combobox['values'] = associacoes

        self.associacao_combobox.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(self.root, text="Solicitar Troca", command=self.solicitar_troca).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def obter_nomes_associacoes(self):
        query = f"""
            SELECT nome_associacao 
            FROM associacao 
            WHERE cod_associacao != (
                SELECT associacao_cod_associacao 
                FROM artista 
                WHERE email_artista = '{self.usuario_logado}'
            )
        """
        resultado = self.database_facade.executa_query(query)
        associacoes = [row[0] for row in resultado]
        return associacoes

    def solicitar_troca(self):
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
            WHERE email_artista = '{self.usuario_logado}'
        """
        self.database_facade.executa_update(query_atualizar_cod_associacao)

        messagebox.showinfo("Sucesso", "Atualização de associação realizada com sucesso!")

if __name__ == "__main__":
    usuario_logado = "artist1@email.com"
    factory_conexao = conexaoFactory('testbase2.db')
    lazy_proxy = LazyProxy(FacadeDB, factory_conexao)

    root = tk.Tk()
    app = TrocaAssociacaoApp(root, usuario_logado, lazy_proxy)
    root.mainloop()
