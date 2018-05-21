from threading import Thread
from time import sleep
from real_time_object_detection_single import detectObject

if __name__ == "__main__":
  print("Starting")
  thread = Thread(target = detectObject)
  thread.start()
  print("Finished")

