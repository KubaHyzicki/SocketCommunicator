#!/usr/bin/python3

import re

from modules.socketUI import *

class Client():
    "Object class containing client specific information allowing server to handle them in parallel"
    def __init__(self, connection, thread):
        self.connection = connection
        self.thread = thread
        self.encrypter = None

class ServerUI(SocketUI):
    # "Subclass to handling socket connection from server side"
    keys = {'p': 17, 'g': 7}
    name = 'Ciastek'

    def __init__(self, hostName = "", port = 8000):
        super().__init__(hostName = hostName, port = port)
        self.clients = []

    def start_server(self):
        # "Main initialise server method"
        self.server = socket.socket()
        self.server.bind(self.address)
        self.stopServer = False
        main_server_thread = threading.Thread(target = self.run)
        main_server_thread.start()
        logging.info("Server correctly set up. Listening")
        while True:
            input_data = input()
            if input_data == "exit":
                break
            if input_data == "help":
                logging.info("[Type exit to shut down server][Type '$\{client_id\}]:$\{message\}' to send sth to specific client]")
                continue
            if not re.match(r'([0-9]+):(.*)', input_data):
                logging.error("Incorrect command! Type help for help ;)")
                continue
            m = re.match(r'([0-9]+):(.*)', input_data)
            id = int(m.group(1))
            message = str(m.group(2))
            message_json = {"from": self.name, "msg": self.clients[id].encrypter.encrypt(message)}
            logging.debug("[Sending message] {}".format(message))
            self.send_json_data(self.clients[id].connection, message_json)

        logging.info("[Shutting down server]")
        stopServer = True
        main_server_thread.join()
        self.server.close()
        logging.info("[Successfully closed all connections]")

    def run(self):
        # "Looped listeing for connection method for creating client specific separate threads"
        while not self.stopServer:
            self.server.listen(1)
            connection, addr = self.server.accept()
            client = Client(connection, threading.Thread(target = self.handle_client, args = (len(self.clients), connection)))
            client.thread.start()
            self.clients.append(client)
        for clinet in self.clients:
            client.thread.join()

    def handle_client(self, id, connection):
        # "Handle connection with client"
        diffyHellman = DiffiHellman(self.keys, int(random.randrange(1, self.max_ab)))

        logging.info("[New connection established]")
        data = self.recive_message(connection)
        if not data.get("request") == "keys":
            logging.error("[Unexpected data. Closing connection]")
            connection.close()
            return
        logging.debug("[Requested for keys]")
        logging.debug("[Sending keys]" + str(self.keys))
        self.send_json_data(connection, self.keys)

        #ToDo: parallel send and receibe A&B
        data = self.recive_message(connection)
        if not isinstance(data.get("a"), int):
            logging.error("[Unexpected data. Closing connection]")
            connection.close()
            return
        logging.debug("[Received calculated A]")
        logging.debug("[Sending calculated B]")
        self.send_json_data(connection, {"b": diffyHellman.calc_AB()})
        encrypter = Encrypter(diffyHellman.calc_s(data.get("a")))

        data = self.recive_message(connection)
        if not data.get("encryption"):
            logging.error("[Unexpected data. Closing connection]")
            connection.close()
            return
        logging.debug("[Set encryption] {}".format(data["encryption"]))
        encrypter.setEncryption(data.get("encryption"))

        logging.info("[Starting chat]")
        self.clients[id].encrypter = encrypter
        try:
            while not self.stopServer:
                data = self.recive_message(connection = connection, timeout = 0)
                if not data.get("from") and data.get("msg"):
                    logging.error("[Unexpected data. Closing connection]")
                    break
                message = self.clients[id].encrypter.decrypt(data["msg"])
                logging.info("[Received message from: {}] {}".format(data["from"], message))
        except AttributeError:
            logging.error("[Empty message recepived. Closing connection]")
            pass
        connection.close()
        logging.info("[Connection closed]")
