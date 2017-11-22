# -*- coding: UTF-8  -*-
"""
Tests for `tbsracetracker` module.
"""
import pytest
from mock import MagicMock

import bluepy
from tbsracetracker.tbsracetracker import tbstracker


@pytest.fixture
def tracker():
    return tbstracker('00:00:00:00:00:00')


def test_connect(monkeypatch, tracker):
    # Patch the bluepy Peripheral connect function because there is no
    # actual bluetooth LE device.
    monkeypatch.setattr(bluepy.btle.Peripheral, 'connect',
                        MagicMock(bluepy.btle.Peripheral))

    # Patch the _connected function to return True because we can
    # not connect to an actual device
    monkeypatch.setattr(tbstracker, '_connected', MagicMock(tbstracker))
    rt = tbstracker
    rt._connected.return_value = True

    assert tracker.connect()


def test_connected(monkeypatch, tracker):
    # Patch the bluepy Peripheral status function because there is no
    # actual bluetooth LE device.
    monkeypatch.setattr(bluepy.btle.Peripheral, 'status',
                        MagicMock(bluepy.btle.Peripheral))
    rt = bluepy.btle.Peripheral
    rt.status.return_value = {'dst': ['00:00:00:00:00:00'],
                              'mtu': [0],
                              'rsp': ['stat'],
                              'sec': ['low'],
                              'state': ['conn']}

    assert tracker._connected()


def test_connected_nobluetooth(monkeypatch, tracker):
    assert not tracker._connected()


def test_encode_value(tracker):
    assert tracker._encode_value('t') == b't'


def test_decode_value(tracker):
    assert tracker._decode_value(b't') == 't'


@pytest.mark.parametrize("string, expected", [
    ("test 123 \x00 12", ['123', '12']),
    ("123.256.123aybay", ['123', '256', '123']),
])
def test_find_re_number(tracker, string, expected):
    assert tracker._find_re_number(string) == expected


@pytest.mark.parametrize("string, expected", [
    ("test 123 \x00 12", ['test', '123', '12']),
    ("123.256.123aybay", ['123', '256', '123aybay']),
])
def test_find_re_word(tracker, string, expected):
    assert tracker._find_re_word(string) == expected


@pytest.mark.parametrize("address, value, expected", [
    (0x0025, 'B', b'B'),
    (0x0025, 'N', b'N'),
])
def test_write_char(tracker, monkeypatch, address, value, expected):
    mock_device = []
    monkeypatch.setattr(bluepy.btle.Peripheral, 'writeCharacteristic',
                        MagicMock(bluepy.btle.Peripheral))
    rt = bluepy.btle.Peripheral
    rt.writeCharacteristic = lambda o, a, v: mock_device.append((a, v))

    tracker._write_char(address, value)

    assert mock_device[0][0] == address
    assert mock_device[0][1] == expected
