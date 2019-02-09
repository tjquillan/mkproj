from pathlib import Path
from typing import Dict

from appdirs import AppDirs

from .bases import BaseTask


# Dictionary of all available languages and their classes
APP_DIRS: AppDirs = AppDirs("mkproj", "iboyperson")

PROJECT_NAME: str = ""
PROJECT_PATH: Path = None

langs: dict = {}

tasks: Dict[str, Dict[str, BaseTask]] = {}

# Used to controle the verbosity of the program
verbosity: bool = False
