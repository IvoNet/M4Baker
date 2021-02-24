#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

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
    return "{major}.{minor}.{build}".format(major=major, minor=minor, build=build)


def versioning():
    new_version = inc_version(read_version())
    version = input(f"Version (enter = {new_version}): ")
    if not version:
        version = new_version
    write_version(version)


if __name__ == '__main__':
    versioning()
