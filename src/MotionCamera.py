import datetime
from picamera import PiCamera
from time import sleep
from AzureStorageAccount import uploadToStorageAccount
import threading
import RPi.GPIO as GPIO
import logging

sensorPin = 11
ledPin = 12
logging.basicConfig(level=logging.INFO)

def takePicture():
    logging.info ('Take Picture')
    newImagePath = f"/home/pi/Desktop/Security/{datetime.datetime.now()}.jpg"
    
    with PiCamera() as camera:
        camera.start_preview()
        camera.rotation = 180
        sleep(2)
        camera.capture(newImagePath)
        camera.stop_preview()
    
    t = threading.Thread(target=uploadToStorageAccount, args=(newImagePath,))
    t.start()
    

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.setup(sensorPin, GPIO.IN)
    
    try:
        while True:
            if GPIO.input(sensorPin)==GPIO.HIGH:
                GPIO.output(ledPin,GPIO.HIGH)
                takePicture()           
            else :
                GPIO.output(ledPin,GPIO.LOW)
 
    finally:
        GPIO.cleanup()
