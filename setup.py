# encoding: utf-8
"""A simple wrapper for the Thenmap API.

See http://thenmap.net
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def readme():
    """Import README for use as long_description."""
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        return f.read()


setup(
    name='thenmap',
    version='1.0.1',

    description='A Thenmap API wrapper',
    long_description=readme(),
    url='https://github.com/jplusplus/thenmap-python',
    author='Leonard Wallentin, J++ Stockholm',
    author_email='stockholm@jplusplus.org',
    license='MIT',
    packages=["thenmap"],
    install_requires=["shapely", "requests", "six"],
)
