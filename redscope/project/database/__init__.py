from typing import List, Any
from redscope.project.helpers import format_model_name
from .executor import execute_query
from .mapper import map_results
from .queries import SqlManager


def fetch_and_map_query_result(connection_name: str, query_name: str, *params) -> List[Any]:
    sql_manager = SqlManager()
    return map_results(
        *execute_query(
            connection_name,
            sql_manager.get_query(query_name),
            *params
        ),
        format_model_name(query_name)
    )
