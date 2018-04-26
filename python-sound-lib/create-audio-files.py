from gtts import gTTS
import os
tts = gTTS(text='tree', lang='en')
tts.save("tree.mp3")


