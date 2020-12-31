from typing import Tuple, List
from redgiant.redscope.introspection.schema.ownership import Ownership
from redgiant.redscope.introspection.formatters.base_formatter import DDLFormatter


class OwnershipFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> List[Ownership]:
        return [Ownership(schema=ddl[0],
                          name=ddl[1],
                          owner=ddl[2],
                          signature=ddl[3],
                          db_obj_type=ddl[4])
                for ddl in raw_ddl]
