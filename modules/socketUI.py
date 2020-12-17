#!/usr/bin/python3

import threading
import logging
import random
import socket
import json
import time

from modules.diffiHellman import DiffiHellman
from modules.encrypter import Encrypter

logging.basicConfig(level = "INFO")

class SocketUI():
	# "Parent class for socket related operations"
    CHUNK_SIZE = 1024
    max_ab = 10
    def __init__(self, hostName = "", port = 8000):
        self.hostName = hostName
        self.port = port
        self.address = (self.hostName, self.port)

    def send_message(self, connection, message):
		# "Send raw text on specific connection"
        msg_string = str(message)
        connection.send(msg_string.encode())

    def send_json_data(self, connection, data):
    	# "Send data defined in json format"
        data_string = json.dumps(data)
        self.send_message(connection, data_string)

    def decode_message(self, data):
    	# "Decode message from string to json format"
        try:
            results = json.loads(data)
        except json.JSONDecodeError:
            logging.error("Incorrect data format!")
            exit(1)
        return results

    def recive_message(self, connection, timeout = 3):
    	# "Receive message on specific connection
    	# args: timeout - amount of retries(each delayed 1 second) when method attempt to read data from input stream. 0 means that attempt will not be timeouted"
        chunks = []
        chunk = connection.recv(self.CHUNK_SIZE).decode('utf-8')
        retry = 0
        while not chunk:
        	if not timeout == 0:
	            if retry < timeout: 
	                retry += 1
	                time.sleep(1)
	                chunk = connection.recv(self.CHUNK_SIZE).decode('utf-8')
	            else:
	                logging.warning("[Maximum amount of retries exceeded. No message reveived]")
	                return
        chunks.append(chunk)
 		# # ToDo: Fix chunk receiving - after reading first one it hangs waiting for input
        # while chunk:
        #     chunks.append(chunk)
        #     chunk = connection.recv(self.CHUNK_SIZE).decode('utf-8')
        message = ''.join(chunks)
        logging.debug("[Received message] {}".format(message))
        decoded_data = self.decode_message(message)
        return decoded_data
