import unittest
import os
from pathlib import Path
from redscope import env


class TestRedscopeEnvLoader(unittest.TestCase):

    def test_valid_path(self):
        path = Path.cwd().absolute() / ".env"
        result = env.path_valid(path)
        self.assertEqual(result, True)

    def test_invalid_path(self):
        path = Path.cwd().absolute() / ".spam"
        self.assertRaises(FileNotFoundError, env.path_valid, path)

    def test_load_default_env(self):
        result = env.load_default_env()
        default_1 = os.getenv('DEFAULT_VAR_1')
        default_2 = os.getenv('DEFAULT_VAR_2')
        self.assertEqual('default_1', default_1)
        self.assertEqual('default_2', default_2)
        self.assertEqual(True, result)

    def test_load_custom_env(self):
        result = env.load_custom_env("custom.env")
        custom_1 = os.getenv('CUSTOM_VAR_1')
        custom_2 = os.getenv('CUSTOM_VAR_2')
        self.assertEqual('custom_1', custom_1)
        self.assertEqual('custom_2', custom_2)
        self.assertEqual(True, result)
