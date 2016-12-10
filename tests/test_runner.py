import unittest

from tests.NetworkTests.AuthenticationTests import AuthenticationTestCase

r = unittest.TestResult()
loader = unittest.TestLoader()
test_suite = unittest.TestSuite()
test_suite = loader.loadTestsFromTestCase(AuthenticationTestCase)
print(test_suite.countTestCases())
test_suite.run(r)

unittest.main()
