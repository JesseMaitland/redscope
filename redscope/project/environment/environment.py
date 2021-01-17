import os
import psycopg2
from pathlib import Path
from psycopg2.extensions import connection
from configparser import ConfigParser
from dotenv import load_dotenv
from redscope.project.environment import REDSCOPE_CONFIG_PATH


def get_redscope_config(config_path: Path = REDSCOPE_CONFIG_PATH) -> ConfigParser:
    config = ConfigParser()
    config.read(config_path)
    return config


def load_redscope_env(config: ConfigParser = None) -> None:
    if not config:
        config = get_redscope_config()
    try:
        load_dotenv(config['env']['file'])
    except KeyError:
        load_dotenv()


def get_redshift_connection(connection_name: str = None) -> connection:
    if connection_name:
        return psycopg2.connect(os.getenv(connection_name))
    else:
        config = get_redscope_config()
        return psycopg2.connect(os.getenv(config['redshift']['connection']))


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
