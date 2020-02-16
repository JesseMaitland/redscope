import os
import psycopg2
from redscope.config import DEFAULT_DB_URL


def connection_exists(db_connection_string: str, connection_name: str = DEFAULT_DB_URL) -> bool:
    if not db_connection_string:
        raise EnvironmentError(f"no connection string found in .env for {connection_name}")
    return True


def get_db_connection(connection_name: str = '') -> psycopg2.connect:
    db_connection_string = os.getenv(connection_name) or os.getenv(DEFAULT_DB_URL)
    if connection_exists(db_connection_string, connection_name):
        return psycopg2.connect(db_connection_string)
