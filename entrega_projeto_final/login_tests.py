import unittest
from login import *

class EmptyFieldsHandlerTDDTests(unittest.TestCase):
    def test_empty_fields(self):
        empty_fields_handler = EmptyFieldsHandler()
        self.assertEqual(empty_fields_handler._handle(['', '']), True)
        self.assertEqual(empty_fields_handler._handle(['', '123']), True)
        self.assertEqual(empty_fields_handler._handle(['123', '']), True)
        self.assertEqual(empty_fields_handler._handle(['123', '123', "", "", ""]), True)
        self.assertEqual(empty_fields_handler._handle(['123', '123', "", "", "123"]), True)
        self.assertEqual(empty_fields_handler._handle(['123', '123', "123", "", ""]), True)
        self.assertEqual(empty_fields_handler._handle(['123', '123', "", "123", ""]), True)
        self.assertEqual(empty_fields_handler._handle(['123', "123", "123", "123", "123"]), False)

    def test_user_already_exists(self):
        user_already_exists_handler = UserExistsHandler()
        self.assertEqual(user_already_exists_handler._handle(["Artist1", "artist1@email.com", "123.456.789-01", "artist1password", "Para artistas"]), True)
        self.assertEqual(user_already_exists_handler._handle(['Association1', 'assoc1@email.com', '12.345.678/0001-34', 'assoc1password', "Para associações"]), True)
        self.assertEqual(user_already_exists_handler._handle(["Owner1", "owner1@email.com", "123.456.789-01", "owner1password", "Para consumidores"]), True)
        self.assertEqual(user_already_exists_handler._handle(["Artist3", "artist3@email.com", "113.456.789-01", "artist1password", "Para artistas"]), False)
        self.assertEqual(user_already_exists_handler._handle(['Association3', 'assoc3@email.com', '12.340.678/0001-34', 'assoc1password', "Para associações"]), False)
        self.assertEqual(user_already_exists_handler._handle(["Owner3", "owner3@email.com", "123.456.619-01", "owner1password", "Para consumidores"]), False)

if __name__ == '__main__':
    unittest.main()