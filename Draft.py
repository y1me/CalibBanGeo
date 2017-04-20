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

Head.updateName()
Head.updateBattData()
print Head.getPortName()
print Head.getName()
	        
Head.updateBattData()
print Head.getTempBatt()
print Head.getVoltBatt()
print str(Head.getTempBattRaw())
print str(Head.getVoltBattRaw())
