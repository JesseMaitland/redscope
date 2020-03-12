from typing import Tuple, List, Dict
from itertools import groupby
from redscope.features.schema_introspection.db_objects.usergroup import UserGroup
from redscope.features.schema_introspection.formatters.base_formatter import DDLFormatter


class UsergroupFormatter(DDLFormatter):

    def __init__(self, raw_ddl: Tuple[str] = None):
        self.raw_ddl = raw_ddl or ()

    def format(self, raw_ddl: Tuple[str]) -> List[UserGroup]:
        self.raw_ddl = raw_ddl
        grouping = self.perform_grouping()
        grouping = {user: [group[1] for group in groups] for user, groups in grouping.items()}
        return [UserGroup(name=user, groups=groups) for user, groups in grouping.items()]

    @staticmethod
    def sort_key(row: Tuple[str]) -> str:
        return row[0]

    def perform_grouping(self) -> Dict:
        sorted_ddl = sorted(self.raw_ddl, key=self.sort_key)
        groups = {}
        for key, group in groupby(sorted_ddl, key=self.sort_key):
            groups[key] = (list(group))
        return groups
