from abc import ABCMeta, abstractmethod
from typing import Dict

from . import LockingDict, config, spinner


class TaskFailedException(Exception):
    pass


class BaseTask(metaclass=ABCMeta):
    def __init__(self, data: LockingDict):
        self._data: LockingDict = data

    @staticmethod
    @abstractmethod
    def task_id() -> str:
        pass

    @staticmethod
    @abstractmethod
    def lang_id() -> str:
        pass

    @staticmethod
    def mixin_id() -> str:
        return None

    @staticmethod
    def depends() -> set:
        return set()

    @staticmethod
    def overrides() -> set:
        return set()

    @staticmethod
    def config_defaults() -> Dict[str, dict]:
        return {}

    @abstractmethod
    def _run(self) -> str:
        pass

    def run(self):
        config.add_section_defaults(self.config_defaults())

        try:
            msg: str = self._run()
            spinner.print_info(msg)
        except Exception as e:
            spinner.print_error("Task with id: '{}' has failed: {}".format(self.task_id(), e))
            raise TaskFailedException
