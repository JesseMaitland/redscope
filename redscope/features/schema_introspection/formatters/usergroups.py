from typing import Tuple, List
from redscope.features.schema_introspection.db_objects.usergroup import UserGroup
from redscope.features.schema_introspection.formatters.base_formatter import DDLFormatter


class UsergroupFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> List[UserGroup]:
        return print(raw_ddl)
