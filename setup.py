#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import os
import sys
from setuptools import setup, find_packages

setup(
    name="bophono",
    version="0.2.0",
    author="Esukhia development team",
    author_email="esukhiadev@gmail.com",
    description="Python utils for Tibetan phonetics in different dialects",
    license="MIT",
    keywords="phonetics ipa tibetan",
    url="https://github.com/Esukhia/bophono",
    packages=find_packages(),
    long_description='',
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
    python_requires='>=3',
)
