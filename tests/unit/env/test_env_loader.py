import unittest
import os
from pathlib import Path
from redscope.terminal.tools.entry import load_redscope_env, env_path_valid


class TestRedscopeEnvLoader(unittest.TestCase):

    def test_valid_path(self):
        path = Path.cwd().absolute() / ".env"
        result = env_path_valid(path)
        self.assertEqual(result, True)

    def test_invalid_path(self):
        path = Path.cwd().absolute() / ".spam"
        self.assertRaises(FileNotFoundError, env_path_valid, path)

    def test_load_default_env(self):
        load_redscope_env()
        default_1 = os.getenv('DEFAULT_VAR_1')
        default_2 = os.getenv('DEFAULT_VAR_2')
        self.assertEqual('default_1', default_1)
        self.assertEqual('default_2', default_2)

    def test_load_custom_env(self):
        load_redscope_env("custom.env")
        custom_1 = os.getenv('CUSTOM_VAR_1')
        custom_2 = os.getenv('CUSTOM_VAR_2')
        self.assertEqual('custom_1', custom_1)
        self.assertEqual('custom_2', custom_2)
