import os

from .. import LockingDict, config
from ..bases import BaseTask
from ..core import depends
from ..subprocess import call


@depends("make-project-dir")
class ModuleInit(BaseTask):
    def __init__(self, data: LockingDict):
        super().__init__(data)
        config.add_section_defaults({
            "go": {
                "url": "github.com",
                "username": config.get_config("user", "name")
            }
        })

    @staticmethod
    def lang_id() -> str:
        return "go"

    @staticmethod
    def task_id() -> str:
        return "init-module"

    def _run(self) -> str:
        module_name: str = "{}/{}/{}".format(
            config.get_config("go", "url"),
            config.get_config("go", "username"),
            self._data["project-name"],
        )

        os.chdir(self._data["project-path"].absolute())
        call(["go", "mod", "init", module_name])

        return "Go module initialized at: {}".format(self._data["project-path"])
