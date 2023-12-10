import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox

# Constante com o nome do banco de dados
DB_FILE: str = "testbase2.db"


# Classe Factory para criar instâncias do sistema
class MusicSystemFactory:
    """Factory para criar instâncias do sistema de música."""
    @staticmethod
    def create_music_system() -> 'MusicSystemFacade':
        """Cria uma instância de MusicSystemFacade."""
        return MusicSystemFacade()


# Classe Facade para fornecer uma interface simplificada para o sistema
class MusicSystemFacade:
    """Fachada para interagir com o sistema de música."""
    def __init__(self):
        self.database: 'MusicDatabase' = MusicDatabase()
        self.certification_service: 'CertificationService' = CertificationService()

    def register_music(self, cod_artista: int, file_path: str) -> str:
        """Registra uma nova música e emite um certificado se única."""
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
        """Lê o conteúdo de um arquivo."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return None


# Classe para manipular o banco de dados
class MusicDatabase:
    """Classe para interagir com o banco de dados de músicas."""
    def __init__(self):
        self.connection: 'sqlite3.Connection' = sqlite3.connect(DB_FILE)
        self.cursor: 'sqlite3.Cursor' = self.connection.cursor()
        self._create_table()

    def _create_table(self) -> None:
        """Cria a tabela 'obra' no banco de dados se não existir."""
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
        """Verifica se uma composição já existe no banco de dados."""
        self.cursor.execute("SELECT * FROM obra WHERE content = ?", (composicao,))
        return not bool(self.cursor.fetchone())

    def register_music(self, composicao: str) -> None:
        """Registra uma nova composição no banco de dados."""
        self.cursor.execute("INSERT INTO obra (content) VALUES (?)", (composicao,))
        self.connection.commit()


# Classe para emitir certificados
class CertificationService:
    """Serviço para emitir certificados de propriedade intelectual."""
    def issue_certificate(self, cod_artista: int) -> str:
        """Emite um certificado para um artista."""
        # Lógica para emitir certificado (pode ser personalizada conforme necessário)
        return f"Certificado de propriedade intelectual emitido para o músico {cod_artista}"


# Interface Gráfica com Tkinter
class MusicRegistrationGUI:
    """Interface gráfica para o registro de músicas."""
    def __init__(self, master: tk.Tk):
        self.master: tk.Tk = master
        self.master.title("Registro de Música")
        self.file_path: str = ''  # Inicialização para evitar problemas de tipo
        self.create_widgets()

    def create_widgets(self) -> None:
        """Cria os widgets da interface gráfica."""
        tk.Label(self.master, text="Selecione o arquivo de música:").pack(pady=10)
        tk.Button(self.master, text="Selecionar Arquivo", command=self.select_file).pack(pady=10)
        tk.Button(self.master, text="Registrar Música", command=self.register_music).pack(pady=10)

    def select_file(self) -> None:
        """Abre uma caixa de diálogo para selecionar um arquivo."""
        file_path: str = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
        self.file_path: str = file_path
        tk.Label(self.master, text=f"Arquivo Selecionado: {file_path}").pack()

    def register_music(self) -> None:
        """Registra uma música."""
        cod_artista: int = 1  # Suponha que o ID do musicista seja 1 (pode ser obtido de forma dinâmica)
        system: 'MusicSystemFacade' = MusicSystemFactory.create_music_system()
        result_message: str = system.register_music(cod_artista, self.file_path)
        messagebox.showinfo("Resultado", result_message)


if __name__ == "__main__":
    # Criação da interface gráfica
    root: tk.Tk = tk.Tk()
    app: 'MusicRegistrationGUI' = MusicRegistrationGUI(root)
    root.mainloop()
