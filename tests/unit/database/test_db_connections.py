from redscope.config import DEFAULT_DB_URL
from unittest.mock import MagicMock, patch
from unittest import TestCase
from redscope.database import db_connections
from redscope.env import load_redscope_env


class TestDbConnections(TestCase):

    def test_default_url(self):
        self.assertEqual('REDSCOPE_DB_URL', DEFAULT_DB_URL)

    @patch('redscope.database.db_connections.psycopg2.connect')
    def test_connect(self, patched_connect):
        db_connections.connection_exists = MagicMock()
        mock_connection = db_connections.get_db_connection()  # noqa: F841
        patched_connect.assert_called()

    @patch('redscope.database.db_connections.psycopg2.connect')
    def test_default_connect(self, patched_connect):
        db_connections.exists = MagicMock()
        load_redscope_env()
        mock_connection = db_connections.get_db_connection()  # noqa: F841
        patched_connect.assert_called_once_with('default_connection_string')

    @patch('redscope.database.db_connections.psycopg2.connect')
    def test_custom_connect(self, patched_connect):
        db_connections.exists = MagicMock()
        load_redscope_env()
        mock_connection = db_connections.get_db_connection('DEFAULT_VAR_1')   # noqa: F841
        patched_connect.assert_called_once_with('default_1')
