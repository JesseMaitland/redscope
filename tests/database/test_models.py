from unittest.mock import MagicMock
from redscope.database import models
from unittest import TestCase

CREATE_SCHEMA = "CREATE SCHEMA IF NOT EXISTS redscope;\n"

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS redscope.migrations
(
    key        BIGINT PRIMARY KEY NOT NULL,
    name       VARCHAR(30)        NOT NULL,
    sql        VARCHAR(10000)     NULL,
    created_at TIMESTAMP   DEFAULT CURRENT_DATE,
    created_by VARCHAR(50) DEFAULT CURRENT_USER
);
"""


class TestDDL(TestCase):

    def setUp(self) -> None:
        self.ddl = models.DDL()

    def test_create_schema(self):
        self.assertEqual(CREATE_SCHEMA, self.ddl.create_schema)

    def test_create_table(self):
        self.assertEqual(CREATE_TABLE, self.ddl.create_migration_table)


# TODO: add tests to throw exceptions
class TestInitiateDb(TestCase):

    def setUp(self) -> None:
        self.mock_cursor = MagicMock()
        self.mock_db_conn = MagicMock()
        self.mock_db_conn.cursor.return_value = self.mock_cursor
        self.initiate_db = models.InitiateDb(models.DDL(), self.mock_db_conn)

    def test_exec_create_schema(self):
        self.initiate_db.exe_create_schema()
        self.mock_cursor.execute.assert_called_once_with(CREATE_SCHEMA)
        self.mock_db_conn.commit.assert_called()

    def test_exec_create_migration_table(self):
        self.initiate_db.exe_create_migration_table()
        self.mock_cursor.execute.assert_called_once_with(CREATE_TABLE)
        self.mock_db_conn.commit.assert_called()
