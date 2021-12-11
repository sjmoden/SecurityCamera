import os
import errno
import uuid
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy
import logging


def testPath(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
    
def uploadToStorageAccount(path):
    testPath(path)
    
    connectStr = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')    
    blobServiceClient = BlobServiceClient.from_connection_string(connectStr)
    
    containerName = "images"
    blobName =  f"{uuid.uuid4()}{os.path.basename(path)}"
    blobClient = blobServiceClient.get_blob_client(container=containerName, blob=blobName)
    
    logging.info("Uploading to Azure Storage as blob:\n\t" + blobName)
    
    with open(path, "rb") as data:
        blobClient.upload_blob(data)
        
    os.remove(path)
    
def checkTakePictureQueueAndDestroyAnyMessage():
    connectStr = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    queueName = "camera"
    queueClient = QueueClient.from_connection_string(conn_str=connectStr, queue_name=queueName,
                            message_encode_policy = BinaryBase64EncodePolicy(),
                            message_decode_policy = BinaryBase64DecodePolicy())
    message = queueClient.receive_message()
    if message is not None:
        queueClient.delete_message(message.id, message.pop_receipt)
        if message.content.decode() == "takepicture":
            return True;
        return False
    return False