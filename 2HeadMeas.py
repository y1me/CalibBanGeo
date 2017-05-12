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
import argparse
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

#dictionnary declarations
title 	= ['Rien', 'Tete', 'Total', 'Tete', 
			'Parallelisme', 'Valeur', 'Valeur', 'Valeur',
			'Chasse', 'Valeur', 'Rien', 'Valeur',
			'Essieu', 'Valeur', 'Rien', 'Valeur',
			'Assiette', 'Valeur', 'Rien', 'Valeur']

parser = argparse.ArgumentParser(description='2 Head control script')
parser.add_argument('ttyport1',type=str,
                                help='input tty device')
parser.add_argument('ttyport2',type=str,
                                help='input tty device')
args = parser.parse_args()
Head1 = Devices.Devices(args.ttyport1,"test")
Head2 = Devices.Devices(args.ttyport2,"test")

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
STARTADDEEPROM = '0'
k_index = [5,9,13,17,6,10,14,18,7,11,15,19]
print "Script mesure 2 têtes"
print "Initialisation : dévoilage des roues"
print "Positionner les têtes et relier les capteurs"
print ""
print "Dévoilage roue munie de la tête : " + Head1.getName()
print "Réglez l'assiette de la roue munie de : " + Head1.getName()
raw_input("appuyer sur entrée pour continuer")
print ""
print "Mesure en cours...."

a = Head1.getAnalogIN()
refS0 = a[0]
refS1 = a[1]
refS2 = a[2]
refS3 = a[3]
time.sleep(1)
for k in range(6):
    a = Head1.getAnalogIN()
    print "Deviation S0 : " + str(abs(a[0]-refS0))
    if abs(a[0]-refS0) >= 3:
        print "Capteur parallélisme instable"
    print "Deviation S1 : " + str(abs(a[1]-refS1))
    if abs(a[1]-refS1) >= 3:
        print "Capteur carrosage instable"
    print "Deviation S2 : " + str(abs(a[2]-refS2))
    if abs(a[2]-refS2) >= 3:
        print "Capteur alignement essieu instable"
    print "Deviation S3 : " + str(abs(a[3]-refS3))
    if abs(a[3]-refS3) >= 3:
        print "Capteur assiette instable"
    time.sleep(1)
DeltaS = []
DeltaS.append(float(a[0]))
DeltaS.append(float(a[1]))
DeltaS.append(float(a[2]))
DeltaS.append(float(a[3]))
print DeltaS
print ""
print "Tournez d'un demi-tour la roue munie de la tête : " + Head1.getName()
print "Réglez l'assiette de la roue munie de : " + Head1.getName()
raw_input("appuyer sur entrée pour continuer")
a = Head1.getAnalogIN()
refS0 = a[0]
refS1 = a[1]
refS2 = a[2]
refS3 = a[3]
time.sleep(1)
for k in range(6):
    a = Head1.getAnalogIN()
    print "Deviation S0 : " + str(abs(a[0]-refS0))
    if abs(a[0]-refS0) >= 3:
        print "Capteur parallélisme instable"
    print "Deviation S1 : " + str(abs(a[1]-refS1))
    if abs(a[1]-refS1) >= 3:
        print "Capteur carrosage instable"
    print "Deviation S2 : " + str(abs(a[2]-refS2))
    if abs(a[2]-refS2) >= 3:
        print "Capteur alignement essieu instable"
    print "Deviation S3 : " + str(abs(a[3]-refS3))
    if abs(a[3]-refS3) >= 3:
        print "Capteur assiette instable"
    time.sleep(1)
print a
print ""
DeltaS[0] -= float(a[0])
DeltaS[0] /= 2
DeltaS[1] -= float(a[1])
DeltaS[1] /= 2
DeltaS[2] -= float(a[2])
DeltaS[2] /= 2
DeltaS[3] -= float(a[3])
DeltaS[3] /= 2
Head1.updateDeltaS(DeltaS)
print "valeurs de correction du voile obtenues :" 
print Head1.getDeltaS()
print "Fin de la séquence de dévoilage de la roue munie de la tête : " + Head1.getName()

print ""
print "Dévoilage roue munie de la tête : " + Head2.getName()
print "Réglez l'assiette de la roue munie de : " + Head2.getName()
raw_input("appuyer sur entrée pour continuer")
print ""
print "Mesure en cours...."

a = Head2.getAnalogIN()
refS0 = a[0]
refS1 = a[1]
refS2 = a[2]
refS3 = a[3]
time.sleep(1)
for k in range(6):
    a = Head2.getAnalogIN()
    print "Deviation S0 : " + str(abs(a[0]-refS0))
    if abs(a[0]-refS0) >= 3:
        print "Capteur parallélisme instable"
    print "Deviation S1 : " + str(abs(a[1]-refS1))
    if abs(a[1]-refS1) >= 3:
        print "Capteur carrosage instable"
    print "Deviation S2 : " + str(abs(a[2]-refS2))
    if abs(a[2]-refS2) >= 3:
        print "Capteur alignement essieu instable"
    print "Deviation S3 : " + str(abs(a[3]-refS3))
    if abs(a[3]-refS3) >= 3:
        print "Capteur assiette instable"
    time.sleep(1)
DeltaS = []
DeltaS.append(float(a[0]))
DeltaS.append(float(a[1]))
DeltaS.append(float(a[2]))
DeltaS.append(float(a[3]))
print DeltaS
print ""
print "Tournez d'un demi-tour la roue munie de la tête : " + Head2.getName()
print "Réglez l'assiette de la roue munie de : " + Head2.getName()
raw_input("appuyer sur entrée pour continuer")
a = Head2.getAnalogIN()
refS0 = a[0]
refS1 = a[1]
refS2 = a[2]
refS3 = a[3]
time.sleep(1)
for k in range(6):
    a = Head2.getAnalogIN()
    print "Deviation S0 : " + str(abs(a[0]-refS0))
    if abs(a[0]-refS0) >= 3:
        print "Capteur parallélisme instable"
    print "Deviation S1 : " + str(abs(a[1]-refS1))
    if abs(a[1]-refS1) >= 3:
        print "Capteur carrosage instable"
    print "Deviation S2 : " + str(abs(a[2]-refS2))
    if abs(a[2]-refS2) >= 3:
        print "Capteur alignement essieu instable"
    print "Deviation S3 : " + str(abs(a[3]-refS3))
    if abs(a[3]-refS3) >= 3:
        print "Capteur assiette instable"
    time.sleep(1)
print a
print ""
DeltaS[0] -= float(a[0])
DeltaS[0] /= 2
DeltaS[1] -= float(a[1])
DeltaS[1] /= 2
DeltaS[2] -= float(a[2])
DeltaS[2] /= 2
DeltaS[3] -= float(a[3])
DeltaS[3] /= 2

Head2.updateDeltaS(DeltaS)
print "valeurs de correction du voile obtenues :" 
print Head2.getDeltaS()
print "Fin de la séquence de dévoilage de la roue munie de la tête : " + Head2.getName()

print ""
print "Valeurs calibration : " + Head1.getName()
print "Zero : "
print Head1.getZeroValue()
print "Sensibilité : "
print Head1.getSensiValue()
print ""
print "Valeurs calibration : " + Head2.getName()
print "Zero : "
print Head2.getZeroValue()
print "Sensibilité : "
print Head2.getSensiValue()
raw_input("press enter key to continue")
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
		pad.addstr(0, 1, "Script mesure 2 tetes", curses.color_pair(1))

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

		pad.addstr(LENGTH-1, 1, "rien")
		pad.refresh(0,0, 1,1, LENGTH,WIDTH+2)
        
                write_value(1,Head1.getName()) 
        	write_value(3,Head2.getName()) 
	
                write_value(4,"Brut/Angle")
                write_value(8,"Brut/Angle")
                write_value(12,"Brut/Angle")
                write_value(16,"Brut/Angle")
	        ANGL = [0.0,0.0,0.0,0.0]
                DEG = [0,0,0,0]
                MIN = [0,0,0,0]
		while True:
			pad.refresh(0,0, 1,1, LENGTH,WIDTH+2)
                        
                        if dec == 1 :
                            AIN = Head1.getAnalogIN()
                            Delta = Head1.getDeltaS()
                            Zero = Head1.getZeroValue()
                            Sensi = Head1.getSensiValue()
                            for k in range(4):
                                ANGL[k] = (AIN[k]+Delta[k]-Zero[k])/Sensi[k]
                                DEG[k] = int(ANGL[k])
                                MIN[k] = int(round((ANGL[k]-DEG[k])*60))
                            write_value(5, str(AIN[0])  )
                            write_value(9, str(AIN[1]))
                            write_value(13, str(AIN[2]) +"/" + str(DEG[2]) + "d" + str(MIN[2])+ "m")
                            write_value(17, str(AIN[3]))

                            write_value(6, str(round(ANGL[0],4)))
                            write_value(10, str(round(ANGL[1],4)))
                            write_value(14, str(round(ANGL[2],4)))
                            write_value(18, str(round(ANGL[3],4)))
                            
                            write_value(7, str(DEG[0]) + "d" + str(MIN[0])+ "m")
                            write_value(11, str(DEG[1]) + "d" + str(MIN[1])+ "m")
                            write_value(15, str(DEG[2]) + "d" + str(MIN[2])+ "m")
                            write_value(19, str(DEG[3]) + "d" + str(MIN[3])+ "m")


                        if dec == LOOP :
                            dec = 0
                        time.sleep(0.01) 
                        dec += 1
	except:
		# In event of error, restore terminal to sane state.
		restore_terminal()
		traceback.print_exc()	# Print the exception

