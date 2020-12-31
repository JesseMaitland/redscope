from itertools import groupby
from typing import Tuple, List
from redgiant.redscope.introspection.ddl import DDL
from redgiant.redscope.introspection.schema.table import Table
from redgiant.redscope.introspection.formatters.base_formatter import DDLFormatter


class TableFormatter(DDLFormatter):

    def format(self, raw_ddl: Tuple[str]) -> List[DDL]:
        raw_ddl = self.group_columns(raw_ddl)
        template = self.template_env.get_template('table.sql')
        template_simple = self.template_env.get_template('table_simple.sql')

        tables = []
        for key, value in raw_ddl.items():
            i = max([len(i[2]) for i in value])
            content = template.render(columns=value, i=i)
            content_simple = template_simple.render(columns=value, i=i)
            schema, name = key.split('.')[:2]
            table = Table(schema=schema, name=name, ddl=content, simple_ddl=content_simple)
            tables.append(table)
        return tables

    @staticmethod
    def grouping_key(row: Tuple) -> Tuple:
        return row[0], row[1]

    def group_columns(self, raw_ddl: Tuple[str]):

        sorted_ddl = sorted(raw_ddl, key=self.grouping_key)
        groups = {}
        for key, group in groupby(sorted_ddl, key=self.grouping_key):
            groups[f"{key[0]}.{key[1]}"] = list(group)

        # keeps the column order as defined in the db
        for group in groups.values():
            group.sort(key=lambda x: x[3])
        return groups
