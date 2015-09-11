#!/usr/bin/env python
import os
from setuptools import setup, find_packages

root = os.path.abspath(os.path.dirname(__file__))

setup(
    name='fatek-fbs-lib',
    version='0.1.4',
    description='Fatek FBs communication lib',
    author='Marcin Rim',
    author_email='rimek@poczta.fm',
    url='http://rimek.org/',
    packages=find_packages(),
    test_suite='tests',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pymodbus'
    ],
    scripts=['bin/fatek-cli'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
