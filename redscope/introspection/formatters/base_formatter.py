from abc import ABC, abstractmethod
from typing import List, Tuple
from redgiant.redscope.introspection.ddl import DDL
from redgiant.redscope.project import RedScopeProject


class DDLFormatter(ABC):

    def __init__(self):
        self.template_env = RedScopeProject.get_jinja_env('redscope')

    @abstractmethod
    def format(self, raw_ddl: Tuple[str]) -> List[DDL]:
        pass
