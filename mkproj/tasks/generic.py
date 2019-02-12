from .. import templates
from ..bases import BaseTask
from ..core import depends
from ..subprocess import call


@depends()
class MakeProjectDir(BaseTask):
    @staticmethod
    def lang_id() -> str:
        return "generic"

    @staticmethod
    def task_id() -> str:
        return "make-project-dir"

    def _run(self):
        self._data["project-path"].mkdir()
        return "Created project directory at: {}".format(
            self._data["project-path"].absolute()
        )


@depends("make-project-dir")
class MakeReadme(BaseTask):
    @staticmethod
    def lang_id() -> str:
        return "generic"

    @staticmethod
    def task_id() -> str:
        return "make-readme"

    def _run(self):
        with open(
            "{0}/README.md".format(str(self._data["project-path"].absolute())), "w"
        ) as file:
            templates.write_to_file(
                file,
                templates.get("generic", "README.md"),
                {"name": self._data["project-name"]},
            )
        return "README created in {}".format(self._data["project-path"].absolute())


@depends("make-project-dir")
class GitInit(BaseTask):
    @staticmethod
    def lang_id() -> str:
        return "generic"

    @staticmethod
    def task_id() -> str:
        return "git-init"

    def _run(self):
        call(["git", "-C", self._data["project-path"].absolute(), "init"])
        return "Project initialized with git"
