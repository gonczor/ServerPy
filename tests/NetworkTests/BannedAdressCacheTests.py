from unittest import TestCase

import datetime
import contextlib
from mock import mock

from Networking.BannedAddressesCache import BannedAddressesCache


real_datetime_class = datetime.datetime

@contextlib.contextmanager
def mock_now(dt_value):
    """Context manager for mocking out datetime.now() in unit tests.
    Example:
    with mock_now(datetime.datetime(2011, 2, 3, 10, 11)):
        assert datetime.datetime.now() == datetime.datetime(2011, 2, 3, 10, 11)
    """

    class MockDateTime(datetime.datetime):
        @classmethod
        def now(cls):
            # Create a copy of dt_value.
            return datetime.datetime(
                dt_value.year, dt_value.month, dt_value.day,
                dt_value.hour, dt_value.minute, dt_value.second, dt_value.microsecond,
                dt_value.tzinfo
            )
    real_datetime = datetime.datetime
    datetime.datetime = MockDateTime
    try:
        yield datetime.datetime
    finally:
        datetime.datetime = real_datetime


class BannedAdressCacheTestCase(TestCase):
    def setUp(self):
        super(BannedAdressCacheTestCase, self).setUp()
        self.cache = BannedAddressesCache()
        self.address = '127.0.0.1'
        self.ban_timestamp = datetime.datetime(2016, 12, 10, 21, 0, 0)
        self.expected_ban_expiry = self.ban_timestamp + datetime.timedelta(seconds=60)

    def test_correct_withdrawal_is_set(self):
        self.cache.add(self.address)
        self.assertTrue(self.cache.contains(self.address))
        expected_expiry = datetime.datetime.now() + datetime.timedelta(seconds=60)
        self.assertEqual(self.cache._cache[self.address].year, expected_expiry.year)
        self.assertEqual(self.cache._cache[self.address].month, expected_expiry.month)
        self.assertEqual(self.cache._cache[self.address].day, expected_expiry.day)
        self.assertEqual(self.cache._cache[self.address].hour, expected_expiry.hour)
        self.assertEqual(self.cache._cache[self.address].minute, expected_expiry.minute)
        self.assertEqual(self.cache._cache[self.address].second, expected_expiry.second)

    def test_flush_after_withdrawal(self):
        with mock_now(self.ban_timestamp):
            self.cache.add(self.address)

        with mock_now(self.expected_ban_expiry):
            self.assertFalse(self.cache.contains(self.address))



