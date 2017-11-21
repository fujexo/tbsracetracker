#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# tbsracetracker - Control your TBS Race Tracker using Python!
# Copyright (C) 2017 Philipp Marmet
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from bluepy.btle import Scanner, DefaultDelegate

scan_delegate = DefaultDelegate()

scanner = Scanner().withDelegate(scan_delegate)
devices = scanner.scan(10.0)

tbs_trackers = {}

for dev in devices:
    for data in dev.getScanData():
        if 'TBSRT' in data[2]:
            name = data[2].replace('\x00', '')
            tbs_trackers[name] = {'addr': dev.addr, 'rssi': dev.rssi}

for item in tbs_trackers:
    addr = tbs_trackers.get(item).get('addr')
    rssi = tbs_trackers.get(item).get('rssi')
    print('Name: %s, Address: %s, RSSI: %s' % (item, addr, rssi))
