import sqlite3
import tkinter as tk
from tkinter import filedialog

DB_FILE: str = "testbase2.db"


# Classe Factory para criar instâncias do sistema
class MusicSystemFactory:
    @staticmethod
    def create_music_system() -> 'MusicSystemFacade':
        return MusicSystemFacade()


# Classe Facade para fornecer uma interface para o sistema
class MusicSystemFacade:
    def __init__(self):
        self.database: 'MusicDatabase' = MusicDatabase()
        self.certification_service: 'CertificationService' = CertificationService()

    def register_music(self, cod_artista: int, file_path: str) -> str:
        composicao: str = self._read_file(file_path)
        if not composicao:
            return "Erro ao ler o arquivo"

        is_unique: bool = self.database.check_uniqueness(composicao)
        if is_unique:
            certificate: str = self.certification_service.issue_certificate(cod_artista)
            return f"Música registrada com sucesso!\n{certificate}"
        else:
            return "Esta música já foi registrada anteriormente. Não exclusiva."

    def _read_file(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return None


# Classe para manipular o banco de dados
class MusicDatabase:
    def __init__(self):
        self.connection: 'sqlite3.Connection' = sqlite3.connect(DB_FILE)
        self.cursor: 'sqlite3.Cursor' = self.connection.cursor()
        self._create_table()

    def _create_table(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS obra (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL UNIQUE
            )
            """
        )
        self.connection.commit()

    def check_uniqueness(self, composicao: str) -> bool:
        self.cursor.execute("SELECT * FROM obra WHERE content = ?", (composicao,))
        return not bool(self.cursor.fetchone())

    def register_music(self, composicao: str) -> None:
        self.cursor.execute("INSERT INTO obra (content) VALUES (?)", (composicao,))
        self.connection.commit()


# Classe para emitir certificados
class CertificationService:
    def issue_certificate(self, cod_artista: int) -> str:
        # Lógica para emitir certificado (pode ser personalizada conforme necessário)
        return f"Certificado de propriedade intelectual emitido para o músico {cod_artista}"


# Interface Gráfica com Tkinter
class MusicRegistrationGUI:
    def __init__(self, master: tk.Tk):
        self.master: tk.Tk = master
        self.master.title("Registro de Música")
        self.file_path: str = ''  # Inicialização para evitar problemas de tipo
        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.master, text="Selecione o arquivo de música:").pack(pady=10)
        tk.Button(self.master, text="Selecionar Arquivo", command=self.select_file).pack(pady=10)
        tk.Button(self.master, text="Registrar Música", command=self.register_music).pack(pady=10)

    def select_file(self) -> None:
        file_path: str = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
        self.file_path: str = file_path
        tk.Label(self.master, text=f"Arquivo Selecionado: {file_path}").pack()

    def register_music(self) -> None:
        cod_artista: int = 1  # Suponha que o ID do musicista seja 1 (pode ser obtido de forma dinâmica)
        system: 'MusicSystemFacade' = MusicSystemFactory.create_music_system()
        result_message: str = system.register_music(cod_artista, self.file_path)
        tk.messagebox.showinfo("Resultado", result_message)


if __name__ == "__main__":
    # Criação da interface gráfica
    root: tk.Tk = tk.Tk()
    app: 'MusicRegistrationGUI' = MusicRegistrationGUI(root)
    root.mainloop()
