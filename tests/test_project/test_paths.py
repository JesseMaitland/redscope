from unittest import TestCase
from pathlib import Path

# paths to test
from redscope.project.environment.paths import (
    PROJECT_ROOT, SCHEMA_DIR, REDSCOPE_CONFIG_PATH
)


class TestProjectPaths(TestCase):
    """
    Tests all project paths and config file paths.
    """
    def setUp(self) -> None:
        self.root = Path.cwd() / "redshift" / "redscope"
        self.schema_dir = self.root / "schema"
        self.redscope_config = self.root / ".redscope"

    def test_project_root(self) -> None:
        self.assertEqual(PROJECT_ROOT, self.root)

    def test_schema_dir(self) -> None:
        self.assertEqual(SCHEMA_DIR, self.schema_dir)

    def test_redscope_config_path(self) -> None:
        self.assertEqual(REDSCOPE_CONFIG_PATH, self.redscope_config)
