from typing import List
from redscope.features.schema_introspection.db_objects.ddl import DDL
from redscope.features.schema_introspection.db_objects.schema import Schema
from redscope.features.schema_introspection.db_objects.group import Group
from redscope.features.schema_introspection.db_objects.view import View
from redscope.features.schema_introspection.db_objects.table import Table
from redscope.features.schema_introspection.db_objects.user import User
from redscope.features.schema_introspection.db_objects.constraint import Constraint


class DbCatalog:

    def __init__(self,
                 schemas: List[Schema] = None,
                 groups: List[Group] = None,
                 views: List[View] = None,
                 tables: List[Table] = None,
                 users: List[User] = None,
                 constraints: List[Constraint] = None):

        self._schemas = schemas or {}
        self._groups = groups or {}
        self._views = views or {}
        self._tables = tables or {}
        self._users = users or {}
        self._constraints = constraints or {}

        self._schemas = {schema.name: schema for schema in self._schemas}
        self._groups = {group.name: group for group in self._groups}
        self._views = {view.name: view for view in self._views}
        self._tables = {table.full_name: table for table in self._tables}
        self._users = {user.name: user for user in self._users}
        self._constraints = {constraint.name: constraint for constraint in self._constraints}

    @property
    def schemas(self) -> List[Schema]:
        return [schema for schema in self._schemas.values()]

    @property
    def groups(self) -> List[Schema]:
        return [group for group in self._groups.values()]

    @property
    def views(self) -> List[View]:
        return [view for view in self._views.values()]

    @property
    def tables(self) -> List[Table]:
        return [table for table in self._tables.values()]

    @property
    def users(self) -> List[User]:
        return [user for user in self._users.values()]

    @property
    def constraints(self) -> List[Constraint]:
        return [constraint for constraint in self._constraints.values()]

    def get_db_objects(self, db_obj_type: str) -> List[DDL]:
        ddl_objs = getattr(self, f"_{db_obj_type}")
        return [ddl for ddl in ddl_objs.values()]

    def get_schema(self, name: str) -> Schema:
        return self._schemas[name]

    def get_group(self, name: str) -> Group:
        return self._groups[name]

    def get_view(self, name: str) -> View:
        return self._views[name]

    def get_table(self, name: str) -> Table:
        return self._tables[name]

    def get_user(self, name: str) -> User:
        return self._users[name]

    def get_constraint(self, name: str) -> Constraint:
        return self._constraints[name]
