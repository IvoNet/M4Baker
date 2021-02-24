#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__doc__ = """
Global defines
"""

import os

HERE = os.path.abspath(os.path.dirname(__file__))
RESOURCE = os.path.abspath(HERE + '/../resources/')
ICON_APP = RESOURCE + "/yoda.png"

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
TXT_APP_NAME = "M4Baker"
TXT_DESCRIPTION_BLOG = "Ivo's blog"
TXT_URL_BLOG = "https://www.ivonet.nl"
TXT_COMMENT = "Converted with M4Baker.\nhttps://www.ivonet.nl"
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
