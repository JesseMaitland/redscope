from logging import Logger
from redscope.config import RAMBO_CONFIG_PATH
from redscope.database import db_connections
from redscope.env.project_context import DirContext
from redscope.features.terminal.project_logging import logger_factory
from redscope import env
from rambo import provide_cmd_args


def get_terminal_logger(name: str, print_stream: bool = True) -> Logger:
    context = DirContext()
    path = context.get_dir('logs')
    path.mkdir(exist_ok=True, parents=True)
    log_file = path / "redscope.log"
    log_file.touch(exist_ok=True)
    return logger_factory(log_file, name, print_stream=print_stream)


@provide_cmd_args(RAMBO_CONFIG_PATH)
def _init_env(cmd_args, provide_db: bool):
    env.load_redscope_env(cmd_args.env_file)
    if provide_db:
        return db_connections.get_db_connection(cmd_args.env_var), cmd_args
    else:
        return None, cmd_args


def init_terminal_env(provide_db: bool, provide_cmd: bool):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                db_conn, cmd_args = _init_env(provide_db=provide_db)

                if db_conn and provide_cmd:
                    return func(db_conn=db_conn, cmd_args=cmd_args, *args, **kwargs)

                elif not db_conn and provide_cmd:
                    return func(cmd_args=cmd_args, *args, **kwargs)

                elif db_conn and not provide_cmd:
                    return func(db_conn=db_conn, *args, **kwargs)

                else:
                    return func(*args, **kwargs)
            except Exception:
                logger = get_terminal_logger(__name__, print_stream=False)
                logger.exception("redscope exception")
                print(f"an exception occurred while running redscope. Check log in /database/redscope.log")
                exit()
        return wrapper
    return decorator
