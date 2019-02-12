from abc import ABCMeta, abstractmethod

from . import LockingDict, spinner


class BaseLang(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def lang_id() -> str:
        pass

    @abstractmethod
    def create(self):
        pass


class TaskFailedException(Exception):
    pass


class BaseTask(metaclass=ABCMeta):
    def __init__(self, data: LockingDict):
        self._data = data

    @staticmethod
    @abstractmethod
    def lang_id() -> str:
        pass

    @staticmethod
    @abstractmethod
    def task_id() -> str:
        pass

    # @staticmethod
    # @abstractmethod
    # def depends() -> set:
    #     pass

    @abstractmethod
    def _run(self) -> str:
        pass

    def run(self):
        try:
            msg = self._run()
            spinner.print_info(msg)
        except Exception:
            spinner.print_error("Task with id: '{}' has failed".format(self.task_id()))
            raise TaskFailedException
