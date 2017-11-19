#!bin/env python3

import bluepy
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
    def reset(self):
        self._device.writeCharacteristic(0x0025, str.encode('Y'))

    """ read value from tracker
    """
    def _get_value(self, value):
        self._device.writeCharacteristic(0x0025, value)
        sleep(1)
        return self._device.readCharacteristic(0x0028)

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

    """ return the mode
    """
    def get_mode(self):
        return self._get_value(b'M')

    """ Return rounds of the pilots
    """
    def get_rounds(self, pilots=8):
        if pilots > 8:
            raise ValueError('Maximum 8 pilots are possible')
            return False

        rounds = []
        for round in range(0, pilots):
            rounds.append(self._get_value(str.encode('R %i' % round)))

        return rounds

    """ Return channel stuff
    """
    def get_channel(self):
        channels = []
        for channel in range(0,10):
            channels.append(self._get_value(str.encode('N %i' % channel)))
        return channels

    def __init__(self, address):
        self._device = bluepy.btle.Peripheral()
        self.address = address

        self._connect()

