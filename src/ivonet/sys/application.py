#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

__doc__ = """
retrieves the application specific system requirements like the application data folder

Needs the PyObjC dependency to work
"""

from os import path

import sys

import ivonet


def data_directory(application_name=ivonet.TXT_APP_NAME):
    """Specialised code for retrieving the allplication data folder where they save """
    if sys.platform == 'darwin':
        # https://stackoverflow.com/questions/1084697/how-do-i-store-desktop-application-data-in-a-cross-platform-way-for-python
        # noinspection PyUnresolvedReferences
        from AppKit import NSSearchPathForDirectoriesInDomains
        return path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], application_name)
    elif sys.platform == 'win32':
        from os import environ
        return path.join(environ['APPDATA'], application_name)
    return path.expanduser(path.join("~", "." + application_name))


if __name__ == '__main__':
    print(data_directory())
    print(data_directory("FooBarBaz is a long name"))
