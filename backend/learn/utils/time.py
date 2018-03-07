"""Utils for working with (UTC) time.
"""
from django.utils import timezone

def utc(year, month, day, hour=0, minute=0, second=0):
    return timezone.datetime(
        year, month, day, hour, minute, second,
        tzinfo=timezone.utc)


def time(hour, minute, second=0):
    """Convient creating datetime objects for testing and simulations.
    """
    return utc(2018, 2, 1, hour, minute, second)


def hm(string):
    hour, minute = map(int, string.split(':'))
    return time(hour, minute, second=0)


def ms(string):
    minute, second = map(int, string.split(':'))
    return utc(2018, 2, 1, 8, minute, second)
