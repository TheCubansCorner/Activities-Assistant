#! python3
#! encrypt_password -- Encrypts user password to be saved

from configparser import ConfigParser

import os

class EncryptPassword:
    def __init__(self) -> None:
        self.config = ConfigParser()
        self.config.read(os.path.join("config", "config_activities.ini"))

    def subPassword(self, password : str) -> str:
        keyOne = self.config["KEYS"]["iterate"]
        keyTwo = self.config["KEYS"]["key"]
        encryptPassword = []

        # Code Substitution
        for letter in password:
            for inx, ltr in enumerate(keyOne):
                
                if letter.upper() == ltr:
                    if letter == ltr.lower():
                        encryptPassword.append(keyTwo[inx].lower())
                    else:
                        encryptPassword.append(keyTwo[inx])

        encryptPassword = self.rothPassword(''.join(encryptPassword))
        return encryptPassword

    def rothPassword(self, password : str) -> str:
        key = self.config["KEYS"]["iterate"]
        length = len(key)
        decPassword = []
        # Code Roth13
        for letter in password:
            letterIndex = key.index(letter.upper())
            newIndex = letterIndex + 13
            while newIndex > length - 1:
                newIndex -= length

            decPassword.append(key[newIndex])
        
        decPassword = "".join(decPassword)

        return decPassword

    def decodeSubPassword(self, password : str) -> str:
        keyOne = self.config["KEYS"]["iterate"]
        keyTwo = self.config["KEYS"]["key"]
        decPassword = []
        # Decode Substitution
        for letter in password:
            for inx, ltr in enumerate(keyTwo):
                if letter.upper() == ltr:
                    if letter == ltr.lower():
                        decPassword.append(keyOne[inx].lower())
                    else:
                        decPassword.append(keyOne[inx])
        
        decPassword = "".join(decPassword)

        return decPassword

    def decodeRothPassword(self, password : str) -> str:
        key = self.config["KEYS"]["iterate"]
        length = len(key)
        decPassword = ''
        # Decode Roth13
        for letter in password:
            letterIndex = key.index(letter.upper())
            newIndex = letterIndex - 13
            while newIndex < 0:
                newIndex += length 

            decPassword += key[newIndex]
        
        decPassword = self.decodeSubPassword("".join(decPassword))

        return decPassword

    def encrypt(self, password: str) -> str:
        crypt = self.subPassword(password)
        return crypt

    def decrypt(self, password : str) -> str:
        crypt = self.decodeRothPassword(password)
        return crypt


if __name__ == "__main__":
    x = EncryptPassword()
    y = x.encrypt("Sopu88!!")
    print(x.encrypt("Sopu88!!"))
    print(x.decrypt(y))