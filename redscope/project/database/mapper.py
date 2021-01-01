from typing import List, Tuple, Type
from redscope.project.database.models import (
    DDL, Schema, View, Procedure, Function, Column
)


def map_results(columns: List[str], results: List[Tuple], type_: str) -> List[Type[DDL]]:
    ddl = globals()[type_]
    return [ddl(**dict(zip(columns, result))) for result in results]
