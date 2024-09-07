from pipes import quote
import random
import subprocess
from playsound import playsound
import eel
import os

import requests
from engine.config import ASSISTANT_NAME
from engine.command import speak
import pywhatkit as kit
import webbrowser
import sqlite3
from engine.helper import extract_yt_term, remove_words
import pvporcupine
import struct
import sounddevice as sd
import pyautogui as autogui
import time
import numpy as np
from openai import OpenAI


con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# playsound on starting jarvis
@eel.expose
def playAssistantSound():
    music_dir = "www/assets/sound/mic_sound.mp3"
    playsound(music_dir)

@eel.expose
def playStartSound():
    music_dir = "www/assets/sound/start_sound.mp3"


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


# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 12
        jarvis_message = "Message sent successfully to " + name
    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "Calling " + name
    else:
        target_tab = 6
        message = ''
        jarvis_message = "Starting video call with " + name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Open WhatsApp with the constructed URL using macOS's 'open' command
    subprocess.run(['open', whatsapp_url])
    time.sleep(3)

    # autogui.hotkey('command', 'f')

    # for i in range(1, target_tab):
    #     autogui.hotkey('tab')

    autogui.press('return')
    speak(jarvis_message)

# openAI implementation
def aiProcess(command):
    try:
        client = OpenAI(api_key="api")
        completion = client.chat.completions.create(
            model = "gpt-4o",
            messages = [
                {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "I'm having trouble processing your request."

# get_news
def get_news():
    r = requests.get(f"https://newsapi.org/v2/everything?q=technology&apiKey=2848ec50eb4341949931d9b084defe94")

    if r.status_code == 200:
        # Parse the JSON response
        data = r.json()
    
        # Extract the articles
        articles = data.get('articles', [])
        # Randomly selecting any 5 articles or less
        articles = random.sample(articles, min(5, len(articles)))
        if not articles:
            speak("No news articles found.")
            eel.DisplayMessage("No news articles found.")
            return

        # Speak out and display the headlines
        for article in articles:
            title = article.get('title', 'No title available')
            image_url = article.get('urlToImage', 'default_image_url')  # Default URL if no image is available
            eel.showFetchingImage(image_url)
            speak(title)
            eel.DisplayMessage(title)
    else:
        error_message = f"Failed to fetch news: {r.status_code}"
        speak(error_message)
        eel.DisplayMessage(error_message)



# # chat bot 
# def chatBot(query):
#     user_input = query.lower()
#     chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
#     id = chatbot.new_conversation()
#     chatbot.change_conversation(id)
#     response =  chatbot.chat(user_input)
#     print(response)
#     speak(response)
#     return response

# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)