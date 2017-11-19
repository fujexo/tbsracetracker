#!bin/env python3

import re
import bluepy
import codecs
from time import sleep
from string import ascii_uppercase

class tbstracker:

    """ Connect to device
    """
    def _connect(self):
        self._device.connect(self.address)

    """ Disconnect from device
    """
    def disconnect(self):
        self._device.disconnect()

    """ Reset the tracker configuration
    """
    def reset_tracker(self):
        self._device.writeCharacteristic(0x0025, codecs.encode('Y', encoding='utf-8'))

    """ read value from tracker
    """
    def _get_value(self, value):
        self._device.writeCharacteristic(0x0025, codecs.encode(value, encoding='utf-8'))
        sleep(1)
        return codecs.decode(self._device.readCharacteristic(0x0028), encoding='utf-8', errors='ignore')


    # Different values of the tracker
    """ read the firmware version of the tracker
    """
    def get_firmware(self):
        return self._device.readCharacteristic(0x0018)

    """ read the name of the tracker
    """
    def get_name(self):
        return self._device.readCharacteristic(0x0003)

    """ read the manufacturer of the tracker
    """
    def get_manufacturer(self):
        return self._device.readCharacteristic(0x001e)

    """ read the battery state of the tracker
    """
    def get_battery(self):
        return self._get_value(b'B')

    def _find_re_number(self, string):
        return re.findall(r'\d+', string)

    def _find_re_word(self, string):
        return re.findall(r'\w+', string)


    # Get configurations
    def get_config_mode(self):
        return self._find_re_number(self._get_value('M'))[0]

    def get_config_pilots(self):
        return self._find_re_number(self._get_value('N'))[0]

    def get_config_laps(self):
        return self._find_re_number(self._get_value('Z 2'))[1]

    def get_config_min_laptime(self):
        return self._find_re_number(self._get_value('Z 6'))[1]



    # Set configurations
    def set_config_pilot(self, number, channel):
        if re.findall(r'(\w\w)', self._get_value('N %i %s' % (number, channel)))[0] == channel:
            return True
        else:
            return False



    # Start and stop races
    def start_flyover(self):
        return self._find_re_word(self._get_value('2'))[0]

    def start_shotgun(self):
        return self._find_re_word(self._get_value('1'))[0]

    def stop_race(self):
        return self._find_re_word(self._get_value('0'))[0]

    def get_signal_strenght(self):
        return self._get_value('Q').replace('\x00', '').split(',')


    # Statistics
    def running_race(self):
        running = True
        previous = ''
        race_stats = []
        # Format: PlayerRound, lap time, total time

        while running is not False:
            playerstats = []
            sleep(1)
            r = codecs.decode(self._device.readCharacteristic(0x0028), encoding='utf-8', errors='ignore')
            if 'RACE COMPLETE' in r:
                running = False
            if not r == previous:
                if re.findall(r'^(STARTED|READY|RACE COMPLETE)', r):
                    print(re.findall(r'^(STARTED|READY|RACE COMPLETE)', r)[0])
                if re.search(r'^P\dR\d', r):
                    for item in re.search(r'(^P\dR\d)T(\d+),(\d+)', r).groups():
                        playerstats.append(item)
                    race_stats.append(playerstats)
                    print(','.join(playerstats))
                previous = r

        print(race_stats)


    def get_total_rounds(self):
        return self._get_value('R')

    """ Return rounds of the pilots
    """
    def get_rounds(self, pilots=8):
        if pilots > 8:
            raise ValueError('Maximum 8 pilots are possible')
            return False

        rounds = []
        for round in range(0, pilots):
            rounds.append(self._get_value('R %i' % round).decode("utf-8", "strict"))

        return rounds

    """ Return channel stuff
    """
    def get_channel(self):
        channels = []
        for channel in range(0,10):
            channels.append(self._get_value('N %i' % channel))
        return channels

    """ Return z stuff
    """
    def get_z(self):
        zs = []
        for z in range(0,33):
            zs.append(self._get_value('Z %i' % z))
        return zs


    def dbg(self, value):
        return self._get_value(value)


    def __init__(self, address):
        self._device = bluepy.btle.Peripheral()
        self.address = address

        self._connect()

