from typing import List
from redscope.features.schema_introspection.db_objects.schema import Schema
from redscope.features.schema_introspection.db_objects.group import Group


class DbCatalog:

    def __init__(self, schemas: List[Schema] = None, groups: List[Group] = None):

        self._schemas = []
        self._groups = []

        self._schemas = {schema.name: schema for schema in schemas}
        self._groups = {group.name: group for group in groups}

    @property
    def schemas(self) -> List[Schema]:
        return [schema for schema in self._schemas.values()]

    @property
    def groups(self) -> List[Schema]:
        return [group for group in self._groups.values()]

    def get_schema(self, name: str) -> Schema:
        return self._schemas[name]

    def get_group(self, name: str) -> Group:
        return self._groups[name]
