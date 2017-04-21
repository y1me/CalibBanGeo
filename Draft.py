#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Graphical interface to calibrate sensor.

This script is used to calibrate angular sensor

WARNING : a terminal window size of at least 75*15 is required.
"""

import sys
import curses
import traceback
import time
import subprocess
from DevicesAPI import Devices

ENTER_KEY = 13

Head = Devices.Devices("/dev/rfcomm0","test")

print Head.getPortName()
print Head.getName()
print Head.getAnalogIN()
print Head.WriteCalib(':')
print Head.ReadCalib('1')
print Head.ReadCalib('2')
print type(Head.ReadCalib('3'))
