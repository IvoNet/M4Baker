#!/usr/bin/env python
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 13:24:39$"
__copyright__ = "Copyright (c) 2004 - 2021 Ivo Woltring"
__license__ = "Python"
__doc__ = """
"""
__history__ = """
2021-02-28
- Upgraded to Python 3
2004-11-14
- added replace methods

"""

from ConfigParser import ConfigParser, DEFAULTSECT


class IniFile(ConfigParser):
    """IniFile
    Is an extention on the ConfigParser class.
    It overrulles the write method so it can write directly to a file provided as
    a parameter. The whole filehandling is done by the IniFile.write(fp) method.
    """

    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults)  # supers init
        self.replace = [('&lbrack;', '['),
                        ('&rbrack;', ']'),
                        ]

    def write(self, fp: str):
        """write(filename)
        this write method just needs a filename as a string to write the config file
        the super method needs a file object.
        """
        with open(fp, 'w') as fo:
            self._write(fo)

    def set_replace(self, input_set, append=True):
        """input_set_replace(input_set, [append=True]) --> Add | Replace the replace options
        input_set must be a list of tuples like: [(source, target),(source, target),...] otherwise
        it will fail.
        No error checking as jet.
        """
        if append:
            [self.replace.append(x) for x in input_set]
        else:
            self.replace = input_set

    def _replace(self, txt, reverse=False):
        """Replace the self.replace stuff
        """
        for source, target in self.replace:
            if reverse:
                txt = txt.replace(target, source)
            else:
                txt = txt.replace(source, target)
        return txt

    def get(self, section, option, raw=False, variables=None):  # override the get() method of super
        """get(section, option, [raw=False], [variablesvariables=None]) --> String
        this get() is an extension on the original ConfigParser.get()
        This one translates html style '&lbrack;' to '[' etc.
        """
        if raw:
            return ConfigParser.get(self, section, option, raw, variables)  # call the get of super
        return self._replace(ConfigParser.get(self, section, option, raw, variables))

    def _write(self, fp):
        """Write an .ini-format representation of the configuration state.
        This one overrulles the superclass write() function.
        """
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s = %s\n" %
                         (key, self._replace(str(value).replace('\n', '\n\t'), reverse=True)))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key != "__name__":
                    fp.write("%s = %s\n" %
                             (key, self._replace(str(value).replace('\n', '\n\t'), reverse=True)))
            fp.write("\n")


if __name__ == "__main__":
    import sys
    import os

    p = IniFile()
    p.add_section('section')
    p.set('section', 'option', '[Ivo Woltring&rbrack;')

    print(p.get('section', 'option'))
    print(p.get('section', 'option', raw=True))
    additional_replace = (('Ivo', 'Sir'),
                          ('Woltring', 'HasFun'),
                          )
    p.set_replace(additional_replace)
    print(p.get('section', 'option'))
    print(p.get('section', 'option', raw=True))

    p.set_replace(additional_replace, append=False)
    print(p.get('section', 'option'))
    print(p.get('section', 'option', raw=True))

    p.write('{0}.ini'.format(os.path.splitext(sys.argv[0])[0]))

    input('Press enter to continue...')
