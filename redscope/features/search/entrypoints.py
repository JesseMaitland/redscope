from typing import Dict, List
from pathlib import Path
from redscope.features.search.file_searching import search_directory, SQLFile, PythonFile, SearchResult
from redscope.features.search.create_file import SaveSearchResultFile
from redscope.features.schema_introspection.db_introspection import introspect_tables
from redscope.terminal.tools.entry import EntryPoint


search_args = {

    ('path',): {
        'help': "the root directory path you would like to search. All children will be searched recursively.",
        'type': Path
    },

    ('file_name',): {
        'help': "what to name the output file including extension",
        'type': str
    }
}


class SearchFunctionEntryPoint(EntryPoint):

    def __init__(self, args_config: Dict):
        super().__init__(args_config=args_config)
        self.set_db_connection()

    def call(self) -> None:
        table_names = self.get_table_names()
        search_results = self.search_sql_files(table_names)
        self.save_text_file(search_results)

    def get_table_names(self) -> List[str]:
        data_catalog = introspect_tables(self.db_connection)
        return [t.full_name for t in data_catalog.tables]

    def search_sql_files(self, table_names: List[str]) -> SearchResult:
        paths = search_directory(self.cmd_args.path, 'sql')
        results = []
        for path in paths:
            search_result = SQLFile(path).search(table_names)

            if not search_result.empty():
                results.append(search_result)

        return SearchResult.combine_results(*results)

    def save_text_file(self, search_result: SearchResult) -> None:
        SaveSearchResultFile(search_result, self.cmd_args.file_name, '.txt').call()
