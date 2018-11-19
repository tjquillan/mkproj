from abc import ABCMeta, abstractmethod
from pathlib import Path

class BaseLang(metaclass=ABCMeta):
    @property
    @abstractmethod
    def lang(self) -> str:
        pass

    @abstractmethod
    def create(self, project_name: str, project_path: Path):
        pass