from gtts import gTTS
from io import BytesIO
from pygame import mixer
import time

soundLocation = 'hello_bonjour.mp3'

tts = gTTS('bonjour', lang='fr')

with open(soundLocation, 'wb') as f:
    tts.write_to_fp(f)

def playSound(soundLocation):
    mixer.init()
    mixer.music.load(soundLocation)
    mixer.music.play()

playSound(soundLocation)