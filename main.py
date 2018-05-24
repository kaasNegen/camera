from threading import Thread
from real_time_object_detection_single_final import detectObject
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import subprocess
      
if __name__ == "__main__":
  print("Starting")
  vs = VideoStream(src=0).start()
  time.sleep(1.0) # Warm up camera

  while(True):
    time.sleep(1.0) # Less stressful on cpu
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400) # Width is 400, length is 300
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imageShape = gray.shape # (rows, columns, channels) Channels is the RGB or Gray value
    print("ImageShape")
    print(imageShape)

    brightnessSum = 0
    averageBrightness = 0
    for l in range(0, imageShape[0]):
      for w in range(0, imageShape[1]):
        brightnessSum += gray[l, w] # individual pixel

    averageBrightness = brightnessSum / 120000 # 400 * 300
    print(averageBrightness) # Trigger should happen if the brightness is around ~ 100
    
    if averageBrightness < 100:
      subprocess.Popen(["mpg123", "-q", "python-sound-lib/utilAudioFiles/ping.mp3"]).wait()
      time.sleep(2.0) # Time to remove hand in front of camera and for camera to refocus
      frameToDetect = vs.read()
      frameToDetect = imutils.resize(frameToDetect, width=400)
      thread = Thread(target = detectObject, kwargs={'frame':frameToDetect})
      thread.start()
      time.sleep(4.0) # Wait on this thread for the object detection to finish

  vs.stop()
  print("Finished")

