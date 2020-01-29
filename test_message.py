from gtts import gTTS
from playsound import playsound

warnfile = "attn.wav"
speechfile = "speak.mp3"

tts = gTTS(text="Hello world!", lang='en')
tts.save(speechfile)

playsound(warnfile)
playsound(speechfile)
print("done")
