# python-tbstracker

This python3 module is used to read various information from a TBS Race Tracker

## Usage

``` python
from tbstracker.tbstracker import tbstracker

# Connection to the tracker
b = tbstracker('FF:FF:FF:FF:FF:FF')

# Get the name and battery status
b.get_name()
b.get_battery()
```
