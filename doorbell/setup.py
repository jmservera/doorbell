#!/usr/bin/python3
import io
import os
from controller import __version__
from setuptools import setup

""" from an example found in """
""" https://github.com/python-beaver/python-beaver/blob/master/setup.py """


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


requirements = read_requirements('requirements/base.txt')

setup(name='doorbell',
      version=__version__,
      description='A controller for the Golmar doorbell hack',
      long_description=read("../README.md"),
      long_description_content_type="text/markdown",
      author='Juan Manuel Servera',
      author_email='juan@email',
      license='LICENSE',
      packages=['controller'],
      url='https://github.com/jmservera/doorbell',
      test_suite='tests',
      extras_require={
        "test": read_requirements('requirements/test.txt')
      },
      setup_requires=['pytest-runner', 'flake8'],
      install_requires=requirements
      )
