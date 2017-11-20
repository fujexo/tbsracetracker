"""Setuptools package definition"""

# PLEASE REMOVE UNUSED CODE like CustomInstallCommand if you don't use it

from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
import codecs
import os
import sys

version = sys.version_info[0]
if version > 2:
    pass
else:
    pass

__version__  = None
version_file = "python-tbstracker/version.py"
with codecs.open(version_file, encoding="UTF-8") as f:
    code = compile(f.read(), version_file, 'exec')
    exec(code)


def find_data(packages, extensions):
    """Finds data files along with source.

    :param   packages: Look in these packages
    :param extensions: Look for these extensions
    """
    data = {}
    for package in packages:
        package_path = package.replace('.', '/')
        for dirpath, _, filenames in os.walk(package_path):
            for filename in filenames:
                for extension in extensions:
                    if filename.endswith(".%s" % extension):
                        file_path = os.path.join(
                            dirpath,
                            filename
                        )
                        file_path = file_path[len(package) + 1:]
                        if package not in data:
                            data[package] = []
                        data[package].append(file_path)
    return data

with codecs.open('README.md', 'r', encoding="UTF-8") as f:
    README_TEXT = f.read()

setup(
    name = "python-tbstracker",
    version = __version__,
    packages = find_packages(),
    package_data=find_data(
        find_packages(), ["json", "json.gz"]
    ),
    entry_points = {
        'console_scripts': [
        ]
    },
    install_requires = [
    ],
    author = "fujexo",
    author_email = "https://github.com/fujexo/",
    description = "Control TBS Race Tracker using python",
    long_description = README_TEXT,
    keywords = "TBSRT",
    url = "https://github.com/fujexo/python-tbstracker",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
    ]
)
