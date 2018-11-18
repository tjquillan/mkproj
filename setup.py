from setuptools import setup, find_packages

from mkproj.__version__ import __version__

setup(
    name='mkproj',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/iboyperson/mkproj',
    license='MIT',
    author='iboyperson',
    author_email='tjquillan@gmail.com',
    description='An application to manage dotfiles efficiently with GNU Stow',
    install_requires=['click', 'click-completion'],
    entry_points={
        'console_scripts': [
            'mkproj = mkproj:cli',
        ]
    },
)
