from redscope.project import project
from unittest import TestCase
from pathlib import Path

ROOT_PATH = Path.cwd().absolute() / "database"
DDL_PATH = ROOT_PATH / "ddl"
MIGRATION_PATH = ROOT_PATH / "migrations"
LOGGING_PATH = ROOT_PATH / "logs"


class TestMigrationDirs(TestCase):

    def setUp(self) -> None:
        self.project_folders = project.Folders('database')

    def test_root_path(self):
        self.assertEqual(ROOT_PATH, self.project_folders.root)

    def test_ddl_path(self):
        self.assertEqual(DDL_PATH, self.project_folders.ddl_path)

    def test_migration_path(self):
        self.assertEqual(MIGRATION_PATH, self.project_folders.migrations_path)

    def test_logging_path(self):
        self.assertEqual(LOGGING_PATH, self.project_folders.log_path)


class TestProjectFunctions(TestCase):

    def test_file_name(self):
        file_name = project.create_file_name('foo')
        file_key, file_name = file_name.split('-')
        self.assertTrue(int, file_key.isdigit())
        self.assertTrue(file_name, str)

    def test_file_key(self):
        file_path = Path.cwd() / "12345678-foo"
        result = project.parse_file_key(file_path)
        self.assertEqual(12345678, result)

    def test_file_key_and_name(self):
        file_path = Path.cwd() / "12345678-foo"
        file_key, file_name = project.parse_file_key_and_name(file_path)
        self.assertEqual(12345678, file_key)
        self.assertEqual('foo', file_name)

    def test_get_file_name(self):
        file_path = Path.cwd() / "1234-spam"
        name = project.parse_file_name(file_path)
        self.assertEqual('spam', name)
