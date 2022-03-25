#!/usr/bin/python3
""" example: https://github.com/python-beaver/python-beaver/blob/master/setup.py """

from controller import __version__

from setuptools import find_packages, setup

requirements = open('requirements/base.txt').readlines()

setup(name='doorbell',
        version=__version__,
        description='A controller for the Golmar doorbell hack',
        author='Juan Manuel Servera',
        license='LICENSE',
        packages=['controller'],
        url='https://github.com/jmservera/doorbell',
        test_suite='tests',
        tests_require= open('requirements/test.txt').readlines(),
        install_requires=requirements
      )