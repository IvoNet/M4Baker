__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 15:27:27$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import os
import unittest

from ivonet import data_directory


class ApplicationTests(unittest.TestCase):
    def test_valid_data_directory(self):
        self.assertTrue(os.path.split(data_directory("M4Baker"))[1] == "M4Baker")
        self.assertTrue(os.path.split(data_directory("FooBarBaz is a long name"))[1] == "FooBarBaz is a long name")
        self.assertTrue("Library" in data_directory("NotImportant"))


if __name__ == '__main__':
    unittest.main()
