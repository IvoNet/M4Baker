#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 14/03/2021 13:56$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import json
import subprocess
from io import StringIO

import ivonet
from ivonet.events import dbg


def checksum(filename) -> str:
    keep_going = True
    cmd = [
        ivonet.APP_FFPROBE,
        f"{filename}"
    ]

    process = shell_command(cmd)

    ret = None
    while keep_going:
        try:
            line = process.stdout.readline()
        except UnicodeDecodeError:
            #  just skip a line
            continue
        dbg(line)
        if not line:
            dbg(f"No more input from subprocess")
            keep_going = False
            break
        # print(line)
        if "checksum == " in line:
            ret = line.split("== ")[1]
    process.stdout.close()
    if process.returncode != 0 and keep_going:
        raise IOError("Could not retrieve checksum")
    return ret.strip()


def metadata(filename) -> dict:
    output = subprocess.getoutput(f'{ivonet.APP_FFPROBE} -print_format json -show_format -v quiet "{filename}"')
    return json.load(StringIO(output))


def shell_command(cmd):
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        universal_newlines=True,
    )
    process.stdin.close()
    return process
