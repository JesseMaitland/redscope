from pathlib import Path
from typing import Dict


class DirContext:

    def __init__(self):

        root_name = 'database'
        main_dir_names = ['migrations', 'schemas', 'permissions', 'logs']

        self.root_path = Path.cwd().absolute() / root_name
        self._paths: Dict[str: Path] = {}

        for dir_name in main_dir_names:
            self._paths[dir_name] = self.root_path / dir_name

    def get_dir(self, name: str):
        return self._paths[name]

    def init_dirs(self):

        self.root_path.mkdir(parents=True, exist_ok=True)

        for path in self._paths.values():
            path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_sql_file_name(name: str) -> str:
        return f"{name}.sql"
