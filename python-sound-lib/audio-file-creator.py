# gtts is een convenience library die het makkelijker maakt om
# gebruik te maken van Google Text-to-Speeach API
from gtts import gTTS
import os

tts = gTTS(text='Geen object herkend', lang='nl')
tts.save('geen_object.mp3')

objects =  ["achtergrond", "vliegtuig", "fiets", "vogel", "boot",
	"fles", "bus", "auto", "kat", "stoel", "koe", "eettafel",
	"hond", "paard", "motorfiets", "persoon", "plant", "schaap",
	"bankstel", "trein", "tvmonitor"]

for obj in objects:
  print(obj)
  tts = gTTS(text=obj, lang='nl')
  tts.save(obj + ".mp3")

# distances
distances = []
for distance in distances:
  tts = gTTS(text='op een afstand van vijf meter', lang='nl')
  tts.save('afstand.mp3')

