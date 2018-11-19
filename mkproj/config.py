import configparser
from pathlib import Path

config_file = "{0}/.config/mkproj/mkproj.conf".format(Path.home())

config = configparser.ConfigParser()
config.read(config_file)

default_values = {
    'core': {
        'projectsDir': "{0}/projects".format(Path.home())
    }
}

def add_section_defaults(section: dict):
    default_values.update(section)

def get(section: str, key: str) -> str:
    return config.get(section, key, fallback=default_values[section][key])



