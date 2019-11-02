from .terminal import init_redscope_env
from redscope.database import models
from redscope.project import project, logger_factory
from rambo import provide_cmd_args

logger = logger_factory(project.Folders().log_file, __name__)


@init_redscope_env
def init_db(db_conn):
    logger.info("creating database table and schema")
    ddl = models.DDL()
    initiate_db = models.InitiateDb(ddl, db_conn)
    initiate_db.exe_create_schema()
    initiate_db.exe_create_migration_table()
    logger.info("database tables created successfully")


def init_project():
    logger.info("creating redscope project")
    init_db()
    redscope_project = project.Folders()
    redscope_project.init_project_directories()
    logger.info("redscope project created successfully")


@provide_cmd_args()
def new_migration(cmd_args):

    if not cmd_args.name:
        logger.info("the --name parameter must be provided when creating new migration")
        exit()

    name = cmd_args.name.replace(' ', '-')
    folders = project.Folders()
    migration_manager = project.Manager(folders)
    migration_manager.create_new_migration(name)
