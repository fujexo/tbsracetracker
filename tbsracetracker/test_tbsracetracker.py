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
