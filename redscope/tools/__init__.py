import psycopg2
from redgiant.terminal.config import RedGiantConfig


def get_redscope_connection() -> psycopg2.connect:
    config = RedGiantConfig()
    return config.get_db_connection('redshift')
