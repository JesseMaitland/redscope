import os
import psycopg2
from typing import Tuple


def execute_query(connection_name: str, query: str, include_columns: bool = True, *params) -> Tuple:
    with psycopg2.connect(os.getenv(connection_name)) as connection:
        with connection.cursor() as cursor:
            if params:
                print(f"we run this {params}")
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()

            if include_columns:
                return [desc[0] for desc in cursor.description], result
            else:
                return result


def execute_statement(connection_name: str, query: str) -> None:
    with psycopg2.connect(os.getenv(connection_name)) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
