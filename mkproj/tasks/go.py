import os

from typing import Dict

from .. import config
from ..bases import BaseTask
from ..core import depends
from ..subprocess import call


@depends("make-project-dir")
class ModuleInit(BaseTask):
    @staticmethod
    def lang_id() -> str:
        return "go"

    @staticmethod
    def task_id() -> str:
        return "init-module"

    @staticmethod
    def config_defaults() -> Dict[str, dict]:
        return {
            "go": {
                "url": "github.com",
                "username": config.get_config("user", "name")
            }
        }

    def _run(self) -> str:
        module_name: str = "{}/{}/{}".format(
            config.get_config("go", "url"),
            config.get_config("go", "username"),
            self._data["project-name"],
        )

        os.chdir(self._data["project-path"].absolute())
        call(["go", "mod", "init", module_name])

        return "Go module initialized at: {}".format(self._data["project-path"])
