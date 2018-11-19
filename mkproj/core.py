from click import echo
import crayons
from pathlib import Path
import sys

from . import config
from .base_lang import BaseLang
from .langs import (python)
from .subprocess import call

class LangManager():
    def __init__(self):
        self._langs = {}
        for lang in BaseLang.__subclasses__():
            self._langs[lang().lang] = lang()

    @property
    def langs(self) -> dict:
        return self._langs
    
    def create(self, project_name: str, lang: str, git: bool):
        project_path = Path("{0}/{1}".format(Path.cwd(), project_name))

        if project_path.exists():
            echo("{0} Project already exists. Aborting...".format(crayons.red("=>")))
            sys.exit(1)

        self._langs[lang].create(project_name, project_path)

        if git:
            echo("{0} Initializing project as git repository".format(crayons.blue("=>")))
            call(["git", "-C", project_path.absolute(),"init"])