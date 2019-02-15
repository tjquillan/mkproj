from pathlib import Path
from typing import Dict

import yaml

from . import environment

if not Path(environment.APP_DIRS.user_config_dir).exists():
    Path(environment.APP_DIRS.user_config_dir).mkdir()

CONFIG_FILE: str = "{0}/mkproj.yml".format(environment.APP_DIRS.user_config_dir)

DEFAULT_VALUES: Dict[str, dict] = {
    "core": {"license": "MIT"},
    "user": {"name": "John Doe", "email": "john.doe@gmail.com"},
    "tasks": {"skip": ""}
}


def add_section_defaults(section: dict):
    DEFAULT_VALUES.update(section)


try:
    with open(CONFIG_FILE, "r") as cfg:
        config_data = yaml.load(cfg)
except FileNotFoundError:
    config_data = {}


def set_config(section: str, key: str, value: str):
    if section not in config_data:
        config_data[section] = {}

    section_list = config_data[section]
    section_list[key] = value

    with open(CONFIG_FILE, "w") as file:
        file.write(yaml.dump(config_data, default_flow_style=False))


def get_config(section: str, key: str):
    try:
        return config_data[section][key]
    except (NameError, KeyError):
        return DEFAULT_VALUES[section][key]


def getboolean_config(section: str, key: str) -> bool:
    return bool(get_config(section, key))
