import os
import eel
from engine.features import *
from engine.command import *
from engine.auth import recognize

def start():
    eel.init("www")

    playAssistantSound()
    flag=recognize.AuthenticateFace()
    os.system('open -a "Google Chrome" --args --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', port=8000, block=True)

