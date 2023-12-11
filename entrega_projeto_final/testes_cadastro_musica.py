import unittest
from unittest.mock import MagicMock, patch
from cadastro_musica import MusicSystemInteraction, DatabaseInteraction


class TestMusicSystemInteraction(unittest.TestCase):
    def setUp(self):
        self.music_system = MusicSystemInteraction()

    @patch('cadastro_musica.CertificationService')
    @patch('cadastro_musica.DatabaseInteraction')
    def test_register_music_unique(self, mock_database, mock_certification_service):
        # Configuração de mocks
        mock_database_instance = mock_database.return_value
        mock_certification_service_instance = mock_certification_service.return_value

        # simulação do comportamento das dependências
        mock_database_instance.check_uniqueness.return_value = True
        mock_certification_service_instance.issue_certificate.return_value = "Certificate123"

        # Teste do processo de registro
        result = self.music_system.register_music(1, "path/to/music.txt")

        # Asserts
        self.assertEqual(result, "Música registrada com sucesso!\nCertificate123")
        mock_database_instance.check_uniqueness.assert_called_once_with("content_of_the_file")
        mock_certification_service_instance.issue_certificate.assert_called_once_with(1)

    @patch('cadastro_musica.DatabaseInteraction')
    def test_register_music_not_unique(self, mock_database):
        # Configuração de mocks
        mock_database_instance = mock_database.return_value

        # Simulação do comportamento das dependências
        mock_database_instance.check_uniqueness.return_value = False

        # Teste do processo de registro para uma música não única
        result = self.music_system.register_music(1, "path/to/music.txt")

        # Asserts
        self.assertEqual(result, "Esta música já foi registrada anteriormente. Não exclusiva")
        mock_database_instance.check_uniqueness.assert_called_once_with("content_of_the_file")

    def test_read_file(self):
        # Mock da função open
        with patch('builtins.open', create=True) as mock_open:
            mock_file = MagicMock()
            mock_file.read.return_value = "content_of_the_file"
            mock_open.return_value = mock_file

            # Teste do método read_file
            result = self.music_system._read_file("path/to/music.txt")

            # Asserts
            self.assertEqual(result, "content_of_the_file")
            mock_open.assert_called_once_with("path/to/music.txt", "r", encoding="utf-8")


class TestDatabaseInteraction(unittest.TestCase):
    def setUp(self):
        self.database = DatabaseInteraction()

    def test_check_uniqueness_unique(self):
        # Teste do método read_file
        self.database.cursor.execute = MagicMock()
        self.database.cursor.fetchone.return_value = None

        # Teste do método check_uniqueness para uma composição única
        result = self.database.check_uniqueness("unique_content")

        # Asserts
        self.assertTrue(result)
        self.database.cursor.execute.assert_called_once_with("SELECT * FROM obra WHERE content = ?", ("unique_content",))

    def test_check_uniqueness_not_unique(self):
        # Mock do método execute
        self.database.cursor.execute = MagicMock()
        self.database.cursor.fetchone.return_value = ("existing_content",)

        # Teste do método check_uniqueness para uma composição não única
        result = self.database.check_uniqueness("existing_content")

        # Asserts
        self.assertFalse(result)
        self.database.cursor.execute.assert_called_once_with("SELECT * FROM obra WHERE content = ?", ("existing_content",))

    def test_register_music(self):
        # Mock do método execute
        self.database.cursor.execute = MagicMock()

        # Teste do método register_music
        self.database.register_music("new_content")

        # Asserts
        self.database.cursor.execute.assert_called_once_with("INSERT INTO obra (content) VALUES (?)", ("new_content",))


if __name__ == '__main__':
    unittest.main()
