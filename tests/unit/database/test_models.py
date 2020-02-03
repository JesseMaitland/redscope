from unittest.mock import MagicMock, patch
from redscope.database import models
from unittest import TestCase
from pathlib import Path

CREATE_SCHEMA = "CREATE SCHEMA IF NOT EXISTS redscope;\n"

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS redscope.migrations
(
    key        BIGINT PRIMARY KEY NOT NULL,
    name       VARCHAR(30)        NOT NULL,
    path       VARCHAR(500)       NOT NULL,
    created_at TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) DEFAULT CURRENT_USER
);
"""

MIGRATION_INSERT = """INSERT INTO redscope.migrations(key, name, path) VALUES (%s, %s, %s);
"""

MIGRATION_SELECT = """SELECT key, name, path FROM redscope.migrations ORDER BY key;
"""

MIGRATION_DELETE = """DELETE FROM redscope.migrations WHERE key = %s
"""

MIGRATION_SELECT_LAST = """SELECT key, name, path FROM redscope.migrations ORDER BY key DESC LIMIT 1;
"""


class TestDDL(TestCase):

    def setUp(self) -> None:
        self.ddl = models.MigrationDDL()

    def test_create_schema(self):
        self.assertEqual(CREATE_SCHEMA, self.ddl.create_schema)

    def test_create_table(self):
        self.assertEqual(CREATE_TABLE, self.ddl.create_migration_table)


class TestDML(TestCase):

    def setUp(self) -> None:
        self.ddl = models.DML()

    def test_select(self):
        self.assertEqual(MIGRATION_SELECT, self.ddl.select)

    def test_delete(self):
        self.assertEqual(MIGRATION_DELETE, self.ddl.delete)

    def test_insert(self):
        self.assertEqual(MIGRATION_INSERT, self.ddl.insert)

    def test_select_last(self):
        self.assertEqual(MIGRATION_SELECT_LAST, self.ddl.select_last)


class TestMigration(TestCase):

    def setUp(self) -> None:
        self.mock_db_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_db_connection.cursor.return_value = self.mock_cursor
        self.migration = models.Migration(1, 'foo', Path.cwd())

    def test_select(self):
        self.migration.select_all(self.mock_db_connection)
        self.mock_cursor.execute.assert_called_once_with(MIGRATION_SELECT)

    def test_insert(self):
        self.migration.insert(self.mock_db_connection)
        self.mock_cursor.execute.assert_called_once_with(MIGRATION_INSERT, [1, 'foo', '.'])

    def test_delete(self):
        self.migration.delete(self.mock_db_connection)
        self.mock_cursor.execute.assert_called_once_with(MIGRATION_DELETE, [1])

    @patch('redscope.database.models.Path')  # needed as workaround for pathlib exception
    def test_select_last(self, mock_path):
        self.migration.select_last(self.mock_db_connection)
        self.mock_cursor.execute.assert_called_once_with(MIGRATION_SELECT_LAST)


# TODO: add tests to throw exceptions
class TestInitiateDb(TestCase):

    def setUp(self) -> None:
        self.mock_cursor = MagicMock()
        self.mock_db_conn = MagicMock()
        self.mock_db_conn.cursor.return_value = self.mock_cursor
        self.initiate_db = models.InitiateDb(models.MigrationDDL(), self.mock_db_conn)

    def test_exec_create_schema(self):
        self.initiate_db.exe_create_schema()
        self.mock_cursor.execute.assert_called_once_with(CREATE_SCHEMA)
        self.mock_db_conn.commit.assert_called()

    def test_exec_create_migration_table(self):
        self.initiate_db.exe_create_migration_table()
        self.mock_cursor.execute.assert_called_once_with(CREATE_TABLE)
        self.mock_db_conn.commit.assert_called()
