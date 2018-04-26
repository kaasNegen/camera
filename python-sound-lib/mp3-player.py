import argparse
import playsound

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--location", required=True, help="path to mp3 file")
args = vars(ap.parse_args())

location = args["location"] + ".mp3"
print(location)

playsound.playsound(location, True)

