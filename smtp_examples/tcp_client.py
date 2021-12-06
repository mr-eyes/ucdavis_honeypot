import socket
import sys
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


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)

received_data = bytes()
original_message_md5sum = None
received_message_md5sum = None

email_message = """
From: Mohamed Hussien <mahussien@ucdavis.edu>
To: Matt Bishop <bishop@ucdavis.edu>
Subject: A test
Message-ID: <TEST>
...
Hi Matt, this is Mo.
"""

PASSWORD = "mo" # should be securely passed not hard-coded
CIPHER = AES_Cipher(PASSWORD)

try:
    message = CIPHER.encrypt(email_message)
    original_message_md5sum = hashlib.md5(message).hexdigest()
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        received_data += data


finally:
    received_message_md5sum = hashlib.md5(received_data).hexdigest()
    assert received_message_md5sum == original_message_md5sum
    print('closing socket')
    sock.close()
