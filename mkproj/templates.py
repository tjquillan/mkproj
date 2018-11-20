from pathlib import Path
from string import Template

from . import MKPROJ_ROOT

templates_dir = Path("{0}/templates".format(MKPROJ_ROOT))

def get_template(section: str, template: str):
    template_path = Path("{0}/{1}/{2}.templ".format(str(templates_dir.absolute()), section, template))
    if template_path.exists():
        with open(str(template_path.absolute()), "r") as template:
            return Template(template.read())



