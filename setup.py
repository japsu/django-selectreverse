#!/usr/bin/env python

from setuptools import setup, find_packages

import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()

setup(
    name="django-selectreverse",
    version="0.0.1",
    author="Santtu Pajukanta",
    author_email="santtu.pajukanta@tut.fi",
    description="A fork of Koen Biermans' django-selectreverse that provides select_related for reverse relations in Django",
    long_description=read_file('README.rst'),
    license="BSD",
    keywords="django orm reverse",
    url="https://github.com/japsu/django-selectreverse",
    packages=find_packages(exclude=[]),
    install_requires=[
        'Django>=1.2'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
