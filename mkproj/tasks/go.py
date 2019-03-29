import os
from typing import Dict

from .. import config, templates
from ..bases import BaseTask
from ..core import depends
from ..subprocess import call


@depends("make-project-dir")
class MakeMainFile(BaseTask):
    @staticmethod
    def task_id() -> str:
        return "make-main-file"

    @staticmethod
    def lang_id() -> str:
        return "go"

    def _run(self):
        file_path: str = "{}/main.go".format(self._data["project-path"].absolute())
        with open(
            file_path,
            "w"
        ) as main_file:
            templates.write_to_file(
                main_file, templates.get_template("go", "main.go"), self._data
            )

        return "Main file created at: {}".format(file_path)


@depends("make-project-dir")
class ModuleInit(BaseTask):
    @staticmethod
    def task_id() -> str:
        return "init-module"

    @staticmethod
    def lang_id() -> str:
        return "go"

    @staticmethod
    def config_defaults() -> Dict[str, dict]:
        return {
            "go": {
                "url": "github.com",
                "username": config.get_config("user", "username"),
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
