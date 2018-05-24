import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time

print("[INFO] starting...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

while(True):
  # grab the frame from the threaded video stream and resize it
  # to have a maximum width of 400 pixels
  frame = vs.read()
  frame = imutils.resize(frame, width=400) # Width is 400, length is 300
  
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  imageShape = gray.shape # (rows, columns, channels)
  print("ImageShape")
  print(imageShape)

  # A gray pixel has an array with a length of 1
  px = gray[100,100]

  brightnessSum = 0
  averageBrightness = 0
  for l in range(0, imageShape[0]):
    for w in range(0, imageShape[1]):
      brightnessSum += gray[l, w]

  averageBrightness = brightnessSum / 120000
  print(averageBrightness) # Trigger should happen if the brightness is around ~ 100

  cv2.imshow('frame', gray)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# update the FPS counter
fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# clean up video streaming stuffy
cv2.destroyAllWindows()
vs.stop()

