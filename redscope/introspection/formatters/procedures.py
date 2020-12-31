from typing import Tuple, List
from redgiant.redscope.introspection.schema.procedure import Procedure
from redgiant.redscope.introspection.formatters.base_formatter import DDLFormatter


class ProcedureFormatter(DDLFormatter):

    def __init__(self):
        super().__init__()

    def format(self, raw_ddl: Tuple[str]) -> List[Procedure]:
        procedures = []
        for ddl in raw_ddl:
            schema, name, content = ddl
            procedure = Procedure(schema=schema, name=name, ddl=content)
            procedures.append(procedure)
        return procedures
