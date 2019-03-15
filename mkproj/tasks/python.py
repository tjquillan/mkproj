import os
from pathlib import Path

from .. import config, templates
from ..bases import BaseTask
from ..core import depends
from ..subprocess import call


@depends("make-project-dir")
class MakePackage(BaseTask):
    @staticmethod
    def task_id() -> str:
        return "make-package-dir"

    @staticmethod
    def lang_id() -> str:
        return "python"

    def _run(self) -> str:
        package_dir = Path(
            self._data["project-path"].joinpath(Path(self._data["project-name"]))
        )
        package_dir.mkdir()
        self._data["source-path"] = package_dir
        return "Package created at: {}".format(package_dir.absolute())


@depends("make-project-dir", "make-package-dir")
class MakeInitFile(BaseTask):
    @staticmethod
    def task_id() -> str:
        return "make-init-file"

    @staticmethod
    def lang_id() -> str:
        return "python"

    def _run(self) -> str:
        open(
            "{0}/__init__.py".format(str(self._data["source-path"].absolute())), "a"
        ).close()
        return "Init file created at: {}".format(
            "{}/__init__.py".format(self._data["source-path"].absolute())
        )


@depends("make-project-dir", "make-package-dir")
class MakeMainFile(BaseTask):
    @staticmethod
    def task_id() -> str:
        return "make-main-file"

    @staticmethod
    def lang_id() -> str:
        return "python"

    def _run(self) -> str:
        open(
            "{0}/__main__.py".format(str(self._data["source-path"].absolute())), "a"
        ).close()
        return "Main file created at: {}".format(
            "{}/__main__.py".format(self._data["source-path"].absolute())
        )


@depends("make-project-dir")
class MakeSetupFile(BaseTask):
    @staticmethod
    def task_id() -> str:
        return "make-setup-file"

    @staticmethod
    def lang_id() -> str:
        return "python"

    def _run(self) -> str:
        with open(
            "{0}/setup.py".format(str(self._data["project-path"].absolute())), "w"
        ) as setup_file:
            templates.write_to_file(
                setup_file,
                templates.get(self.lang_id(), "setup.py"),
                {
                    "name": self._data["project-name"],
                    "license": config.get_config("core", "license"),
                    "author": config.get_config("user", "name"),
                    "author_email": config.get_config("user", "email"),
                },
            )
        return "Setup file created at: {}".format(
            "{}/setup.py".format(self._data["project-path"].absolute())
        )


@depends("make-project-dir")
class PipenvInit(BaseTask):
    @staticmethod
    def task_id() -> str:
        return "pipenv-init"

    @staticmethod
    def lang_id() -> str:
        return "python"

    @staticmethod
    def mixin_id() -> str:
        return "pipenv"

    def _run(self) -> str:
        os.chdir(self._data["project-path"].absolute())
        call(["pipenv", "install"])

        return "Project initialized with pipenv"
