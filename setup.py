import codecs
import os

from setuptools import find_packages, setup

# Taken from pipenv
# See https://github.com/pypa/pipenv/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

about = {}
with open(os.path.join(here, "mkproj", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name='mkproj',
    version=about["__version__"],
    description='An opinionated tool to generate base projects for a multitude of languages.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/iboyperson/mkproj',
    author='iboyperson',
    author_email='tjquillan@gmail.com',
    packages=find_packages(exclude=["tasks", "tasks.*"]),
    entry_points={
        'console_scripts': [
            'mkproj = mkproj:cli',
        ]
    },
    package_data={
        "": ["LICENSE"],
        "mkproj.templates": ["**/*.templ"]
    },
    include_package_data=True,
    license='MIT',
)
