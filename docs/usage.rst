=====
Usage
=====

To use tbsracetracker in a project

.. code-block:: py

   from tbracestracker.tbsracetracker import tbstracker

   # Connection to the tracker
   b = tbstracker('FF:FF:FF:FF:FF:FF')

   # Get the name and battery status
   b.get_name()
   b.get_battery()
