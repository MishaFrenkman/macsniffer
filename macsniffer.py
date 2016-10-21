#!/usr/bin/python
# -*- coding: utf-8 -*-

""" * Macsniffer *

Author: MishaFrenkman

About:  This script reacts on a connection/disconnection of a specific device in your local network based on its MAC 

Usage:
	-h (--help) for arguments usage
	- run with sudo
	- provide your own network and device information
	- edit push() with your own script
	- nmap must be installed
"""

from time import sleep
from timeit import default_timer as timer
from subprocess import call, PIPE, Popen
import datetime
import argparse

def date():
	return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

def shell(command):
	process = Popen(
		args=command,
		stdout=PIPE,
		shell=True
	)
	return process.communicate()[0]

def push(par):
	# executes bash script
	shell("~/bin/sendPush " +par)

buff = 1
def log(msg):
	if args.log:
		global buff
		if buff:
			open('monitormac.log', 'w+')
			buff = 0

		with open("monitormac.log", "a") as myfile:
			myfile.write(msg +"\n")
			myfile.close()
	else:
		print(msg)

# grep multiple macs (OR)
'''
macs = {
	"mac1" : "AB:12:CD:34:EF:56",
	"mac2" : "98:FE:76:DC:54:BA"
}
multi = "'"
for i in macs.itervalues():
	multi += i + "|"

multi = multi[:-1] + "'"
'''

msg = {
	1: "'Welcome!'",
	0: "'Bye bye :('"
}

### Arguments ###
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interface', default="en1", help="Desired wifi interface")
parser.add_argument('-n', '--net', '--network', required=True, help="Local network (eg. 192.168.1.0/24)")
parser.add_argument('-m', '--mac', required=True, help="MAC Address of desired device")
parser.add_argument('-l', '--log', action="store_true", help="Logs stdout to logfile (monitormac.log)")
parser.add_argument('-w', '--wait', default=30, help="Defines how long to wait before recognize abscence of device")
parser.add_argument('-s', '--sleep', default=5, help="Scan every n seconds")

args = parser.parse_args()

cmd = "sudo nmap -e %s -sP %s | grep %s" % (args.interface, args.net, args.mac)
log(cmd)
#################


### Logic ###
start = 0
diff = 0
toggle_timer = 0

while 1:
	found = shell(cmd)

	# Found #
	if found:
		log("\n%s\nMAC found!" % date())

		if (toggle_timer == 0):
			log("sending..")
			push(msg[1])
			toggle_timer = 1

	# !Found #
	if not found:
		log("\n%s\nMAC not found!" % date())
		if (toggle_timer != 0):
			if start == 0:
				start = timer()
			end = timer()
			diff = end - start

		if (diff > args.wait):
			log("sending..")
			push(msg[0])
			diff = -1
			toggle_timer = 0
			start = 0

	log("Time away : %d" % diff) 

	#scan every n seconds
	sleep(args.sleep)
#######
