import tests.NetworkTests.AuthenticationTests
import tests.NetworkTests.BannedAdressCacheTests
import unittest


def run():
    s = unittest.defaultTestLoader.loadTestsFromModule(tests.NetworkTests.AuthenticationTests.AuthenticationTestCase)
    unittest.TextTestRunner().run(s)
    s = unittest.defaultTestLoader.loadTestsFromTestCase(tests.NetworkTests.BannedAdressCacheTests.BannedAdressCacheTestCase)
    unittest.TextTestRunner().run(s)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromModule(tests.NetworkTests)
    unittest.TextTestRunner().run(suite)
