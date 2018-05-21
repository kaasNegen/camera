# How to use: python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2
import playsound

def detectObject():
  # initialize the list of class labels MobileNet SSD was trained to
  # detect, then generate a set of bounding box colors for each class
  CLASSES = ["achtergrond", "vliegtuig", "fiets", "vogel", "boot",
	  "fles", "bus", "auto", "kat", "stoel", "koe", "eettafel",
	  "hond", "paard", "motorfiets", "persoon", "plant", "schaap",
	  "bankstel", "trein", "tvmonitor"]
  COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

  # load our serialized model from disk
  print("[INFO] loading model...")
  net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', "MobileNetSSD_deploy.caffemodel")

  # initialize the video stream, allow the cammera sensor to warmup,
  # and initialize the FPS counter
  print("[INFO] starting video stream...")
  vs = VideoStream(src=0).start()
  time.sleep(2.0)
  fps = FPS().start()

  # grab the frame from the threaded video stream and resize it
  # to have a maximum width of 400 pixels
  frame = vs.read()
  frame = imutils.resize(frame, width=400)

  # grab the frame dimensions and convert it to a blob
  (h, w) = frame.shape[:2]
  blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
	  0.007843, (300, 300), 127.5)

  # pass the blob through the network and obtain the detections and
  # predictions
  net.setInput(blob)
  detections = net.forward()
  
  defaultConfidence = 0.4

  # loop over the detections
  for i in np.arange(0, detections.shape[2]):
	  # extract the confidence (i.e., probability) associated with
	  # the prediction
	  confidence = detections[0, 0, i, 2]

	  # filter out weak detections by ensuring the `confidence` is
	  # greater than the minimum confidence
	  if confidence > defaultConfidence:
		  # extract the index of the class label from the
		  # `detections`, then compute the (x, y)-coordinates of
		  # the bounding box for the object
		  idx = int(detections[0, 0, i, 1])
		  box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		  (startX, startY, endX, endY) = box.astype("int")

		  # draw the prediction on the frame
		  label = "{}: {:.2f}%".format(CLASSES[idx],
			  confidence * 100)
		  cv2.rectangle(frame, (startX, startY), (endX, endY),
			  COLORS[idx], 2)
		  y = startY - 15 if startY - 15 > 15 else startY + 15
		  print("python-sound-lib/audioFiles/" + CLASSES[idx] + ".mp3")
		  playsound.playsound("python-sound-lib/audioFiles/" + CLASSES[idx] + ".mp3", True)

  # update the FPS counter
  fps.update()

  # stop the timer and display FPS information
  fps.stop()
  print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
  print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

  # clean up video streaming stuffy
  vs.stop()

