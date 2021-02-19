#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__doc__ = """
Global defines
"""

import os

import wx

HERE = os.path.abspath(os.path.dirname(__file__))
RESOURCE = os.path.abspath(HERE + '/../resources/')
ICON_APP = RESOURCE + "/yoda.png"
APP_NAME = "M4Baker"
VERSION = "0.1.0"
COPYRIGHT = "(c) 2021 Ivo Woltring"
ABOUT_DESCRIPTION = """Converts mp3 files to m4b with metadata and chapter information"""
BLOG = "https://www.ivonet.nl"
BLOG_DESCRIPTION = "Ivo's blog"
DEVELOPERS = [
    "Ivo Woltring"
]
LICENSE = """Copyright 2021 Ivo Woltring
        
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

# File Menu
FILE_MENU_PROCESS = wx.NewIdRef()
FILE_MENU_CLEAR = wx.NewIdRef()
FILE_MENU_STOP_PROCESS = wx.NewIdRef()
FILE_MENU_SHOW_LOG = wx.NewIdRef()
FILE_MENU_TO_DIR = wx.NewIdRef()

# Art
ART_PREFIX = "inART_"
