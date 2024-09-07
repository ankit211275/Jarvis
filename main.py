import os
import eel
from engine.features import *
from engine.command import *
from engine.auth import recognize

def start():
    eel.init("www")

    playAssistantSound()
    @eel.expose
    def init():
        
        speak("Ready for Face Authentication")
        eel.hideLoader()
        authenticated = recognize.authenticate()
        if authenticated:
            eel.hideFaceAuth()
            speak("Face Authentication Successfull")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome sir, How can i help you?")
            eel.hideStart()
            playStartSound()
        else:
            speak("Face Authentication Failed!")
    os.system('open -a "Google Chrome" --args --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', port=8000, block=True)
    

