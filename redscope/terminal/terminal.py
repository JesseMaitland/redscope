from logging import Logger
from redscope.database import models, db_connections
from redscope.project import project, logger_factory
from redscope import env, rambo_path
from rambo import provide_cmd_args


def get_terminal_logger(name: str) -> Logger:
    folders = project.Folders()
    folders.log_path.mkdir(exist_ok=True, parents=True)
    folders.log_file.touch(exist_ok=True)

    return logger_factory(folders.log_file, name)


@provide_cmd_args(rambo_path)
def _init_env(cmd_args):
    if env.load_custom_env(cmd_args.env_file):
        return True
    elif env.load_default_env():
        return True
    else:
        return False


@provide_cmd_args(rambo_path)
def _db_connection(cmd_args):
    if cmd_args.env_var:
        return db_connections.custom(cmd_args.env_var)
    else:
        return db_connections.default()


def init_redscope_env(func):
    def wrapper(*args, **kwargs):
        if _init_env():
            db_conn = _db_connection()
            return func(db_conn=db_conn, *args, **kwargs)
        else:
            print(f"unable to init redscope environment. Please provide a .env file in the cwd, or name of a custom file")
            exit()
    return wrapper
