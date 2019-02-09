from ..bases import BaseTask


class MakePackage(BaseTask):
    @staticmethod
    def lang_id() -> str:
        return "python"

    @staticmethod
    def task_id() -> str:
        return "make-package"

    def _run(self):
        pass


class MakeInitFile(BaseTask):
    @staticmethod
    def lang_id() -> str:
        return "python"

    @staticmethod
    def task_id() -> str:
        return "make-init-file"

    def _run(self):
        pass
