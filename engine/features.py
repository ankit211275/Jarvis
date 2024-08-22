from playsound import playsound
import eel
import os
from engine.config import ASSISTANT_NAME
from engine.command import speak
import pywhatkit as kit
import webbrowser
import sqlite3
from engine.helper import extract_yt_term
import pvporcupine
import struct
import sounddevice as sd
import pyautogui as autogui
import time
import numpy as np

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# playsound on starting jarvis
@eel.expose
def playAssistantSound():
    music_dir = "www/assets/sound/mic_sound.mp3"
    playsound(music_dir)

# open app
def opencommand (query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.strip().lower()
    app_name = query
    
    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()
            

            if len(results) != 0:
                speak("Opening "+query)
                os.system('open "' + results[0][0] + '"')

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        query = query.replace(" ", "\\ ")
                        os.system('open -a '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine = None
    stream = None

    try:
        # Initialize Porcupine with your access key and keywords
        porcupine = pvporcupine.create(
            keywords=["jarvis", "alexa"],
            access_key="JcH5CvPStN/1yg3vMzI8zgX1h436UoH/nhtKy8DCLGwf51HCFx3aBA=="  # Replace with your Picovoice access key
        )

        # Callback function for processing audio stream
        def callback(indata, frames, time, status):
            if status:
                print(f"Callback Status: {status}")

            try:
                # Process audio data
                keyword_index = porcupine.process(indata.flatten())
                if keyword_index >= 0:
                    print("Hotword detected")
                    autogui.keyDown("command")
                    autogui.press("j")
                    time.sleep(0.1)  # Short delay to ensure the key press is registered
                    autogui.keyUp("command")
            except Exception as e:
                print(f"Callback Error: {e}")

        # Start the audio stream
        stream = sd.InputStream(
            samplerate=porcupine.sample_rate,
            channels=1,
            dtype='int16',
            callback=callback,
            blocksize=porcupine.frame_length
        )
        stream.start()
        print("Listening for hotwords...")

        while True:
            # Check if the stream is still active
            if not stream.active:
                print("Stream inactive. Restarting...")
                stream.start()
            time.sleep(0.1)  # Keep the script running and responsive

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if stream is not None:
            stream.stop()
            stream.close()
        if porcupine is not None:
            porcupine.delete()

if __name__ == "__main__":
    hotword()