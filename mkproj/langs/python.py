import os

from pathlib import Path

from .. import config, printer, templates
from ..base_lang import BaseLang
from ..subprocess import call


class Python(BaseLang):
    def __init__(self):
        self._lang = "python"

        config.add_section_defaults({'python': {}})

    @property
    def lang(self) -> str:
        return self._lang

    def create(self, project_name: str, project_path: Path):
        printer.print_info("Creating python package '{0}' in '{1}'".format(project_name, str(project_path.absolute())))
        package_dir = Path(project_path.joinpath(Path(project_name)))
        package_dir.mkdir()
        printer.print_verbose("Creating file '__init__.py'", True)
        open("{0}/__init__.py".format(str(package_dir.absolute())), "a").close()
        printer.print_verbose("Creating file '__main__.py'", True)
        open("{0}/__main__.py".format(str(package_dir.absolute())), "a").close()
        with open("{0}/__version__.py".format(str(package_dir.absolute())), "w") as version_file:
            version_file.write("__version__ = \"\"")

        printer.print_info("Creating file 'setup.py'")
        with open("{0}/setup.py".format(str(project_path.absolute())), "w") as setup_file:
            templates.write_to_file(setup_file,
                                        templates.get(self._lang, "setup.py"),
                                        {
                                            'name': project_name,
                                            'license': config.get_config("core", "license"),
                                            'author': config.get_config("user", "name"),
                                            'author_email': config.get_config("user", "email")
                                        })

        printer.print_info("Initializing project with pipenv")
        os.chdir(project_path.absolute())
        call(["pipenv", "install"])
