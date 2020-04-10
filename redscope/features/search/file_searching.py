import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Iterator, Dict, Tuple


def search_directory(path: Path, extension: str) -> Iterator[Path]:
    glob_pattern = f"**/*.{extension}"
    return path.glob(glob_pattern)


class SearchResult:

    def __init__(self):
        self._search_results: Dict[str, Path] = {}

    def __setitem__(self, key, value):
        self._search_results[key] = value

    def __getitem__(self, key):
        return self._search_results[key]

    def add_result(self, key: str, path: Path):
        self._search_results[key] = path

    def get_result(self, key: str):
        return self._search_results.get(key, None)

    def results(self) -> List[Tuple[str, Path]]:
        return list(self._search_results.items())

    def keys(self) -> List[str]:
        return list(self._search_results.keys())

    def values(self) -> List[Path]:
        return list(self._search_results.values())

    def empty(self) -> bool:
        return self._search_results == {}

    @staticmethod
    def combine_results(*search_results: 'SearchResult') -> 'SearchResult':

        # first find all the keys which we have
        all_keys = []
        final_results = SearchResult()

        for search_result in search_results:
            all_keys.extend(search_result.keys())

        unique_keys = list(set(all_keys))

        for unique_key in unique_keys:
            final_result_values = []
            for search_result in search_results:
                try:
                    results = search_result[unique_key]
                    final_result_values.append(results)
                except KeyError:
                    continue
            final_results[unique_key] = final_result_values

        return final_results


class BaseFileSearcher(ABC):

    def __init__(self, path: Path):
        self.path = path

    def search(self, search_strings: List[str]) -> SearchResult:
        search_results = SearchResult()
        text_to_search = self._get_text_to_search()

        for search_string in search_strings:
            # do a coarse search first using the in operator because it is loads faster
            if search_string in text_to_search:
                # if the string is in our text to search, do a more exact search using regex
                pattern = re.compile(rf"\b{search_string}\b")
                if pattern.search(text_to_search):
                    search_results[search_string] = self.path

        return search_results

    @abstractmethod
    def _get_text_to_search(self) -> str:
        pass


class SQLFile(BaseFileSearcher):

    def __init__(self, path: Path):
        super().__init__(path=path)

    def _get_text_to_search(self) -> str:

        lines_to_search = []

        with self.path.open() as file:
            for line in file:

                if '/*' in line:    # if we find a multi-line comment, skip lines until we find the end marker.

                    for comment_line in file:
                        if '*/' not in comment_line:
                            continue

                if '--' in line:    # in all cases just skip comment lines
                    continue

                lines_to_search.append(line)

        return ''.join(lines_to_search)


class PythonFile(BaseFileSearcher):

    def __init__(self, path: Path):
        super().__init__(path=path)

    # TODO: implement logic to skip comment strings in python files
    def _get_text_to_search(self) -> str:
        return self.path.read_text()
