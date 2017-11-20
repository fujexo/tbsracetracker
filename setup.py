#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://tbsracetracker.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='tbsracetracker',
    version='0.1.0',
    description='Control your TBS Race Tracker using Python',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Philipp Marmet',
    author_email='fujexo@c0d3.ch',
    url='https://github.com/fujexo/tbsracetracker',
    packages=[
        'tbsracetracker',
    ],
    package_dir={'tbsracetracker': 'tbsracetracker'},
    include_package_data=True,
    install_requires=[
        'bluepy'
    ],
    license='GPLv3',
    zip_safe=False,
    keywords='tbsracetracker',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
