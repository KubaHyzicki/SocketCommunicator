#!/usr/bin/python3

import logging
import base64

logging.basicConfig(level = "INFO")

class Encrypter():
    # "Module used to encrypt and decrypt data"
    available_encryption_types = ["none", "cesar", "xor"]

    def __init__(self, secret, encryptionType = "none"):
        self.encryptionType = encryptionType
        self.secret = secret

    def setEncryption(self, encryptionType):
        # "Set encrtption type from available options. Default is none"
        if encryptionType not in self.available_encryption_types:
            logging.error("Inproper encryption type. Available options: {}".format(self.available_encryption_types))
            exit(1)
        self.encryptionType = encryptionType

    def encrypt(self, data):
        # "Main encrypting method"
        if self.encryptionType == "cesar":
            return self.encryptCesar(data)
        if self.encryptionType == "xor":
            return self.encryptXOR(data)
        elif self.encryptionType == "none":
            return self.encodeB64(data)
        else:
            logging.error("Incorrect encryption type! {}".format(self.encryptionType))
            exit(1)

    def decrypt(self, data):
        # "Main decrypting method"
        if self.encryptionType == "cesar":
            return self.decryptCesar(data)
        if self.encryptionType == "xor":
            return self.decryptXOR(data)
        elif self.encryptionType == "none":
            return self.decodeB64(data)
        else:
            logging.error("Incorrect encryption type! {}".format(self.encryptionType))
            exit(1)

    def encodeB64(self, data):
        data_bytes = data.encode('ascii')
        encoded_data = base64.b64encode(data_bytes)
        return encoded_data.decode('ascii')

    def decodeB64(self, encoded_data):
        data_bytes = base64.decodebytes(encoded_data.encode('ascii'))
        decoded_data = data_bytes.decode('ascii')
        return decoded_data

    def encryptCesar(self, data):
        encrypted_data = ''
        for char in str(data):
            if (char.isupper()):
                encrypted_data += chr((ord(char) + self.secret - 65) % 26 + 65)
            else:
                encrypted_data += chr((ord(char) + self.secret - 97) % 26 + 97)
        return encrypted_data

    def decryptCesar(self, data):
        if isinstance(data, (bytes, bytearray)):
            data = data.decode('ascii')
        decrypted_data = ''
        for char in str(data):
            if (char.isupper()):
                decrypted_data += chr((ord(char) + (26 - 65) - self.secret) % 26 + 65)
            else:
                decrypted_data += chr((ord(char) + (26 - 97) - self.secret) % 26 + 97)
        return decrypted_data

    # def encryptXOR(self, data):
    #     encrypted_data = ''
    #     y = self.secret % 2

    #     for i in range(length): 
          
    #         inpString = (inpString[:i] + 
    #              chr(ord(inpString[i]) ^ ord(y)) +
    #                      inpString[i + 1:]);
    #         print(inpString[i], end = ""); 

    #     for char in str(data):
    #         bit_array = ''
    #         for bit in bin(ord(char)):
    #             encrypted_data += bit ^ y
    #         encrypted_data += chr(bit_array)
    #     return encrypted_data
    #     # return encrypted_data.encode('ascii')

    # def decryptXOR(self, data):
    #     if isinstance(data, (bytes, bytearray)):
    #         data = data.decode('ascii')
    #     decrypted_data = ''
    #     y = bool(self.secret % 2)
    #     for char in str(data):
    #         if (char.isupper()):
    #             encrypted_data += chr((ord(char) - self.secret - 65) % 26 + 65)
    #         else:
    #             encrypted_data += chr((ord(char) - self.secret - 97) % 26 + 97)
    #     return encrypted_data
