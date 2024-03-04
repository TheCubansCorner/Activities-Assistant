#! python3
#! encrypt_password -- Encrypts user password to be saved

class EncryptPassword:
    def __init__(self):
        pass

    def subPassword(self, password : str) -> str:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!?@#$"
        key =      "KQPXULCZTVFOADGIJYHWESMRNB4893125706$#@?!"
        encryptPassword = []

        # Code Substitution
        for letter in password:
            for inx, ltr in enumerate(alphabet):
                
                if letter.upper() == ltr:
                    if letter == ltr.lower():
                        encryptPassword.append(key[inx].lower())
                    else:
                        encryptPassword.append(key[inx])

        encryptPassword = self.rothPassword(''.join(encryptPassword))
        return encryptPassword

    def rothPassword(self, password : str) -> str:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!?@#$"
        length = len(alphabet)
        decPassword = []
        # Code Roth13
        for letter in password:
            letterIndex = alphabet.index(letter.upper())
            newIndex = letterIndex + 13
            while newIndex > length - 1:
                newIndex -= length

            decPassword.append(alphabet[newIndex])
        
        decPassword = "".join(decPassword)

        return decPassword

    def decodeSubPassword(self, password : str) -> str:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!?@#$"
        key = "KQPXULCZTVFOADGIJYHWESMRNB4893125706$#@?!"
        decPassword = []

        # Decode Substitution
        for letter in password:
            for inx, ltr in enumerate(key):
                if letter.upper() == ltr:
                    if letter == ltr.lower():
                        decPassword.append(alphabet[inx].lower())
                    else:
                        decPassword.append(alphabet[inx])
        
        decPassword = "".join(decPassword)

        return decPassword

    def decodeRothPassword(self, password : str) -> str:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!?@#$"
        length = len(alphabet)
        decPassword = ''
        # Decode Roth13
        for letter in password:
            letterIndex = alphabet.index(letter.upper())
            newIndex = letterIndex - 13
            while newIndex < 0:
                newIndex += length 

            decPassword += alphabet[newIndex]
        
        decPassword = self.decodeSubPassword("".join(decPassword))

        return decPassword

    def encrypt(self, password: str) -> str:
        crypt = self.subPassword(password)
        return crypt

    def decrypt(self, password : str) -> str:
        crypt = self.decodeRothPassword(password)
        return crypt


if __name__ == "__main__":
    EncryptPassword()