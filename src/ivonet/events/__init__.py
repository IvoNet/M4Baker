#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import os

from ivonet.events.EventEmitter import EventEmitter
from ivonet.events.defines import *

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


def log(*args):
    """Emit a 'log' event convenience method"""
    ee.emit("log", *args)


__all__ = [
    "ee",
    "_",
    "log",
    "REGISTERED_EVENTS"
]
