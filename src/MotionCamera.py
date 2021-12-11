import datetime
from picamera import PiCamera
import time
from AzureStorageAccount import uploadToStorageAccount, checkTakePictureQueueAndDestroyAnyMessage
import threading
import RPi.GPIO as GPIO
import logging

sensorPin = 11
logging.basicConfig(level=logging.INFO)
lastQueueCheck = time.time()
queueCheckWaitSeconds = 300

def takePicture(location):
    logging.info ('Take Picture')
    newImagePath = f"/home/pi/Desktop/Security/{location}{datetime.datetime.now()}.jpg"
    with PiCamera() as camera:
        camera.start_preview()
        camera.rotation = 180
        time.sleep(2)
        camera.capture(newImagePath)
        camera.stop_preview()
    logging.info('picture taken')
    

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(sensorPin, GPIO.IN)
    
    try:
        while True:
            if(time.time() - lastQueueCheck > queueCheckWaitSeconds):
                lastQueueCheck = time.time()
                if(checkTakePictureQueueAndDestroyAnyMessage()):
                    logging.info("Taking Picture from Queue")
                    takePicture("queue")
            if GPIO.input(sensorPin)==GPIO.HIGH:
                logging.info("Taking Picture from Motion")
                takePicture("motion")
 
    finally:
        GPIO.cleanup()
