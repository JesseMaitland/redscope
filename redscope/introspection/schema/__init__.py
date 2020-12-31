from itertools import groupby
from typing import List, Dict
from redgiant.redscope.introspection.ddl import DDL


class PermissionsBox:

    def __init__(self,
                 users: Dict = None,
                 groups: Dict = None,
                 membership: Dict = None) -> None:

        self._users = {u.name: u for u in users} if users else {}
        self._groups = {g.name: g for g in groups} if groups else {}
        self._membership = {m.name: m for m in membership} if membership else {}

    @property
    def get(self) -> 'PermissionsBox':
        return self

    def ddl(self) -> List[DDL]:
        return [i for value in self.__dict__.values() for i in value.values()]

    def users(self) -> Dict[str, DDL]:
        return self._users

    def user(self, name: str) -> DDL:
        return self._users.get(name, DDL.empty())

    def groups(self) -> Dict[str, DDL]:
        return self._groups

    def group(self, name: str) -> DDL:
        return self._groups.get(name, DDL.empty())

    def memberships(self) -> Dict[str, DDL]:
        return self._membership

    def membership(self, name: str) -> DDL:
        return self._membership.get(name, DDL.empty())


class SchemaBox:

    def __init__(self,
                 tables: Dict = None,
                 views: Dict = None,
                 udfs: Dict = None,
                 procedures: Dict = None,
                 constraints: Dict = None,
                 ownership: Dict = None) -> None:
        self._tables = {t.name: t for t in tables} if tables else {}
        self._views = {v.name: v for v in views} if views else {}
        self._udfs = {u.name: u for u in udfs} if udfs else {}
        self._procedures = {p.name: p for p in procedures} if procedures else {}
        self._constraints = {c.name: c for c in constraints} if constraints else {}
        self._ownership = {o.name: o for o in ownership} if ownership else {}

    def ddl(self) -> List[DDL]:
        return [i for value in self.__dict__.values() for i in value.values()]

    def tables(self) -> Dict[str, DDL]:
        return self._tables

    def table(self, name: str) -> DDL:
        return self._tables.get(name, DDL.empty())

    def views(self) -> Dict[str, DDL]:
        return self._views

    def view(self, name: str) -> DDL:
        return self._views.get(name, DDL.empty())

    def udfs(self) -> Dict[str, DDL]:
        return self._udfs

    def udf(self, name: str) -> DDL:
        return self._udfs.get(name, DDL.empty())

    def procedures(self) -> Dict[str, DDL]:
        return self._procedures

    def procedure(self, name: str) -> DDL:
        return self._procedures.get(name, DDL.empty())

    def constraints(self) -> Dict[str, DDL]:
        return self._constraints

    def constraint(self, name: str) -> DDL:
        return self._constraints.get(name, DDL.empty())

    def ownerships(self) -> Dict[str, DDL]:
        return self._ownership

    def ownership(self, name: str) -> DDL:
        return self._ownership.get(name, DDL.empty())


class Schema(DDL):

    def __init__(self, name: str, ddl: str) -> None:
        super().__init__(name=name, schema=name, ddl=ddl)
        self._schema_box: SchemaBox = SchemaBox()

    @property
    def get(self) -> SchemaBox:
        return self._schema_box

    def file_name(self) -> str:
        return f"{self.name}.sql"

    def drop(self) -> str:
        return self.drop_if_exists()

    def drop_if_exists(self) -> str:
        return f"DROP SCHEMA IF EXISTS {self.schema};"

    def drop_cascade(self) -> str:
        return f"DROP SCHEMA IF EXISTS {self.schema} CASCADE;"

    def create_external(self, prefix: str) -> str:
        return f"CREATE EXTERNAL SCHEMA {prefix}_{self.schema};"

    def set_schema_box(self, schema_box: SchemaBox):
        self._schema_box = schema_box

    def items(self) -> List[DDL]:
        return self._schema_box.ddl()

    def map_constraints(self) -> None:
        for table in self._schema_box.tables().values():
            for constraint in self._schema_box.constraints().values():
                if constraint.table == table.name:
                    table.add_constraint(constraint)


class RedshiftSchema:

    schema_mapping_keys = ['tables', 'views', 'udfs', 'procedures', 'constraints', 'ownership']
    permission_mapping_keys = ['users', 'groups', 'membership']
    allowed_kwargs = ['schemas']

    def __init__(self, **kwargs):

        self._validate_kwargs(self.allowed_kwargs, kwargs)

        for kwarg in self.allowed_kwargs:
            setattr(self, f"_{kwarg}", kwargs.get(kwarg, {}))

        self._permissions = PermissionsBox()

    def schemas(self):
        return getattr(self, '_schemas')

    def schema(self, name: str) -> 'Schema':
        return self.schemas()[name]

    def permissions(self):
        return self._permissions

    @staticmethod
    def _validate_kwargs(allowed_kwargs: List[str], kwargs):
        for kwarg in kwargs.keys():
            if kwarg not in allowed_kwargs:
                raise ValueError(f"redshift schema got unexpected keyword {kwarg}")

    def map_schemas(self, **kwargs):
        self._validate_kwargs(self.schema_mapping_keys, kwargs)

        mapping = {}
        for name, ddls in kwargs.items():  # eg. tables:{table_name: ddl object}

            schema_grouping = {}
            ddls.sort(key=lambda x: x.schema)

            for schema, group in groupby(ddls, lambda x: x.schema):
                schema_grouping[schema] = list(group)

            mapping[name] = schema_grouping

        for schema_name, schema in self.schemas().items():
            schema_mapping = {}  # add the schema to the mapping

            for db_object_type, ddls in mapping.items():
                items = ddls.get(schema_name, None)

                if items:
                    schema_mapping[db_object_type] = items

            schema_box = SchemaBox(**schema_mapping)
            schema.set_schema_box(schema_box)
            schema.map_constraints()

    def map_permissions(self, **kwargs):
        self._validate_kwargs(self.permission_mapping_keys, kwargs)
        self._permissions = PermissionsBox(**kwargs)
