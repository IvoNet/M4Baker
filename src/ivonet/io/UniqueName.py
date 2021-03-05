#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 05/03/2021 13:25$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import os


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        input -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, input, message):
        self.input = input
        self.message = message


class OnSizeError(Error):
    """Exception raised for errors in the input.

    Attributes:
        input -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, input, message):
        self.input = input
        self.message = message


def unique_name(fn, max=1000, ldelim='(', rdelim=')'):
    """unique_name(fn, max) -> unique_name string
    fn = is the wanted filename with the destination
    if fn is unique it will be returned as is
    if not unique it will be made unique according to the following rule:
       - extentions must be maintained
       - path\\filename[count].ext where [count] will make the file unique
       - raises an error if the path does not exist
    max = the maximum occurrence of the same filename allowed.
          if max=None there is no limmit. Be careful for endless loop here.
    (l/r)delim = defines the brackets around count
    """
    if not ldelim:
        ldelim = ''
    if not rdelim:
        rdelim = ''
    pad = os.path.split(fn)[0]
    if pad and not os.path.isdir(pad):
        raise InputError(fn, "The path to the file does not exist. Can't make filename unique")
    if not os.path.isfile(fn):  # file does not exist so is unique (yet)
        return fn
    fi, ext = os.path.splitext(fn)
    count = 0
    while 1:
        count += 1
        fo = "%s%s%s%s%s" % (fi, ldelim, count, rdelim, ext)
        if not os.path.isfile(fo):
            return fo
        if not max:
            continue
        if count >= max:
            raise OnSizeError(fn, "Maximum count (%s) for filename has been reached." % max)


if __name__ == "__main__":
    # Test 1
    try:
        raise InputError('pad', 'bestaat niet')
    except InputError as msg:
        print(msg.input)
        print(msg.message)

    # test 2: filepath does not exist
    try:
        print(unique_name('./blablalbalba/filenotexiste.txt'))
    except InputError as e:
        print(e.message)

    # test 3: File does not exist so is returned as unique
    print(unique_name('./Uniquenamefoundereondisc.txt'))

    # test 4: File does exist and must be made unique
    os.mkdir('UniqueTest')
    fns = ['test.txt',
           'test[1].txt',
           'test[2].txt',
           'test[3].txt',
           'test[4].txt',
           'test[5].txt',
           'test',
           ]
    for f in fns:
        open('UniqueTest/' + f, 'w').write(f)

    print(unique_name('UniqueTest/test.txt'))

    # test 5: OnSizeError
    try:
        print(unique_name('UniqueTest/test.txt', max=3))
    except OnSizeError as e:
        print(e.message)

    # test 6: Geen extentie op filename
    print(unique_name('UniqueTest/test'))

    # Cleaning up
    os.system('rm -rf UniqueTest')
