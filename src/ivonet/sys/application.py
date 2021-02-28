#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 14:45:53$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
retrieves the application specific system requirements like the application data folder

Needs the PyObjC dependency to work
"""

from os import path

import sys


def data_directory(application_name) -> str:
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
