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

from ivonet.events.EventEmitter import EventEmitter

ee = EventEmitter(wildcard=True)

# Set to False if you do not want the emitted messages shown in stdout
# Should be set to False for prod!

try:
    DEBUG = os.environ["DEBUG"]
except KeyError:
    DEBUG = False


def _(*args):
    """Emit a 'debug' event convenience method"""
    if DEBUG:
        ee.emit("debug", *args)


@ee.on_any
def print_any_event_to_stdout(*args):
    """Prints all message events if DEBUG = True"""
    if DEBUG:
        print(time.strftime('%X'), "[DEBUG]", " ".join([str(x) for x in args]))


def log(*args):
    """Emit a 'log' event convenience method"""
    ee.emit("log", *args)


__all__ = [
    "ee",
    "_",
    "log",
]
