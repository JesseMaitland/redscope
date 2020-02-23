from typing import Tuple, List
from redscope.features.schema_introspection.db_objects.schema import Schema
from redscope.features.schema_introspection.formatters.base_formatter import DDLFormatter


class SchemaFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> List[Schema]:
        return [Schema(name=schema[0]) for schema in raw_ddl]
