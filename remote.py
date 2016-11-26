#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  remote.py - Control a 3-button RF remote to raise and lower a
#              motorized projector screen
#
#  Copyright (C) 2015  Kyle T. Gabriel
#
#  remote.py is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  remote.py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with remote.py. If not, see <http://www.gnu.org/licenses/>.
#
#  Contact at kylegabriel.com

import ConfigParser
import getopt
from lockfile import LockFile
import os
import sys
import time
import RPi.GPIO as GPIO

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

lock_directory = "/var/lock"
write_lock_file = "{ldir}/remote-write".format(ldir=lock_directory)
run_lock_file = "{ldir}/remote-run".format(ldir=lock_directory)
config_file = os.path.join(__location__, 'remote.cfg')

# GPIO pins connected to the remote buttons
upPin = 8
downPin = 4
stopPin = 7


def usage():
    print "remote.py: Control a 3-button remote to raise and lower a" \
          "projector screen\n"
    print "Usage: remote.py OPTION\n"
    print "Options:"
    print "    -i, --initialize"
    print "           Initialize the GPIO pins (set all low)"
    print "    -d, --down"
    print "           Lower the screen"
    print "    -u, --up"
    print "           Raise the screen"
    print "    -h, --help"
    print "           Show this help and exit"


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(upPin, GPIO.OUT)
    GPIO.output(upPin, 0)
    GPIO.setup(downPin, GPIO.OUT)
    GPIO.output(downPin, 0)
    GPIO.setup(stopPin, GPIO.OUT)
    GPIO.output(stopPin, 0)


def read_config():
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    return config.get('Projector', 'projector_position')


def write_config(position):
    config = ConfigParser.RawConfigParser()
    if not os.path.exists(lock_directory):
        os.makedirs(lock_directory)    
    write_lock = LockFile(write_lock_file)

    while not write_lock.i_am_locking():
        try:
            write_lock.acquire(timeout=10)
        except Exception as e:
            print("Warning: Could not gain write lock: Breaking {path}:"
                  "{err}".format(path=write_lock.path, err=e))
            write_lock.break_lock()
            write_lock.acquire()

    config.add_section('Projector')
    config.set('Projector', 'projector_position', position)

    try:
        with open(config_file, 'wb') as configfile:
            config.write(configfile)
    except Exception as e:
        print("Unable to write config: {path}: {err}".format(path=config_file,
                                                             err=e))
    finally:
        write_lock.release()


def up():
    init()
    print "Raising projector screen"
    GPIO.output(upPin, 1)
    time.sleep(1)
    GPIO.output(upPin, 0)
    time.sleep(36.5)  # delay (seconds) for screen to fully raise
    GPIO.output(stopPin, 1)
    time.sleep(1)
    GPIO.output(stopPin, 0)
    time.sleep(0.1)
    GPIO.output(stopPin, 1)
    time.sleep(2.5)
    GPIO.output(stopPin, 0)
    write_config('up')


def down():
    init()
    print "Lowering projector screen"
    GPIO.output(downPin, 1)
    time.sleep(1)
    GPIO.output(downPin, 0)
    time.sleep(39)  # permit catching ctrl+c to stop screen descent
    GPIO.output(stopPin, 1)
    time.sleep(1)
    GPIO.output(stopPin, 0)
    write_config('down')


def write_stop():
    init()
    GPIO.output(stopPin, 1)
    time.sleep(1)
    GPIO.output(stopPin, 0)
    write_config('stop')


if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

if len(sys.argv) == 1:  # No arguments given
    usage()
    sys.exit(1)

try:
    opts, args = getopt.getopt(sys.argv[1:],
                               'iduh',
                               ["initialize", "down", "up", "help"])
except getopt.GetoptError as err:
    print(err)  # print "option -x not recognized"
    usage()
    sys.exit(2)

if not os.path.exists(lock_directory):
    os.makedirs(lock_directory)

run_lock = LockFile(run_lock_file)
while not run_lock.i_am_locking():
    try:
        run_lock.acquire(timeout=1)
    except Exception as e:
        print("Error: Cannot start: Run lock file present: {path}: "
              "{err}".format(path=run_lock.path, err=e))
        sys.exit(1)

try:
    projector_position = read_config()
    print("Projector is currently set as being {dir}.".format(
        dir=projector_position))
    for opt, arg in opts:
        if opt in ("-i", "--initialize"):
            print("Initializing GPIO pins connected to the projector remote")
            init()
        elif opt in ("-u", "--up"):
            if 'up' in projector_position:
                print("Cannot raise projector screen.")
            else:
                up()
        elif opt in ("-d", "--down"):
            if 'down' in projector_position:
                print("Cannot lower projector screen.")
            else:
                down()
        else:
            usage()
except KeyboardInterrupt:
    print("Keyboard interrupted operation")
    write_stop()
except Exception as e:
    print("Exception: {err}".format(err=e))
    write_stop()
finally:
    run_lock.release()
