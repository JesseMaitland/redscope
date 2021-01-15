import os
import psycopg2
from psycopg2.extensions import connection
from configparser import ConfigParser
from dotenv import load_dotenv
from redscope.project.environment import REDSCOPE_CONFIG_PATH


def get_redscope_config() -> ConfigParser:
    config = ConfigParser()
    config.read(REDSCOPE_CONFIG_PATH)
    return config


def load_redscope_env(config: ConfigParser = None) -> None:
    if not config:
        config = get_redscope_config()
    try:
        load_dotenv(config['env']['file'])
    except KeyError:
        load_dotenv()


def get_redshift_connection() -> connection:
    config = get_redscope_config()
    var_name = config['redshift']['connection']
    connection_string = os.getenv(var_name)
    return psycopg2.connect(connection_string)


def init_redscope_env(provide_config: bool = False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            load_redscope_env()
            if provide_config:
                return func(config=get_redscope_config(), *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator
