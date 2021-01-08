from typing import List, Tuple, Type
from redscope.project.database.models import (  # noqa: F401
    DDL, Schema, View, Procedure, Function, Column, Constraint
)


def map_results(columns: List[str], results: List[Tuple], type_: str) -> List[Type[DDL]]:
    ddl = globals()[type_]
    return [ddl(**dict(zip(columns, result))) for result in results]
