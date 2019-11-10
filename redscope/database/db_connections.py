import os
import psycopg2

DEFAULT_DB_URL = 'REDSCOPE_DB_URL'


def exists(db_connection_string: str, connection_name: str = DEFAULT_DB_URL) -> bool:
    if not db_connection_string:
        raise EnvironmentError(f"no connection string found in .env for {connection_name}")
    return True

# TODO: refactor these to single method which takes optional default parameter
def default() -> psycopg2.connect:
    db_connection_string = os.getenv(DEFAULT_DB_URL)
    if exists(db_connection_string):
        return psycopg2.connect(db_connection_string)


def custom(connection_name: str) -> psycopg2.connect:
    db_connection_string = os.getenv(connection_name)
    if exists(db_connection_string, connection_name):
        return psycopg2.connect(db_connection_string)
