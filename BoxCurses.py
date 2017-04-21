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

def restore_terminal():
	stdscr.keypad(0)
	curses.echo()
	curses.nocbreak()
	curses.endwin()

def write_value(key,data):

        if key < 2:
            value_pad[key].addstr(0, 0, data, curses.color_pair(3))
        elif key in [ 2, 3 ]:
            value_pad[key].addstr(0, 0, data, curses.color_pair(5))
        elif (key)%4 == 0:
            value_pad[key].addstr(0, 0, data, curses.color_pair(5))
        else:
            value_pad[key].addstr(0, 0, data, curses.color_pair(1))
        value_pad[key].clrtoeol()

def comb_amplifier():
        time.sleep(0.2)

def single_spike():
        time.sleep(0.2)

def set_SX(SX_key):
        time.sleep(0.2)

def SX_on_off(key):
        time.sleep(0.2)

def change_freq(SX, key, freq):
        time.sleep(0.2)

#dictionnary declarations
title 	= ['Device Name', 'Port', 'Battery Voltage', 'Battery Temperature', 
			'Sensor 0 Value', 'S0 Zero', 'S0 Low value', 'S0 High Value',
			'Sensor 1 Value', 'S1 Zero', 'S1 Low value', 'S1 High Value',
			'Sensor 2 Value', 'S2 Zero', 'S2 Low value', 'S2 High Value',
			'Sensor 3 Value', 'S3 Zero', 'S3 Low value', 'S3 High Value']

Head = Devices.Devices("/dev/rfcomm0","test")

value_pad = [0]*20

x, y, len_x, len_y= 1, 1, 4, 5
cursor_x = [(2+18*e) for e in range(len_x)]
cursor_y = [(3+2*e) for e in range(len_y)]
LENGTH = 3+2*len_y
WIDTH = 3+18*len_x
PAD_MIN = 1
PAD_MAX = 15

dec = 0
LOOP = 50

if __name__ == "__main__":
	try:
		stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		stdscr.keypad(1)
		stdscr.nodelay(1)
		curses.nonl()
		curses.start_color()
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_RED, curses.COLOR_GREEN)
		curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
		curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(8, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
		curses.init_pair(9, curses.COLOR_BLUE, curses.COLOR_WHITE)
		curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_WHITE)
		stdscr.refresh()
		pad = curses.newpad(LENGTH, WIDTH+2)

		pad.box()
		pad.addstr(0, 1, "Device Sensor Calibration", curses.color_pair(1))

		for i in range(len_y):
			for j in range(len_x):
				pad.addstr(cursor_y[i]-1, cursor_x[j], title[len_x*i+j], curses.A_BOLD)
				value_pad[len_x*i+j] = pad.subpad(PAD_MIN, PAD_MAX, cursor_y[i],cursor_x[j])
                                if len_x*i+j < 2:
				    value_pad[len_x*i+j].addstr(0, 0, "AT", curses.color_pair(3))
                                elif len_x*i+j in [ 2, 3 ]:
				    value_pad[len_x*i+j].addstr(0, 0, "AT", curses.color_pair(5))
				elif (len_x*i+j)%4 == 0:
				    value_pad[len_x*i+j].addstr(0, 0, "AT", curses.color_pair(5))
				else:
				    value_pad[len_x*i+j].addstr(0, 0, "AT", curses.color_pair(1))

		pad.addstr(LENGTH-1, 1, "Use arrows to navigate, +/- to increase/decrease value, Enter to confirm")
		pad.refresh(0,0, 1,1, LENGTH,WIDTH+2)
	
        	write_value(1,Head.getPortName())
        	write_value(0,Head.getName())
	        
		while True:
			pad.move(cursor_y[y], cursor_x[x])
			index = len_x*y + x
			pad.refresh(0,0, 1,1, LENGTH,WIDTH+2)
                        
                        if dec == 1 :
                            batt = Head.getBattStat() 
        	            write_value(3,str(batt[1])+"°C/ "+str(batt[0]))
        	            write_value(2,str(batt[3])+"V/"+str(round((batt[3]/6),2))+"V")
                        if dec == LOOP :
                            dec = 0
                        time.sleep(0.01) 
                        dec += 1
			c = stdscr.getch()
			if c == curses.KEY_UP:
				if y <= 1:
					y = (len_y - 1)
				else:
					y -=1
			elif c == curses.KEY_DOWN:
				if y >= (len_y - 1):
					y = 1
				else:
					y += 1
			elif c == curses.KEY_RIGHT:
				if x >= (len_x - 1):
					x = 1
				else:
					x += 1
			elif c == curses.KEY_LEFT:
				if x <= 1:
					x = (len_x - 1)
				else:
					x -= 1 				
			elif c == 43: # '+' KEY
				if y == 1:
					write_value(index, str(index) )
				elif y == 2:
					write_value(index, str(index) )
				elif y == 3:
					write_value(index, index)
				elif y == 4:
					write_value(index, y)
			elif c == 45: # '-' KEY
				if y == 2:
					write_value(index, str(index))
				elif y == 3:
					write_value(index, str(index))
				elif y == 4:
					write_value(index, str(index))
			elif c == ENTER_KEY:
				if y == 0 and x == 0:
					write_value(index, str(index))
				if y == 0 and x == 1:
					write_value(index, str(index))
				elif y == 1:
					write_value(index, str(index))
				elif y == 2:
					write_value(index, str(index))
				elif y == 3:
					write_value(index, str(index))
				elif y == 4:
					write_value(index, str(index))
	except:
		# In event of error, restore terminal to sane state.
		restore_terminal()
		traceback.print_exc()	# Print the exception

