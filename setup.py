#!/usr/bin/env python

import os

from setuptools import setup, find_packages

from fatek.version import __version__

root = os.path.abspath(os.path.dirname(__file__))

setup(
    name='fatek-fbs-lib',
    install_requires=open(os.path.join(root, 'requirements.txt')).readlines(),
    version=".".join([str(x) for x in __version__]),
    description='Fatek FBs communication lib',
    author='Marcin Rim',
    author_email='rimek@poczta.fm',
    url='http://rimek.org/',
    packages=find_packages(),
    test_suite='tests',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'fatek = fatek.tools:console',
        ],
    }
)
