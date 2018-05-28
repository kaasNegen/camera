# This class is imported and used in prototype.

import cv2
import imutils
import numpy as np
import time
from imutils.video import VideoStream
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread

'''
 How to use this class:
 c = Camera()
   if c.data_ready:
     for thing in c.data_ready:
       (name, pan_value) = thing
       c.play_sound(name, pan_value)
       c.data_ready = None
'''


class Camera:
    def __init__(self):
        print("Starting camera")
        self.data_ready = None
        self.net = None
        self.stream = VideoStream(src=0).start()
        self.load_model()
        time.sleep(1.0)  # Warm up camera
        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            time.sleep(0.1)
            if not self.data_ready:
                # grab the frame from the threaded video stream and resize it
                # to have a maximum width of 400 pixels
                frame = self.stream.read()
                # Width is 400, length is 300
                frame = imutils.resize(frame, width=400)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # (rows, columns, channels) Channels is the RGB or Gray value
                image_shape = gray.shape
                print("ImageShape")
                print(image_shape)

                brightness_sum = 0
                for l in range(0, image_shape[0]):
                    for w in range(0, image_shape[1]):
                        brightness_sum += gray[l, w]  # individual pixel

                average_brightness = brightness_sum / 120000  # 400 * 300
                # Trigger should happen if the brightness is around ~ 100
                print(average_brightness)

                if average_brightness < 100:
                    self.play_sound()
                    time.sleep(2.0)
                    # Wait on this thread for the object detection to finish
                    self.detect_object_easy()

    def stop(self):
        self.stream.stop()
        print("Camera stopping")

    def play_sound(self, audio_to_play="ping", pan_value=0):
        play(AudioSegment.from_mp3("python-sound-lib/audioFiles/" + audio_to_play + ".mp3").pan(
            pan_value))

    def load_model(self):
        # load our serialized model from disk
        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt',
                                            "MobileNetSSD_deploy.caffemodel")

    # Object for the outside world
    def detect_object_easy(self):
        # Time to remove hand in front of camera and for camera to refocus
        frame_to_detect = self.stream.read()
        frame_to_detect = imutils.resize(frame_to_detect, width=400)

        self.data_ready = self.detect_object(frame_to_detect)

    def detect_object(self, frame):
        # initialize the list of class labels MobileNet SSD was trained to
        # detect, then generate a set of bounding box colors for each class
        classes = ["achtergrond", "vliegtuig", "fiets", "vogel", "boot",
                   "fles", "bus", "auto", "kat", "stoel", "koe", "eettafel",
                   "hond", "paard", "motorfiets", "persoon", "plant", "schaap",
                   "bankstel", "trein", "tvmonitor"]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)),0.007843, (300, 300), 127.5)

        # pass the blob Caffe to run detections and predictions
        self.net.setInput(blob)
        detections = self.net.forward()

        default_confidence = 0.4

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # don't include weak detections by checking confidence is
            # greater than the default_confidence
            if confidence > default_confidence:
                # get the index of the class label from the
                # detections, then calculate the (x, y)-coordinates
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (start_x, start_y, end_x, end_y) = box.astype("int")

                cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), colors[idx], 2)
                print("python-sound-lib/audioFiles/" + classes[idx] + ".mp3")
                center = (start_x + end_x) / 2
                print(center)
                pan_value = (center / 200) * -1 if center < 200 else ((center - 200) / 200)
                print(pan_value)

                return classes[idx], pan_value

        return 'geen_object', 0
