# flake8: noqa
import os
from pathlib import Path
from unittest import TestCase
from redscope.terminal.tools.entry import load_redscope_env, parse_redscope_config




class TestEnvLoaders(TestCase):

    def setUp(self) -> None:
        self.this_dir = Path(__file__).parent.relative_to(Path.cwd())
        self.config_path = self.this_dir / ".redscope"
        self.bad_config = self.this_dir.parent / ".redscope"
        self.env_path = self.this_dir / "test.env"
        self.bad_env = self.this_dir / "bad.env"

    def test_load_env(self):
        load_redscope_env(self.env_path.as_posix())
        default_url = os.getenv('')
