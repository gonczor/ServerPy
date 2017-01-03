from unittest import TestCase


class SomeTestCase(TestCase):
    def test_simple(self):
        self.assertAlmostEqual(2+2, 4)
        print('another simple test case')
