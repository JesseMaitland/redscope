from typing import Tuple, List
from redscope.features.schema_introspection.db_objects.group import Group
from redscope.features.schema_introspection.formatters.base_formatter import DDLFormatter


class GroupFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> List[Group]:
        return [Group(name=group[0]) for group in raw_ddl]
