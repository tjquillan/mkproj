import os

from setuptools import find_packages, setup

# Taken from pipenv
# See https://github.com/pypa/pipenv/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))
about = {}

with open(os.path.join(here, "mkproj", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name='mkproj',
    version=about["__version__"],
    packages=find_packages(exclude=["tasks", "tasks.*"]),
    url='https://github.com/iboyperson/mkproj',
    license='MIT',
    author='iboyperson',
    author_email='tjquillan@gmail.com',
    description='An application to manage dotfiles efficiently with GNU Stow',
    entry_points={
        'console_scripts': [
            'mkproj = mkproj:cli',
        ]
    },
    package_data={
        "": "LICENSE",
    },
    include_package_data=True,
)
