#!/usr/bin/python3

from modules.socketUI import *

class ClientUI(SocketUI):
    # "Subclass to handling socket connection from client side"
    def __init__(self, name, hostName = "", port = 8000):
        super().__init__(hostName = hostName, port = port)
        self.name = name

    def set_up_connection(self):
        # "Connect to server"
        self.client = socket.socket()
        self.client.connect(self.address)

    def start_chat(self):
        # "Initialise chat with server"
        logging.info("[Starting connection]")
        logging.debug("[Requesting for keys]")
        self.send_json_data(self.client, {"request": "keys"})

        keys = self.recive_message(self.client)
        if not isinstance(keys.get("p"), int) and isinstance(keys.get("g"), int):
            logging.error("[Unexpected data. Aborting]")
            return
        logging.debug("[Received keys]")
        diffyHellman = DiffiHellman(keys, int(random.randrange(1, self.max_ab)))

        #ToDo: parallel send and receibe A&B
        logging.debug("[Sending calculated A]")
        self.send_json_data(self.client, {"a": diffyHellman.calc_AB()})

        data = self.recive_message(self.client)
        if not isinstance(data.get("b"), int):
            logging.error("[Unexpected data. Closing connection]")
            connection.close()
            return
        logging.debug("[Received calculated B]")
        self.encrypter = Encrypter(diffyHellman.calc_s(data.get("b")))

        encryption = "cesar"
        logging.debug("[Setting encryption as:] {}".format(encryption))
        self.send_json_data(self.client, {"encryption": encryption})
        self.encrypter.setEncryption(encryption)

        logging.info("[Starting chat]")
        receive_data_thread = threading.Thread(target=self.recv_data)
        receive_data_thread.start()
        try:
            while True:
                input_data = input()
                message = {"from": self.name, "msg": self.encrypter.encrypt(input_data)}
                logging.debug("[Sending message] {}".format(message))
                self.send_json_data(self.client, message)
        except KeyboardInterrupt:
            self.closeChat = True
            # self.client.settimeout(1)
            receive_data_thread.join()
            self.clinet.close()
            logging.info("[Connection closed]")

    def recv_data(self):
        # "Looped read data method for background message receiving"
        self.closeChat = False
        while not self.closeChat:
            data = self.recive_message(self.client, 0)
            message = self.encrypter.decrypt(data["msg"])
            logging.info("[Received message from: {}] {}".format(data["from"], message))
