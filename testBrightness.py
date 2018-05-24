import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils

print("[INFO] starting...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

# grab the frame from the threaded video stream and resize it
# to have a maximum width of 400 pixels
frame = vs.read()
frame = imutils.resize(frame, width=400)

# grab the frame dimensions
(h, w) = frame.shape[:2]

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
	  label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
	  cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
	  y = startY - 15 if startY - 15 > 15 else startY + 15

# update the FPS counter
fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# clean up video streaming stuffy
vs.stop()

