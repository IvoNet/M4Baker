#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 13:21:13$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Package module init of the EventEmitter so that it will be treated as a Singleton.
and some convenience methods
"""

import os
import time

import wx

import ivonet

try:
    DEBUG = os.environ["DEBUG"]
except KeyError:
    DEBUG = False


def dbg(*args):
    """Emit a 'debug' event convenience method"""
    if DEBUG:
        msg = " ".join([str(x) for x in args])
        with open(ivonet.LOG_FILE, "a") as fo:
            fo.write(msg + "\n")
        if len(msg) > 750:
            msg = msg[:750] + "..."
        wx.LogMessage("{timestamp} [DEBUG] {message}".format(timestamp=time.strftime('%X'), message=msg))


def log(*args):
    """Emit a 'log' event convenience method"""
    message = " ".join([str(x) for x in args])
    wx.LogMessage("{timestamp} - {message}".format(timestamp=time.strftime('%X'), message=message))


__all__ = [
    "dbg",
    "log",
]
