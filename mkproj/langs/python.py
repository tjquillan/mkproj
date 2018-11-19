import crayons
from pathlib import Path
import os

from click import echo

from ..subprocess import call
from ..base_lang import BaseLang
from .. import config

class Python(BaseLang):
    def __init__(self):
        self._lang = "python"

        config.add_section_defaults({'python': {}})

    @property
    def lang(self) -> str:
        return self._lang

    def create(self, project_name: str, project_path: Path):
        echo("{0} Creating project at '{1}'".format(crayons.blue("=>"), project_path.absolute()))
        project_path.mkdir()

        os.chdir(project_path.absolute())

        echo("{0} Initializing project with pipenv".format(crayons.blue("=>")))
        call(["pipenv", "install"])


        


        
    