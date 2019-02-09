import os

from pathlib import Path

from .. import config, environment, printer, templates
from ..bases import BaseLang
from ..subprocess import call


config.add_section_defaults({"python": {}})


class Python(BaseLang):
    def __init__(self):
        self._package_dir = Path(
            environment.PROJECT_PATH.joinpath(Path(environment.PROJECT_NAME))
        )

    @staticmethod
    def lang_id() -> str:
        return "python"

    def create(self):
        @printer.report(
            "Creating python package '{0}' in '{1}'".format(
                environment.PROJECT_NAME, str(environment.PROJECT_PATH.absolute())
            )
        )
        def make_project_dir():
            self._package_dir.mkdir()

        @printer.report("Creating file '__init__.py'")
        def make_init_file():
            open(
                "{0}/__init__.py".format(str(self._package_dir.absolute())), "a"
            ).close()

        @printer.report("Creating file '__main__.py'")
        def make_main_file():
            open(
                "{0}/__main__.py".format(str(self._package_dir.absolute())), "a"
            ).close()

        @printer.report("Creating file '__version__.py'")
        def make_version_file():
            with open(
                "{0}/__version__.py".format(str(self._package_dir.absolute())), "w"
            ) as version_file:
                version_file.write('__version__ = ""')

        @printer.report("Creating file 'setup.py'")
        def make_setup_file():
            with open(
                "{0}/setup.py".format(str(environment.PROJECT_PATH.absolute())), "w"
            ) as setup_file:
                templates.write_to_file(
                    setup_file,
                    templates.get(self.lang_id(), "setup.py"),
                    {
                        "name": environment.PROJECT_NAME,
                        "license": config.get_config("core", "license"),
                        "author": config.get_config("user", "name"),
                        "author_email": config.get_config("user", "email"),
                    },
                )

        @printer.report("Initializing project with pipenv")
        def pipenv():
            os.chdir(environment.PROJECT_PATH.absolute())
            call(["pipenv", "install"])

        make_project_dir()
        make_init_file()
        make_main_file()
        make_version_file()
        make_setup_file()
        pipenv()
