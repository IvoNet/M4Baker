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
    output = subprocess.getoutput(
        f'{ivonet.APP_FFPROBE} -print_format json -show_format -loglevel error -v quiet "{filename}"')
    return json.load(StringIO(output))


def chapters(filename) -> dict:
    output = subprocess.getoutput(
        f'{ivonet.APP_FFPROBE} -print_format json -show_format -show_chapters -loglevel error -v quiet -i "{filename}"')
    return json.load(StringIO(output))


def sexagesimal(dur):
    mills = str(dur).split(".")
    if len(mills) == 2:
        mills = mills[1]
    else:
        mills = "000"
    hours = int(dur / 3600)
    minutes = int((dur - (hours * 3600)) / 60)
    seconds = int(dur - (hours * 3600) - (minutes * 60))
    print(dur, hours, minutes, seconds, mills)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{mills[:3]}"


def duration(filename: str, formatted=False) -> float:
    options = ""
    if formatted:
        options += "-sexagesimal"
    return float(subprocess.getoutput(
        f'{ivonet.APP_FFPROBE} -show_entries format=duration -loglevel error -v quiet -of default=noprint_wrappers=1:nokey=1 {options} -i "{filename}"'))


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


if __name__ == '__main__':
    print(sexagesimal(duration(
        "/Users/iwo16283/Downloads/m4b/000-Rachel Aaron - The Legend of Eli Monpress Omnibus 05 - Spirit's End.mp3")))
