# -*- coding: UTF-8  -*-
"""
Tests for `tbsracetracker` module.
"""
import pytest
from mock import MagicMock

import bluepy
from tbsracetracker.tbsracetracker import tbstracker


class TestTracker():

    @pytest.fixture(autouse=True)
    def setup_tracker_device(self):
        self.tracker = tbstracker('00:00:00:00:00:00')

    def test_connect(self, monkeypatch):
        # Patch the bluepy Peripheral connect function because there is no
        # actual bluetooth LE device.
        monkeypatch.setattr(bluepy.btle.Peripheral, 'connect',
                            MagicMock(bluepy.btle.Peripheral))

        # Patch the _connected function to return True because we can
        # not connect to an actual device
        monkeypatch.setattr(tbstracker, '_connected', MagicMock(tbstracker))
        rt = tbstracker
        rt._connected.return_value = True

        assert(self.tracker.connect() is True)

    def test_connected(self, monkeypatch):
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

        assert(self.tracker._connected() is True)

    def test_encode_value(self):
        assert self.tracker._encode_value('t') == b't'

    def test_decode_value(self):
        assert self.tracker._decode_value(b't') == 't'
