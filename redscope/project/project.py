from pathlib import Path
from .project_logging import logger_factory


class ProjectFolders:

    def __init__(self):
        self.root = Path.cwd() / "database"
        self.log_path = self.root / "logs"
        self.migrations_path = self.root / "migrations"
        self.ddl = self.root / "ddl"

        self.log_file = self.log_path / "redscope.log"

        self.logger = logger_factory(self.log_file, __name__)

    def init_project_directories(self):
        self.logger.info("creating redscope project directories")
        self.root.mkdir(exist_ok=True, parents=True)
        self.log_path.mkdir(exist_ok=True, parents=True)
        self.migrations_path.mkdir(exist_ok=True, parents=True)
        self.ddl.mkdir(exist_ok=True, parents=True)
        self.logger.info("project directories created successfully")
