from abc import ABCMeta, abstractmethod
from pathlib import Path


class BaseLang(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, project_name: str, project_path: Path):
        pass


    @staticmethod
    @abstractmethod
    def lang_id() -> str:
        pass

    @abstractmethod
    def create(self):
        pass
