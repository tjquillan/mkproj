from appdirs import AppDirs
import configparser
from pathlib import Path

dirs = AppDirs("mkproj", "iboyperson")

if not Path(dirs.user_config_dir).exists():
    Path(dirs.user_config_dir).mkdir()

config_file = "{0}/mkproj.conf".format(dirs.user_config_dir)

config = configparser.ConfigParser()
config.read(config_file)

default_values = {
    'core': {
        'license': 'MIT',
        'git': 'yes',
        'readme': 'yes',
    },
    'user': {
        'name': 'John Doe',
        'email': 'john.doe@gmail.com',
    }
}

def add_section_defaults(section: dict):
    default_values.update(section)

def set_config(section: str, key: str, value: str):
    if section not in config:
        config[section] = {}

    section = config[section]
    section[key] = value

    with open(config_file, "w") as file:
        config.write(file)

def get_config(section: str, key: str):
    return config.get(section, key, fallback=default_values[section][key])

def getboolean_config(section: str, key: str):
    return config.getboolean(section, key, fallback=bool(default_values[section][key]))


