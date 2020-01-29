# Remember to scroll down past the import statements to set your bot's token.

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
    from playsound import playsound
    import discord
except:
    sys.stderr.write("ERROR: Failed to import modules! Please make sure you have gTTS, playsound and discord installed. Install with: \"pip install gTTS playsound discord\"\n")
    sys.exit(2)

client = discord.Client()


# Set your bot's token here
token = ""


@client.event
async def on_ready():
    print("Connected to Discord.\n")

# Function used to announce everything

createMessageSuccess = False


def announce(announcement):
    global createMessageSuccess
    createMessageSuccess = False

    warnfile = "attn.wav"
    speechfile = "speak.mp3"

    os.system("@echo off && del /F /A " + speechfile)   # delete the old file, or else it will not work

    try:
        tts = gTTS(text=announcement, lang='en')
        tts.save(speechfile)
        createMessageSuccess = True
    except:
        pass

    # if for some reason Google can't generate a sound file, give an error
    if not createMessageSuccess:
        return "ERROR: Failed to generate announcement!"

    os.system("nircmdc.exe muteappvolume timechimes.exe 1")  # mute TimeChimes while the announcement is being made
    print(time.ctime() + ": \"" + announcement + "\"")
    playsound(warnfile)
    playsound(speechfile)
    os.system("nircmdc.exe muteappvolume timechimes.exe 0")  # unmute TimeChimes
    
    return "Announcement \"" + announcement + "\" successfully played on " + systemName + "!"


# Customize announcements and define all the commands here

def goToOffice(studentName):
    if studentName == "":
        return "ERROR: You must enter a student name!"
    studentName += '.'
    return announce((studentName + " Please come to the office. ") * 2)


def attendanceReminder():
    return announce("Attention all teachers. If you have not handed in your attendance slips, please do so now. Thank you!")


def indoorRecess():
    return announce("Attention all teachers and students. We will be having an indoor recess. Once again, we will be having an indoor recess. Thank you!")


def bellError():
    return announce("Attention all teachers and students. Today is not a short bell day. Please disregard the previous bell. Thank you!")

# Main function triggered when the bot receives a message - put the commands that you want it to recognize here


def mainFn(inStr):
    global client
    command = inStr.split(' ', 1)[0]
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
    else:
        return "ERROR: Invalid command!"


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await message.channel.send(mainFn(message.content))

client.run(token)
