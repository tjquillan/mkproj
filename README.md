# mkproj

mkproj is an opinionated tool to generate base projects for a multitude of languages.

## Supported Languages

* Python
* Go [[WIP](https://github.com/iboyperson/mkproj/tree/go-lang)]
* More To Come!

## Installation

Simply run `pip install mkproj`

## Usage

Usage is simple! You simply type `mkproj` then specify the language and mixins you want to use.

### Examples:

* If you wanted to make a base python project called pyproj you would type: `mkproj -l python pyproj`. Here the `-l` flag specifies
the langage you want the project to be made with (in this instance python).


* Now lets say you want this python project to also be initialized with [Pipenv](https://github.com/pypa/pipenv). Instead you would type:
`mkproj -l python -m pipenv pyproj`. Here in addition to the above the `-m` flag specifies the mixins the project should be made with (in this instance
pipenv).
