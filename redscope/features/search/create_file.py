import csv
from prettytable import PrettyTable
from redscope.features.search.file_searching import SearchResult


class SaveSearchResultFile:

    def __init__(self, search_result: SearchResult, file_name: str, file_type: str = '.txt'):
        self.search_result = search_result
        self.file_name = file_name
        self.file_type = file_type

    def call(self):
        pretty_table = self.make_text_table()
        self.save_csv_file(pretty_table)

    def make_text_table(self) -> PrettyTable:
        pretty_table = PrettyTable()
        pretty_table.field_names = ['table_name', 'file_path']

        table_names = self.search_result.keys()
        table_names.sort()

        for table_name in table_names:
            paths = self.search_result[table_name]
            for path in paths:
                pretty_table.add_row([table_name, path])
        return pretty_table

    def save_pretty_table_file(self, pretty_table: PrettyTable) -> None:
        with open(self.file_name, mode="w+") as file:
            file.writelines(pretty_table.get_string())

    def save_csv_file(self, pretty_table: PrettyTable):
        with open(self.file_name, mode="w+") as file:
            writer = csv.writer(file)
            writer.writerow(pretty_table.field_names)
            for row in pretty_table:
                row.border = False
                row.header = False
                writer.writerow(row.get_string(fields=pretty_table.field_names).strip().split())
