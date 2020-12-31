from typing import Tuple, List, Dict
from itertools import groupby
from redgiant.redscope.introspection.permissions.usergroup import UserGroup
from redgiant.redscope.introspection.formatters.base_formatter import DDLFormatter


class MembershipFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> List[UserGroup]:
        user_groups = []
        grouping = self.perform_grouping(raw_ddl)
        template = self.template_env.get_template('groups.sql')

        for user, groups in grouping.items():
            ddl = template.render(user=user, groups=groups)
            user_group = UserGroup(name=user, ddl=ddl)
            user_groups.append(user_group)

        return user_groups

    @staticmethod
    def sort_key(row: Tuple[str]) -> str:
        return row[0]

    def perform_grouping(self, raw_ddl) -> Dict:
        sorted_ddl = sorted(raw_ddl, key=self.sort_key)
        groups = {}
        for key, group in groupby(sorted_ddl, key=self.sort_key):
            groups[key] = (list(group))
        return groups
