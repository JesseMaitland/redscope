from redscope.database import models, db_connections
from redscope import env
from rambo import provide_cmd_args


@provide_cmd_args()
def _init_env(cmd_args):
    if env.load_custom_env(cmd_args.env_file):
        return True
    elif env.load_default_env():
        return True
    else:
        return False


@provide_cmd_args()
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
