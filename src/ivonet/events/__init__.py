#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

from ivonet.events.EventEmitter import EventEmitter

ee = EventEmitter()


def _(*args):
    """Emit a 'log' event convenience method"""
    ee.emit("log", *args)


__all__ = [
    "ee",
    "_"
]
