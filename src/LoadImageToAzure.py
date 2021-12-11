import os
from time import sleep
from AzureStorageAccount import uploadToStorageAccount
import logging

imageFolder = "/home/pi/Desktop/Security"
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    while True:
        files = os.listdir(imageFolder)
        
        if len(files) > 0:
            sleep(5)
            for file in files:
                fullpath = os.path.join(imageFolder, file)
                uploadToStorageAccount(fullpath)