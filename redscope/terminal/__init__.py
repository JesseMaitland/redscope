from .terminal import init_redscope_env
from redscope.database import models
from redscope.project import project, logger_factory

logger = logger_factory(project.ProjectFolders().log_file, __name__)


@init_redscope_env
def init_db(db_conn):
    logger.info("initializing database")
    ddl = models.DDL()
    initiate_db = models.InitiateDb(ddl, db_conn)
    initiate_db.exe_create_schema()
    initiate_db.exe_create_migration_table()


def init_project():
    logger.info("creating redscope project")
    init_db()
    redscope_project = project.ProjectFolders()
    redscope_project.init_project_directories()
    logger.info("redscope project created successfully")
