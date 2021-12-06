import hashlib
from Crypto.Cipher import AES
class AES_Cipher():
    IV = 16 * '\x00'
    mode = AES.MODE_CBC
    encryptor = None

    def __init__(self, password):
        password = password.encode('utf-8')
        key = hashlib.sha256(password).digest()
        self.encryptor = AES.new(key, self.mode, IV=self.IV)

    def encrypt(self, text_str):
        cipher_text = self.encryptor.encrypt(text_str)
        return cipher_text

    def decrypt(self, cipher_text):
        plain_text = self.encryptor.decrypt(cipher_text)
        return plain_text