from redscope.config import DEFAULT_DB_URL
from unittest.mock import patch
from unittest import TestCase
from redscope.terminal.tools.entry import get_db_connection
from redscope.terminal.tools.entry import load_redscope_env


class TestDbConnections(TestCase):

    def test_default_url(self):
        self.assertEqual('REDSCOPE_DB_URL', DEFAULT_DB_URL)

    @patch('redscope.terminal.tools.entry.db_connection_exists')
    @patch('redscope.terminal.tools.entry.psycopg2.connect')
    def test_connect(self, patched_connect, patched_connection_exists):
        load_redscope_env()
        mock_connection = get_db_connection()  # noqa: F841
        patched_connect.assert_called()
        patched_connection_exists.assert_called()

    @patch('redscope.terminal.tools.entry.psycopg2.connect')
    def test_default_connect(self, patched_connect):
        load_redscope_env()
        mock_connection = get_db_connection()  # noqa: F841
        patched_connect.assert_called_once_with('default_connection_string')

    @patch('redscope.terminal.tools.entry.psycopg2.connect')
    def test_custom_connect(self, patched_connect):
        load_redscope_env()
        mock_connection = get_db_connection('DEFAULT_VAR_1')   # noqa: F841
        patched_connect.assert_called_once_with('default_1')
