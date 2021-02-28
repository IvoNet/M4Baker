__author__ = "Ivo Woltring"
__version__ = "$version: 00.01$"
__revised__ = "$revised: 2004-11-16 11:03:07$"
__copyright__ = "Copyright (c) 2004 Ivo Woltring"
__license__ = "Python"
__doc__ = """
"""
__history__ = """
"""

import fnmatch
import os


def dir_walk(directory_name):
    """walk a directory tree, using a generator"""
    for f in os.listdir(directory_name):
        fullpath = os.path.join(directory_name, f)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            for x in dir_walk(fullpath):  # recurse into subdir
                yield x
        else:
            yield fullpath


def walk2(root, pattern='*', recurse=True, return_folders=False):
    """See walk, but the order of kwargs is different"""
    return walk(root, recurse, pattern, return_folders)


def walk(root, recurse=True, pattern='*', return_folders=False):
    """walk( root, recurse=True, pattern='*', return_folders=False)
    root     = start directory
    recurse  = if you want to enter sub directories (default = True)
    pattern  = fnmatch like pattern more patterns are possible separated by semicolon
               (e.g. '*.txt;*.log')
    return_folders = return folder names in the list or only filenames
    """

    # initialize
    result = []

    # must have at least root folder
    try:
        names = os.listdir(root)
    except os.error:
        return result

    # expand pattern
    pattern = pattern or '*'
    pat_list = pattern.split(';')

    # check each file
    for name in names:
        fullname = os.path.normpath(os.path.join(root, name))

        # grab if it matches our pattern and entry type
        for pat in pat_list:
            if fnmatch.fnmatch(name, pat) and (
                    os.path.isfile(fullname) or (return_folders and os.path.isdir(fullname))):
                result.append(fullname)

        # recursively scan other folders, appending results
        if recurse and os.path.isdir(fullname) and not os.path.islink(fullname):
            result = result + walk(fullname, recurse, pattern, return_folders)

    return result


def ex_walk(root, exclude=None, recurse=True, include='*', return_folders=False):
    """ex_walk(root,exclude=None,recurse=True,,include='*'return_folders=False)
    Extended Walk... It makes it possible to exclude certain patterns
    root     = start directory
    recurse  = if you want to enter subdirs (default = True)
    include  = fnmatch like pattern more patterns are possible separated by
               semicolon (e.g. '*.txt;*.log')
    exclude  = fnmatch like pattern to exclude (e.g. '*[!zip];*.nfo')
               Note: the negative form is preferred (like *[!zip]) because it is
               much more efficient
    return_folders = return folder names in the list or only filenames
    """
    # expand pattern
    exclude = exclude or None
    pat_list = exclude.split(';')

    if not exclude:
        return walk(root, recurse, include, return_folders)
    files = walk(root, recurse, include, return_folders)

    import re
    for pat in pat_list:
        if re.findall('[!.+]', pat):  # [!zip] or somesuch
            # if '!' in pat and '[' in pat and ']' in pat:
            ret = fnmatch.filter(files, pat)
        else:
            fdel = walk(root, recurse, pat, return_folders)
            ret = []
            for f in files:
                if f not in fdel:
                    ret.append(f)
        files = ret
    return files


if __name__ == '__main__':
    print(ex_walk(r'D:\RARFiles', '*[!r??]'))

    """
    print walk('/IvoNet',True,'*.py;*.pyw',False)
       # test code walk
    print '\nExample 1:'
    files = walk('\\', 1, '*', 1)
    print 'There are %s files below current location:' % len(files)
    for file in files:
        print file

    print '\nExample 2:'
    files = walk('.', 1, '*.py;*.html')
    print 'There are %s files below current location:' % len(files)
    for file in files:
        print file

    #dir_walk test
    for elem in dir_walk('..'):
        print elem
    """
