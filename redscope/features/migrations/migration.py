from pathlib import Path
from redscope.database.models import MigrationQueries


class Migration(MigrationQueries):

    def __init__(self, file_path: Path, up: str = None, down: str = None):
        super().__init__()
        self._file_path = file_path
        self._up = up or ''
        self._down = down or ''

    @property
    def up(self) -> str:
        return self._up

    @property
    def down(self) -> str:
        return self._down

    @property
    def path(self) -> Path:
        return self._file_path

    @property
    def full_name(self) -> str:
        return self._file_path.name.split('.')[0]

    @property
    def file_name(self) -> str:
        return self._file_path.name

    @property
    def key(self) -> int:
        return int(self.full_name.split('-')[0])

    @property
    def name(self) -> str:
        return self.full_name.split('-')[-1]
