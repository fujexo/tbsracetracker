"""
Tests for `tbsracetracker` module.
"""

from tbsracetracker.tbsracetracker import tbstracker

tracker = tbstracker('00:00:00:00:00:00')


# Pytest
def test_encode_value():
    assert tracker._encode_value('t') == b't'


def test_decode_value():
    assert tracker._decode_value(b't') == 't'
