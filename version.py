#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 14:20:25$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Versioning file
"""


def read_version():
    try:
        return open("VERSION", "r").read().strip()
    except IOError:
        return "0.0.0"


def write_version(version):
    with open("VERSION", "w") as fo:
        fo.write(version)


def inc_version(version):
    major, minor, build = version.split(".")
    build = str(int(build) + 1)
    return f"{major}.{minor}.{build}"


def versioning():
    new_version = inc_version(read_version())
    version = input(f"Version (enter = {new_version}): ")
    if not version:
        version = new_version
    write_version(version)


if __name__ == '__main__':
    versioning()
