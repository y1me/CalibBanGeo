#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Head calibration.

"""

import sys
import curses
import traceback
import time
import subprocess
import re
from tempfile import mkstemp
from shutil import move
from os import remove, close


def restore_terminal():
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

def servo_pos(position, subpad):
    time.sleep(1)

def servo_delay():
    time.sleep(1)

import ConfigParser, os

mode_select = 0
cursor_x = [2, 21, 41, 53]
cursor_y = [3, 3, 3, 5]

low_pos = 10
high_pos = 10
delay = 10

#subprocess.Popen(['sudo', 'mobikill.sh']).communicate()
time.sleep(1)

stdscr = curses.initscr()
try:
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.nodelay(1)
    curses.nonl()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    stdscr.refresh()
    pad = curses.newpad(20, 56)
    lowpos_pad = pad.subpad(1,10, 3,2)
    highpos_pad = pad.subpad(1,10, 3,21)
    delay_pad = pad.subpad(1,10, 3,41)

    pad.box()
    pad.addstr(0, 16, "Servomotor calibration", curses.color_pair(1))
    pad.addstr(2, 2, "Low position", curses.A_BOLD)
    pad.addstr(3, 2, str(low_pos))
    pad.addstr(2, 21, "High position", curses.A_BOLD)
    pad.addstr(3, 21, str(high_pos))
    pad.addstr(2, 41, "Delay setting", curses.A_BOLD)
    pad.addstr(3, 41, str(delay))
    pad.addstr(19, 38, "Save and exit [X]", curses.A_BOLD)
    pad.refresh(0,0, 1,1, 30,57)

    while True:
        pad.move(cursor_y[mode_select], cursor_x[mode_select])
        pad.refresh(0,0, 1,1, 7,57)
        low_pos += 1
        time.sleep(0.2)
        if low_pos >= 200000:
            low_pos = 0
        lowpos_pad.addstr(0, 0, str(low_pos))
        delay_pad.clrtoeol()
        pad.refresh(0,0, 1,1, 7,57)
        # Wait for key press.

        c = stdscr.getch()
        
        if c == curses.KEY_UP:
            if mode_select == 0:
                low_pos += 20
                servo_pos(low_pos, lowpos_pad)
            elif mode_select == 1:
                high_pos += 20
                servo_pos(high_pos, highpos_pad)
            elif mode_select == 2:
                delay += 50
                delay_pad.addstr(0, 0, str(delay))
                delay_pad.clrtoeol()
                pad.refresh(0,0, 1,1, 7,57)
        elif c == curses.KEY_DOWN:
            if mode_select == 0:
                low_pos -= 20
                servo_pos(low_pos, lowpos_pad)
            elif mode_select == 1:
                high_pos -= 20
                servo_pos(high_pos, highpos_pad)
            elif mode_select == 2:
                delay -= 50
                delay_pad.addstr(0, 0, str(delay))
                delay_pad.clrtoeol()
                pad.refresh(0,0, 1,1, 7,57)
        elif c == curses.KEY_RIGHT:
            mode_select += 1
            mode_select = mode_select%4
        elif c == curses.KEY_LEFT:
            mode_select -= 1
            mode_select = mode_select%4
        elif c == 13: #ENTER KEY
            if mode_select == 3:
                restore_terminal()
                #subprocess.call(["setup-openbts-db.sh"])
                break
            else:
                servo_delay()

except KeyboardInterrupt:
    restore_terminal()
    sys.exit(1)

except Exception as e:
    # In event of error, restore terminal to sane state.
    restore_terminal()
    if isinstance(e, SystemExit):
        raise
    traceback.print_exc()    # Print the exception

restore_terminal()
sys.exit(0)

