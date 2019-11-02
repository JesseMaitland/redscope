from redscope.project import project
from unittest import TestCase
from pathlib import Path

ROOT_PATH = Path.cwd().absolute() / "database"
DDL_PATH = ROOT_PATH / "ddl"
MIGRATION_PATH = ROOT_PATH / "migrations"
LOGGING_PATH = ROOT_PATH / "logs"


class TestMigrationDirs(TestCase):

    def setUp(self) -> None:
        self.project_folders = project.Folders()

    def test_root_path(self):
        self.assertEqual(ROOT_PATH, self.project_folders.root)

    def test_ddl_path(self):
        self.assertEqual(DDL_PATH, self.project_folders.ddl)

    def test_migration_path(self):
        self.assertEqual(MIGRATION_PATH, self.project_folders.migrations_path)

    def test_logging_path(self):
        self.assertEqual(LOGGING_PATH, self.project_folders.log_path)


class TestMigrationManager(TestCase):

    def setUp(self) -> None:
        project_folders = project.Folders()
        self.file_manager = project.Manager(project_folders)

    def test_file_name(self):
        file_name = self.file_manager.file_name('foo')
        file_key, file_name = file_name.split('-')
        self.assertTrue(int, file_key.isdigit())
        self.assertTrue(file_name, str)

    def test_file_key(self):
        file_name = "12345678-foo"
        result = self.file_manager.migration_key(file_name)
        self.assertEqual(12345678, result)

    def test_file_key_and_name(self):
        file_name = "12345678-foo"
        file_key, file_name = self.file_manager.migration_key_and_name(file_name)
        self.assertEqual(12345678, file_key)
        self.assertEqual(file_name, 'foo')
