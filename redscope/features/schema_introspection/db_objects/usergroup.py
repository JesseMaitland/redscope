from typing import List
from redscope.features.schema_introspection.db_objects.ddl import DDL


class UserGroup(DDL):

    def __init__(self, name: str, groups: List[str]):
        super().__init__(name)
        self.groups = groups

    @property
    def file_name(self) -> str:
        return f"{self.name}_groups.sql"

    @property
    def create(self) -> str:
        add_groups = [f"ALTER GROUP {group} ADD USER {self.name};" for group in self.groups]
        return '\n'.join(add_groups)

    @property
    def create_if_not_exist(self) -> str:
        return self.create

    @property
    def drop(self) -> str:
        remove_groups = [f"ALTER GROUP {group} DROP USER {self.name};" for group in self.groups]
        return '\n'.join(remove_groups)

    @property
    def drop_if_exist(self) -> str:
        return self.drop
