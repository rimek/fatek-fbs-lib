#!/usr/bin/env python
import os

from setuptools import find_packages, setup

VERSION = '0.1.8'

root = os.path.abspath(os.path.dirname(__file__))

setup(
    name='fatek-fbs-lib',
    version=VERSION,
    description='Fatek FBs communication lib',
    author='Marcin Rim',
    author_email='rimek@poczta.fm',
    url='https://github.com/rimek/fatek-fbs-lib',
    packages=find_packages(),
    test_suite='tests',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pymodbus3; python_version >= '3.0'",
        "pymodbus; python_version < '3.0'",
        'pyserial',
    ],
    scripts=['bin/fatek-cli'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
