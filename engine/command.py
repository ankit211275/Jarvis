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
            eel.receiverText(text)
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
def allCommands(message=1):
    # input through mic
    if message==1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    # input through chatbox
    else:
        query=message
        eel.senderText(query)

    try:
    
        if "open" in query:
            from engine.features import opencommand
            opencommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preference = takecommand()
                print(preference)

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preference:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)
        elif "news" in query:
            from engine.features import get_news
            get_news()

        else:
            # let openAI handle 
            from engine.features import aiProcess
            output = aiProcess(query)
            eel.DisplayMessage(output)
            speak(output)
    except:
        print("error")
    eel.ShowHood()