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

import re
import bluepy
import codecs
from time import sleep


class tbstracker:
    """TBSRTracker class."""

    def __init__(self, address):
        """Initialize"""
        self._device = bluepy.btle.Peripheral()
        self.address = address

    def _encode_value(self, value):
        """encode a given value

        :return: Bytes
        """
        return codecs.encode(value, encoding='utf-8')

    def _decode_value(self, value):
        """decode a given value

        :return: String
        """
        return codecs.decode(value, encoding='utf-8', errors='ignore')

    def _connected(self):
        """Check if we are connected

        :return: Boolean
        """
        if self._device.status()['state'][0] == 'conn':
            return True
        else:
            return False

    def _write_char(self, address, value):
        """write value to address on device

        :return: None
        """
        self._device.writeCharacteristic(address, self._encode_value(value))

    def _read_char(self, address):
        """read value from address on device

        :return: str
        """
        return self._decode_value(self._device.readCharacteristic(address))

    def _write_read_tracker(self, value):
        """write value to device and read the returned data"""
        self._write_char(0x0025, value)
        sleep(1)
        return self._read_char(0x0028)

    def connect(self):
        """Connect to tracker device.

        :return: Boolean
        """
        self._device.connect(self.address)
        return self._connected()

    def disconnect(self):
        """Disconnect from tracker device."""
        self._device.disconnect()

    def reset_tracker(self):
        """ Reset the tracker configuration."""
        self._write_char('Y')

    # Different values of the tracker
    def get_firmware(self):
        """read the firmware version of the tracker."""
        return self._read_char(0x0018)

    def get_name(self):
        """read the name of the tracker"""
        return self._read_char(0x0003)

    def get_manufacturer(self):
        """read the manufacturer of the tracker"""
        return self._read_char(0x001e)

    def get_battery(self):
        """read the battery state of the tracker"""
        return self._write_read_tracker('B')

    def _find_re_number(self, string):
        """find numbers in string"""
        return re.findall(r'\d+', string)

    def _find_re_word(self, string):
        """find words in string"""
        return re.findall(r'\w+', string)

    # Get configurations
    def get_config_mode(self):
        """read thte mode from tracker"""
        return self._find_re_number(self._write_read_tracker('M'))[0]

    def get_config_pilots(self):
        """read how many pilots are configured"""
        return self._find_re_number(self._write_read_tracker('N'))[0]

    def get_config_laps(self):
        """read how many laps are configured"""
        return self._find_re_number(self._write_read_tracker('Z 2'))[1]

    def get_config_min_laptime(self):
        """read the minimum time for each lap"""
        return self._find_re_number(self._write_read_tracker('Z 6'))[1]

    # Set configurations
    def set_config_pilot(self, number, channel):
        """configure a pilot"""
        if re.findall(r'(\w\w)',
                      self._write_read_tracker('N %i %s' % (number, channel)
                                               ))[0] == channel:
            return True
        else:
            return False

    # Start and stop races
    def start_flyover(self):
        """Start Race in Flyover mode"""
        return self._find_re_word(self._write_read_tracker('2'))[0]

    def start_shotgun(self):
        """Start Race in Shotgun mode"""
        return self._find_re_word(self._write_read_tracker('1'))[0]

    def stop_race(self):
        """Stop a Race"""
        return self._find_re_word(self._write_read_tracker('0'))[0]

    def get_signal_strenght(self):
        """Get Signal strenght of the first pilot"""
        return self._write_read_tracker('Q').replace('\x00', '').split(',')

    # Statistics
    def running_race(self):
        """Read the tracker while a race is running"""
        running = True
        previous = ''
        race_stats = []
        # Format: PlayerRound, lap time, total time

        while running is not False:
            playerstats = []
            sleep(1)
            r = codecs.decode(self._device.readCharacteristic(0x0028),
                              encoding='utf-8', errors='ignore')
            if 'RACE COMPLETE' in r:
                running = False
            if not r == previous:
                if re.findall(r'^(STARTED|READY|RACE COMPLETE)', r):
                    print(re.findall(r'^(STARTED|READY|RACE COMPLETE)', r)[0])
                if re.search(r'^P\dR\d', r):
                    for item in re.search(r'(^P\dR\d)T(\d+),(\d+)',
                                          r).groups():
                        playerstats.append(item)
                    race_stats.append(playerstats)
                    print(','.join(playerstats))
                previous = r

        print(race_stats)

    def get_total_rounds(self):
        """Read the total flown rounds"""
        return self._write_read_tracker('R')

    def get_rounds(self, pilots=8):
        """Return rounds of the pilots"""
        if pilots > 8:
            raise ValueError('Maximum 8 pilots are possible')
            return False

        rounds = []
        for round in range(0, pilots):
            rounds.append(self._write_read_tracker('R %i'
                                                   % round).decode("utf-8",
                                                                   "strict"))

        return rounds

    def get_channel(self):
        """Return channel stuff"""
        channels = []
        for channel in range(0, 10):
            channels.append(self._write_read_tracker('N %i' % channel))
        return channels

    def get_z(self):
        """Return z stuff"""
        zs = []
        for z in range(0, 33):
            zs.append(self._write_read_tracker('Z %i' % z))
        return zs
