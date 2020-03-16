print("NTCS Morning Reminder\nLoading...")

import sys
import datetime

dstoday = datetime.datetime.today()
dttoday = datetime.date.today()
#if dstoday.strftime("%A") == "Saturday" or dstoday.strftime("%A") == "Sunday":
#    print("Today is a weekend, exiting...")
#    sys.exit(0)

import os
os.chdir(r"C:\Users\ebell\NTCS-PA")

if not sys.platform.startswith('win'):
    sys.stderr.write("ERROR: This program must be run on a Windows Vista or newer system!\n")
    sys.exit(1)
try:
    from gtts import gTTS
except:
    sys.stderr.write("ERROR: Failed to import modules!\n")
    sys.exit(2)

import math
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

from ctypes import c_buffer, windll
from random import random
from time import sleep
from sys import getfilesystemencoding

warnfile = "attn.wav"
speechfile = "morningReminder.mp3"

# This function is a minor modification of the playsound module by TaylorSMarks: https://github.com/TaylorSMarks/playsound
def playsound(sound, block=True):
    def winCommand(*command):
        buf = c_buffer(255)
        command = ' '.join(command).encode(getfilesystemencoding())
        errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
        if errorCode:
            errorBuffer = c_buffer(255)
            windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
            exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                '\n        ' + command.decode() +
                                '\n    ' + errorBuffer.value.decode())
            raise Exception(exceptionMessage)
        return buf.value

    alias = 'playsound_' + str(random())
    winCommand('open "' + sound + '" alias', alias)
    winCommand('set', alias, 'time format milliseconds')
    durationInMS = winCommand('status', alias, 'length')
    winCommand('play', alias, 'from 0 to', durationInMS.decode())

    # Beginning of modifications by Felix An
    # This closes the file so that it can be deleted
    sleep(int(durationInMS.decode()) / 1000)
    winCommand('close ', alias)
    # End of modifications

# Function used to announce everything
def announce(announcement):
    global warnfile
    global speechfile
    try:
        os.remove(speechfile)
    except:
        pass

    try:
        tts = gTTS(text=announcement, tld='ca', lang='en')  # uses the Canadian Google Translate site
        tts.save(speechfile)
    except:
        print("ERROR: Failed to generate announcement!")

    try:
        print("Announcing...")
        playsound(warnfile)
        playsound(speechfile)
        os.remove(speechfile)
    except:
        print("ERROR: Failed to play sound! (Try restarting the PA system computer.)")
        
announce("Good morning North Toronto Christian School! Today's date is " + dstoday.strftime("%A") + " " + dstoday.strftime("%B") + " the " + ordinal(dttoday.day) + " " + str(dttoday.year) + "! Classes will begin shortly! Please remember to bring all necessary supplies for class. Thank you!")
