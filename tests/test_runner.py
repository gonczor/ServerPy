import unittest

from . import testcases


def run():
    s = unittest.defaultTestLoader.loadTestsFromModule(testcases)
    unittest.TextTestRunner().run(s)
