from pathlib import Path
from redscope.api import get_db_connection, load_redscope_env
from redscope.features.search.file_searching import search_directory, SQLFile, SearchResult


# env_path = Path("/Users/jessemaitland/PycharmProjects/redscope/stg.env")
# load_redscope_env(env_path)
# db_connection = get_db_connection('REDSCOPE_DB_URL')


search_path = Path("/Users/jessemaitland/PycharmProjects/redscope/database/schemas/dds")

results = []
for p in search_directory(search_path, 'sql'):
    search_string = ["dds"]

    result = SQLFile(path=p).search(search_string)

    if not result.empty():
        results.append(result)


final_results = SearchResult.combine_results(*results)

