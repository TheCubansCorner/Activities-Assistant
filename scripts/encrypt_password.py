#! python3
#! encrypt_password -- Encrypts user password to be saved

import os

from configparser import ConfigParser


class EncryptPassword:
    def __init__(self) -> None:                                 # -- Initiates the module
        self.config: object = ConfigParser()
        self.config.read(os.path.join("config", "config_activities.ini"))

    def subPassword(self, password: str) -> str:                # -- Encodes password and sends it to the second encoder
        keyOne: str = self.config["KEYS"]["iterate"]
        keyTwo: str = self.config["KEYS"]["key"]
        encryptPassword: str = ""

        # Code Substitution
        for letter in password:
            for inx, ltr in enumerate(keyOne):
                
                if letter.upper() == ltr:
                    if letter == ltr.lower():
                        encryptPassword += keyTwo[inx].lower()
                    else:
                        encryptPassword += keyTwo[inx]

        encryptPassword: str = self.rothPassword(encryptPassword)
        return encryptPassword

    def rothPassword(self, password: str) -> str:               # -- Encodes the already encoded password
        key: str = self.config["KEYS"]["iterate"]
        length: int = len(key)
        decPassword: str = ""

        # Code Roth13
        for letter in password:
            letterIndex: int = key.index(letter.upper())
            newIndex: int = letterIndex + 13
            while newIndex > length - 1:
                newIndex -= length

            decPassword += key[newIndex]
        
        decPassword: str = decPassword

        return decPassword

    def decodeSubPassword(self, password: str) -> str:          # -- Finishes the decoding process
        keyOne: str = self.config["KEYS"]["iterate"]
        keyTwo: str = self.config["KEYS"]["key"]
        decPassword: str = ""
        
        # Decode Substitution
        for letter in password:
            for inx, ltr in enumerate(keyTwo):
                if letter.upper() == ltr:
                    if letter == ltr.lower():
                        decPassword += keyOne[inx].lower()
                    else:
                        decPassword += keyOne[inx]
        
        decPassword: str = decPassword

        return decPassword

    def decodeRothPassword(self, password: str) -> str:         # -- Decodes password and sends it to the second decoder
        key: str = self.config["KEYS"]["iterate"]
        length: int = len(key)
        decPassword: str = ""

        # Decode Roth13
        for letter in password:
            letterIndex = key.index(letter.upper())
            newIndex = letterIndex - 13
            while newIndex < 0:
                newIndex += length 

            decPassword += key[newIndex]
        
        decPassword: str = self.decodeSubPassword(decPassword)

        return decPassword

    def encrypt(self, password: str) -> str:                    # -- Sends password to encoders
        return self.subPassword(password)

    def decrypt(self, password: str) -> str:                    # -- Sends password to decoders
        return self.decodeRothPassword(password)


if __name__ == "__main__":
    EncryptPassword()
