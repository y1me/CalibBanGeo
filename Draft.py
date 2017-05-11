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


raw_input("press enter key to continue")
for k in range(12):
    print k
print "end"

