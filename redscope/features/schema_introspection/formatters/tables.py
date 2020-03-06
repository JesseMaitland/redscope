from itertools import groupby
from typing import Tuple, List, Dict
from redscope.features.schema_introspection.db_objects.table import Table
from redscope.features.schema_introspection.formatters.base_formatter import DDLFormatter


class TableFormatter(DDLFormatter):

    def __init__(self, raw_ddl: Tuple[str] = None):
        self.raw_ddl = raw_ddl or ()

    def format(self, raw_ddl: Tuple[str]) -> List[Table]:
        self.raw_ddl = raw_ddl
        groups = self.perform_grouping()
        groups = self.concat_lines(groups)
        return self.convert_to_tables(groups)

    @staticmethod
    def sort_key(row: Tuple) -> Tuple:
        return row[0], row[1]

    def perform_grouping(self) -> Dict:
        sorted_ddl = sorted(self.raw_ddl, key=self.sort_key)
        groups = {}
        for key, group in groupby(sorted_ddl, key=self.sort_key):
            groups[key] = (list(group))
        return groups

    @staticmethod
    def concat_lines(groups: Dict):
        concat_tables = {}

        for raw_table_key in groups.keys():
            table_def = groups[raw_table_key]
            table_lines = []
            for row in table_def:
                line = ' '.join([r for r in row[2:] if type(r) is not int])
                line = line.lstrip().rstrip()
                line = line + ','
                line = TableFormatter.format_keywords(line)
                table_lines.append(line)
                table_lines = TableFormatter.format_tabs(table_lines)
            concat_tables[raw_table_key] = table_lines
        return concat_tables

    @staticmethod
    def convert_to_tables(groups: Dict) -> List[Table]:
        tables = []
        for table_name, ddl_strings in groups.items():
            ddl = '\n'.join(ddl_strings)
            ddl = ddl.rstrip(',')
            table = Table(schema=table_name[0], name=table_name[1], ddl=ddl)
            tables.append(table)
        return tables

    @staticmethod
    def format_keywords(line: str) -> str:
        line = line.replace(' integer', ' INT')
        line = line.replace(' character varying', ' VARCHAR')
        line = line.replace(' numeric', ' DECIMAL')
        line = line.replace(' timestamp', ' TIMESTAMP')
        line = line.replace(' without time zone', ' WITHOUT TIME ZONE')
        line = line.replace(' with time zone', ' WITH TIME ZONE')
        line = line.replace(' bigint', ' BIGINT')
        line = line.replace(' double precision', ' FLOAT')
        line = line.replace(' boolean', ' BOOLEAN')
        line = line.replace(' date', ' DATE')
        return line

    @staticmethod
    def format_tabs(table_lines) -> List[str]:
        max_length = max([len(l.split(' ')[0]) for l in table_lines])

        new_lines = []
        for line in table_lines:
            col_name = line.split(' ')[0]
            col_name_len = len(col_name)
            diff = max_length - col_name_len
            spaces = ' ' * diff
            new_line = col_name + ' ' + spaces + ' '.join(line.split()[1:])
            new_lines.append(new_line)
        return new_lines
