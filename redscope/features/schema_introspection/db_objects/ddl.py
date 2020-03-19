from abc import ABC, abstractmethod


class DDL(ABC):

    def __init__(self, name: str):
        self.name = name

    @property
    @abstractmethod
    def file_name(self) -> str:
        pass

    @property
    @abstractmethod
    def create(self) -> str:
        pass

    @property
    @abstractmethod
    def create_if_not_exist(self) -> str:
        pass

    @property
    @abstractmethod
    def drop(self) -> str:
        pass

    @property
    @abstractmethod
    def drop_if_exist(self) -> str:
        pass
