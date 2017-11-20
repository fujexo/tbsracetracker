#!/bin/env python3

from tbstracker.tbstracker import tbstracker

# Get our tracker object
mytracker = tbstracker('F4:5E:AB:B1:6D:5C')

# Tracker stuff
tracker_name = mytracker.get_name()

# Set up configration
for i in range(2,8):
    mytracker.set_config_pilot(i, 'FF')

mytracker.set_config_pilot(1, 'F3')
mytracker.set_config_pilot(2, 'F4')


# Start with informations
print('We configured', mytracker.get_config_laps(), 'laps')
print('The minimal round time is', mytracker.get_config_min_laptime())


# Start the race
print(mytracker.get_signal_strenght())
print('\n')

print(mytracker.start_flyover())
mytracker.running_race()

print('\n\n', mytracker.get_total_rounds())

