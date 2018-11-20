from pathlib import Path
import os

from click import echo

from .. import config, printer, templates
from ..subprocess import call
from ..base_lang import BaseLang

class Python(BaseLang):
    def __init__(self):
        self._lang = "python"

        config.add_section_defaults({'python': {}})

    @property
    def lang(self) -> str:
        return self._lang

    def create(self, project_name: str, project_path: Path):
        printer.print_info("Creating project at '{0}'".format(project_path.absolute()))
        project_path.mkdir()

        printer.print_info("Creating python package '{0}' in project dir".format(project_name))
        package_dir = Path(project_path.joinpath(Path(project_name)))
        package_dir.mkdir()
        open("{0}/__init__.py".format(str(package_dir.absolute())), "a").close()
        with open("{0}/__version__.py".format(str(package_dir.absolute())), "w") as version_file:
            version_file.write("__version__ = \"\"")

        printer.print_info("Creating base setup.py")
        with open("{0}/setup.py".format(str(project_path.absolute())), "w") as setup_file:
            templates.write_to_template(setup_file,
                                        templates.get_template(self._lang, "setup.py"),
                                        {
                                            'name': project_name,
                                            'license': config.get("core", "license"),
                                            'author': config.get("core", "fullName"),
                                            'author_email': config.get("core", "email")
                                        })

        printer.print_info("Initializing project with pipenv")
        os.chdir(project_path.absolute())
        call(["pipenv", "install"])


        


        
    