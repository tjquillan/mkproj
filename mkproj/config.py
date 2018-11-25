import configparser

from pathlib import Path

from appdirs import AppDirs


DIRS = AppDirs("mkproj", "iboyperson")

if not Path(DIRS.user_config_dir).exists():
    Path(DIRS.user_config_dir).mkdir()

CONFIG_FILE = "{0}/mkproj.conf".format(DIRS.user_config_dir)

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

DEFAULT_VALUES = {
    "core": {"license": "MIT", "git": "yes", "readme": "yes"},
    "user": {"name": "John Doe", "email": "john.doe@gmail.com"},
}


def add_section_defaults(section: dict):
    DEFAULT_VALUES.update(section)


def set_config(section: str, key: str, value: str):
    if section not in config:
        config[section] = {}

    section_list = config[section]
    section_list[key] = value

    with open(CONFIG_FILE, "w") as file:
        config.write(file)


def get_config(section: str, key: str):
    return config.get(section, key, fallback=DEFAULT_VALUES[section][key])


def getboolean_config(section: str, key: str):
    return config.getboolean(section, key, fallback=bool(DEFAULT_VALUES[section][key]))
