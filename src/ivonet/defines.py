#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 14:45:47$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Global defines
"""

import os

from ivonet.sys.application import data_directory

TXT_APP_NAME = "M4Baker"
HERE = os.path.abspath(os.path.dirname(__file__))
RESOURCE = os.path.abspath(HERE + '/../resources/')
ICON_APP = RESOURCE + "/yoda.png"

SETTINGS_DIRECTORY = data_directory(TXT_APP_NAME)
if not os.path.isdir(SETTINGS_DIRECTORY):
    os.mkdir(SETTINGS_DIRECTORY)

SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, f"{TXT_APP_NAME}.ini")

try:
    VERSION = open(os.path.join(RESOURCE, "VERSION"), "r").read().strip()
except IOError as e:
    VERSION = "0.0.0"

DEVELOPERS = [
    "Ivo Woltring"
]

# Art
ART_PREFIX = "inART_"

# texts
TXT_DESCRIPTION_BLOG = "Ivo's blog"
TXT_URL_BLOG = "https://www.ivonet.nl"
TXT_COMMENT = "Converted with M4Baker.\nhttps://github.com/IvoNet/ivonet-audiobook"
TXT_COPYRIGHT = "M4Baker (c) 2021 Ivo Woltring"
TXT_ABOUT_DESCRIPTION = """Converts mp3 files to m4b with metadata and chapter information"""
TXT_LICENSE = """Copyright 2021 Ivo Woltring
        
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

FILE_WILDCARD = "M4Baker (*.ivo)|*.ivo|" \
                "All files (*.*)|*.*"
