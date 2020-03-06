from typing import Tuple, List
from redscope.features.schema_introspection.db_objects.user import User
from redscope.features.schema_introspection.formatters.base_formatter import DDLFormatter


class UserFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> List[User]:
        return [User(name=user[0]) for user in raw_ddl]
