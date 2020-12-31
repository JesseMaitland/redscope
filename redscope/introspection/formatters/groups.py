from typing import Tuple, List
from redgiant.redscope.introspection.permissions.group import Group
from redgiant.redscope.introspection.formatters.base_formatter import DDLFormatter


class GroupFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> List[Group]:
        return [Group(name=group[0], ddl=f"CREATE GROUP {group[0]};") for group in raw_ddl]
