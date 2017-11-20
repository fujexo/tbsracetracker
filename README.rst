=============================
tbsracetracker
=============================

.. image:: https://travis-ci.org/fujexo/tbsracetracker.png?branch=master
    :target: https://travis-ci.org/fujexo/tbsracetracker

.. image:: https://codecov.io/gh/fujexo/tbsracetracker/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/fujexo/tbsracetracker

This python module allows to read/write different values on a TBS Race Tracker.

You can find an example for running a race in `race.py`.

Implemented Features
--------------------

- Connect/Disconnect Tracker
- Start/Stop Race (Flyover and Shotgun)
- Configure pilots (add, update, remove)
- Read device information

  - Firmware version
  - Device name
  - Manufacturer
  - Battery status
  - Configured Laps
  - Configured Min Lap Time
  - How Pilots are configured
  - Signal strenght of first pilot
  - Total Rounds / Rounds per Pilot
  - Some other information

- Reset Tracker

Missing Features
----------------

- Configure Min/Max Laptime
- Configure Max Laps
- Calibrate tracker
