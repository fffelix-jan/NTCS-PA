# Licenced under the GNU GPL v3: http://www.gnu.org/licenses/gpl-3.0.en.html

# Set your bot's token and the name of the system here:
token = ""
systemName = "Secondary PA"


print("""
NTCS TTS PA System (ver. 1.0)
Copyright (c) 2020 Felix An

System: """ + systemName + """

This window runs the text-to-speech PA system, which can be operated using a Discord bot. 
DO NOT CLOSE THIS WINDOW, OR ELSE IT WILL NOT WORK!
""")

import sys
import os
import time
if not sys.platform == 'win32':
    sys.stderr.write("ERROR: This program must be run on a Windows Vista or newer system!\n")
    sys.exit(1)
os.system("nircmdc.exe muteappvolume timechimes.exe 0")
try:
    print("Loading...")
    from gtts import gTTS
    import discord
except:
    sys.stderr.write("ERROR: Failed to import modules! Please make sure you have gTTS and discord installed. Install with: \"pip install gTTS discord\"\n")
    sys.exit(2)

client = discord.Client()


@client.event
async def on_ready():
    print("Connected to Discord.\n")


# This function is a minor modification of the playsound module by TaylorSMarks: https://github.com/TaylorSMarks/playsound
def playsound(sound, block=True):
    from ctypes import c_buffer, windll
    from random import random
    from time import sleep
    from sys import getfilesystemencoding

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
            raise PlaysoundException(exceptionMessage)
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
    warnfile = "attn.wav"
    speechfile = "speak.mp3"

    try:
        tts = gTTS(text=announcement, lang='en')
        tts.save(speechfile)
    except:
        return "ERROR: Failed to generate announcement!"

    os.system("nircmdc.exe muteappvolume timechimes.exe 1")  # mute TimeChimes while the announcement is being made
    print(time.ctime() + ": \"" + announcement + "\"")
    playsound(warnfile)
    playsound(speechfile)
    os.system("nircmdc.exe muteappvolume timechimes.exe 0")  # unmute TimeChimes
    os.remove(speechfile)

    return "Announcement \"" + announcement + "\" successfully played on " + systemName + "!"


# Customize announcements and define all the commands here

def goToOffice(studentName):
    if studentName == "":
        return "ERROR: You must enter a student name!"
    studentName += '.'
    return announce((studentName + " Please come to the office. ") * 2)


def attendanceReminder():
    return announce("Attention all teachers. If you have not handed in your attendance slips, please hand them in now. Thank you!")


def indoorRecess():
    return announce("Attention all teachers and students. We will be having an indoor recess. Once again, we will be having an indoor recess. Thank you!")


def bellError():
    return announce("Attention all teachers and students. Today is not a short bell day. Please disregard the previous bell. Thank you!")

# Main function triggered when the bot receives a message - put the commands that you want it to recognize here


def mainFn(inStr):
    global client
    command = inStr.split(' ', 1)[0].lower()
    try:
        mainInput = inStr.split(' ', 1)[1]
    except:
        mainInput = ""
    if command == "ofc":
        return goToOffice(mainInput)
    elif command == "ar":
        return attendanceReminder()
    elif command == "ir":
        return indoorRecess()
    elif command == "berr":
        return bellError()
    elif command == "anc":
        return announce(mainInput)
    elif command == "time":
        return time.ctime()
    else:
        return "ERROR: Invalid command!"


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await message.channel.send(mainFn(message.content))

client.run(token)
