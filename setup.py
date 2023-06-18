#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import os
import sys
from setuptools import setup, find_packages
import setuptools
from pkg_resources import parse_version

assert(parse_version(setuptools.__version__) >= parse_version("38.6.0"))

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="bophono",
    version="0.2.0",  #edit version in __init__.py
    author="Esukhia development team",
    author_email="roux.elie@gmail.com",
    description="Python utils for Tibetan phonetics in different dialects",
    license="MIT",
    keywords="phonetics IPA tibetan",
    url="https://github.com/Esukhia/bophono",
    packages=find_packages(),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    project_urls={
        'Source': 'https://github.com/Esukhia/bophono',
        'Tracker': 'https://github.com/Esukhia/bophono/issues',
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Tibetan"
    ],
    package_data={'bophono': ['data/*', 'data/chinese/*']},
    python_requires='>=3',
)
