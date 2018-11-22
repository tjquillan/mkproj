from jinja2 import Environment, PackageLoader, select_autoescape, Template
from pathlib import Path

from . import MKPROJ_ROOT

env = Environment(
    loader=PackageLoader('mkproj', 'templates'),
    autoescape=select_autoescape(['j2'])
)

def get(section: str, template: str):
    template_path = "{0}/{1}.j2".format(section, template)
    return env.get_template(template_path)

def write_to_file(file, template: Template, data: dict):
    file.write(template.render(data))




