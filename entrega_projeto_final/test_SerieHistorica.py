import unittest
from unittest.mock import Mock, patch
from SerieHistorica import QueryFactory, DatabaseSingleton, SearchRecordsCommand, DatabaseFacade, DatabaseConnectionError


class TestDatabaseFacade(unittest.TestCase):
    def test_error_handling_during_search(self):
        """Test error handling during database search operation."""
        db_singleton = Mock(spec=DatabaseSingleton)
        db_singleton.get_connection.side_effect = DatabaseConnectionError
        facade = DatabaseFacade(db_singleton)

        with self.assertRaises(DatabaseConnectionError):
            facade.search_records('code', '2023-01-01', '2023-12-31', Mock(), 'SELECT 1', ('param1',))

if __name__ == '__main__':
    unittest.main()


class TestSearchRecordsCommand(unittest.TestCase):
    def test_command_execution(self):
        """Test the execution of SearchRecordsCommand."""
        db_facade = Mock(spec=DatabaseFacade)
        command = SearchRecordsCommand(db_facade, 'code', '2023-01-01', '2023-12-31', Mock())
        command.execute('SELECT 1', ('param1',))

        db_facade.search_records.assert_called_once()

if __name__ == '__main__':
    unittest.main()

class TestDatabaseSingleton(unittest.TestCase):
    def test_singleton_instance(self):
        """Test that DatabaseSingleton always returns the same instance."""
        instance1 = DatabaseSingleton()
        instance2 = DatabaseSingleton()
        self.assertIs(instance1, instance2)

    def test_connection_established(self):
        """Test that a database connection is established."""
        instance = DatabaseSingleton()
        conn = instance.get_connection()
        self.assertIsNotNone(conn)

if __name__ == '__main__':
    unittest.main()

class TestQueryFactory(unittest.TestCase):
    def test_create_query_artist_deduction(self):
        """Test for create_query_artist_deduction with valid inputs."""
        sql, params = QueryFactory.create_query_artist_deduction('123', '2023-01-01', '2023-12-31', 'field_name', 'value')
        self.assertIn('SELECT', sql)
        self.assertEqual(len(params), 3)
        self.assertIn('2023-01-01', params)

# Add more test cases as needed

if __name__ == '__main__':
    unittest.main()