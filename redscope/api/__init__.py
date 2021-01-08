from typing import Union, Dict

from redscope.project.database import fetch_and_map_query_result
from redscope.project.database.models import Table, Schema, Constraint, Column, View, Procedure, Function


class RedshiftSchema:

    def __init__(self, connection_name: str = None) -> None:
        self.connection_name = connection_name
        self._schema: str = ''
        self._object_name: str = ''
        self._kind: str = ''

    def _set_kind(self, kind: str) -> None:
        if self._kind:
            raise ValueError("kind is already set. Please clear the schema before calling another query.")
        else:
            self._kind = kind

    def _clear_attributes(self) -> None:
        self._schema = ''
        self._object_name = ''
        self._kind = ''

    def schema(self, schema_name: str):
        self._schema = schema_name
        return self

    def table(self, table_name: str) -> 'RedshiftSchema':
        self._set_kind('table_ddl')
        self._object_name = table_name
        return self

    def view(self, view_name: str) -> 'RedshiftSchema':
        self._set_kind('view')
        self._object_name = view_name
        return self

    def views(self) -> 'RedshiftSchema':
        self._set_kind('views')
        return self

    def fetch(self) -> Union[Table, Schema, Constraint, Column, View, Procedure, Function, Dict]:

        if self._kind in ['view', 'table', 'function', 'procedure']:
            result = fetch_and_map_query_result(self.connection_name, self._kind, True, self._schema, self._object_name)
            self._clear_attributes()
            return result[0]

        elif self._kind in ['views', 'tables', 'functions', 'procedures']:
            result = fetch_and_map_query_result(self.connection_name, self._kind, True)
            self._clear_attributes()
            return {f"{d.schema}.{d.name}": d for d in result}
