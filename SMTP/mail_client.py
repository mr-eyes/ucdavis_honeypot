import socket
import sys
import hashlib
from AES import AES_Cipher

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
