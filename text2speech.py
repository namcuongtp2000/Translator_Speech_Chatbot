import time
import os
import playsound
import speech_recognition as sr
from gtts import gTTS

def speak(massage):
    speech = gTTS(text=massage, lang= "en")
    filename="voice.mp3"
    speech.save(filename)
    playsound.playsound(filename)
