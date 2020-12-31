from typing import Tuple, Dict
from redgiant.redscope.introspection.schema import Schema
from redgiant.redscope.introspection.formatters.base_formatter import DDLFormatter


class SchemaFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> Dict[str, Schema]:

        schemas = {}
        for schema in raw_ddl:
            ddl = f'CREATE SCHEMA IF NOT EXISTS{schema[0]};'
            schema_obj = Schema(name=schema[0], ddl=ddl)
            schemas[schema_obj.name] = schema_obj
        return schemas
