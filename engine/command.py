import sounddevice as sd
import numpy as np
import speech_recognition as sr
import os
from gtts import gTTS
import eel
import time

def speak(text):
    if text:
        try:
            tts = gTTS(text=text, lang='en')
            tts.save("output.mp3")
            eel.DisplayMessage(text)
            os.system("afplay output.mp3")  # Use 'afplay' to play audio on macOS
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No text provided for speech.")


def takecommand():
    r = sr.Recognizer()
    
    # Use sounddevice to capture audio
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=6)
            print("Recognizing...")
            eel.DisplayMessage('Recognizing...')
            query = r.recognize_google(audio, language="en-in")
            eel.DisplayMessage(query)
            time.sleep(1)
            
        except sr.UnknownValueError:
            print("Google Web Speech Recognition could not understand audio.")
            eel.DisplayMessage('Couldn\'t understand...Please try again')
            time.sleep(1)
            eel.ShowHood()
            
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech Recognition service; {e}")
            return ""
        
        return query.lower()

@eel.expose # so that we can use this fn in main.js
def allCommands():
    
    try:
        query = takecommand()
        print(query)
    
        if "open" in query:
            from engine.features import opencommand
            opencommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        else:
            print("Not run")
    except:
        print("error")
    eel.ShowHood()