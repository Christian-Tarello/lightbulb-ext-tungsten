# -*- coding: utf-8 -*-
# Copyright © Christian-Tarello 2022-present
#
# This file is part of Tungsten.
#
# Tungsten is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tungsten is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tungsten. If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup, find_namespace_packages
import os
import types
import re

name = "lightbulb"


def parse_meta():
    with open(os.path.join("lightbulb", "ext", "tungsten", "__init__.py")) as fp:
        code = fp.read()

    token_pattern = re.compile(r"^__(?P<key>\w+)?__\s*=\s*(?P<quote>(?:'{3}|\"{3}|'|\"))(?P<value>.*?)(?P=quote)", re.M)

    groups = {}

    for match in token_pattern.finditer(code):
        group = match.groupdict()
        groups[group["key"]] = group["value"]

    return types.SimpleNamespace(**groups)


def long_description():
    with open("README.md") as fp:
        return fp.read()


def parse_requirements_file(path):
    with open(path, "r") as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


def parse_requirements_files(*args):
    for path in args:
        if os.path.exists(path):
            return parse_requirements_file(path)
            


meta = parse_meta()

setup(
    name="lightbulb-ext-tungsten",
    version=meta.version,
    description="An add-on for hikari-lightbulb providing an alternative for handling component interactions.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="Christian-Tarello",
    author_email="",
    url="https://github.com/Christian-Tarello/lightbulb-ext-tungsten",
    packages=find_namespace_packages(include=[name + "*"]),
    license="GPL-3.0",
    install_requires=parse_requirements_files("requirements.txt", "requires.txt"),
    include_package_data=True,
    python_requires=">=3.8.0,<3.11",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)