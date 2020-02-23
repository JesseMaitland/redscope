from abc import ABC, abstractmethod
from typing import List, Tuple
from redscope.features.schema_introspection.db_objects.ddl import DDL


class DDLFormatter(ABC):

    @abstractmethod
    def format(self, raw_ddl: Tuple[str]) -> List[DDL]:
        pass
