from logging import Logger
from redscope.config import RAMBO_CONFIG_PATH
from redscope.database import db_connections
from redscope.project import Folders, logger_factory
from redscope import env
from rambo import provide_cmd_args


def get_terminal_logger(name: str, print_stream: bool = True) -> Logger:
    folders = Folders("database")
    folders.log_path.mkdir(exist_ok=True, parents=True)
    folders.log_file.touch(exist_ok=True)
    return logger_factory(folders.log_file, name, print_stream=print_stream)


@provide_cmd_args(RAMBO_CONFIG_PATH)
def _init_env(cmd_args):
    env.load_redscope_env(cmd_args.env_file)
    return db_connections.get_db_connection(cmd_args.env_var)


def init_terminal_env(func):
    def wrapper(*args, **kwargs):
        try:
            db_conn = _init_env()
            return func(db_conn=db_conn, *args, **kwargs)
        except Exception:
            logger = get_terminal_logger(__name__, print_stream=False)
            logger.exception("redscope exception")
            print(f"an exception occurred while running redscope. Check log in /database/redscope.log")
            exit()
    return wrapper
