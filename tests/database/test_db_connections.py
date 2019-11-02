from unittest.mock import MagicMock, patch
from unittest import TestCase
from redscope.database import db_connections
from redscope import env


class TestDbConnections(TestCase):

    def test_default_url(self):
        self.assertEqual('REDSCOPE_DB_URL', db_connections.DEFAULT_DB_URL)

    @patch('redscope.database.db_connections.psycopg2.connect')
    def test_connect(self, patched_connect):
        db_connections.exists = MagicMock()
        mock_connection = db_connections.default()
        patched_connect.assert_called()

    @patch('redscope.database.db_connections.psycopg2.connect')
    def test_default_connect(self, patched_connect):
        db_connections.exists = MagicMock()
        env.load_default_env()
        mock_connection = db_connections.default()
        patched_connect.assert_called_once_with('default_connection_string')

    @patch('redscope.database.db_connections.psycopg2.connect')
    def test_custom_connect(self, patched_connect):
        db_connections.exists = MagicMock()
        env.load_default_env()
        mock_connection = db_connections.custom('DEFAULT_VAR_1')
        patched_connect.assert_called_once_with('default_1')
