from typing import Tuple, List
from redgiant.redscope.introspection.permissions.user import User
from redgiant.redscope.introspection.formatters.base_formatter import DDLFormatter


class UserFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> List[User]:
        return [User(name=user[0], ddl=f'CREATE USER {user[0]}') for user in raw_ddl]
