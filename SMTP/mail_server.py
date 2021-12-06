import socket
import sys
import hashlib
from AES import AES_Cipher

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

PASSWORD = "mo"
AES_DECODER = AES_Cipher("PASSWORD")

while True:
    # Wait for a connection
    # print('waiting for a connection')
    connection, client_address = sock.accept()
    full_message = bytes()
    
    try:
        # print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            if data:
                full_message += data
                # print('received "%s"' % data)
                connection.sendall(bytes(data))
            else:
                full_message = AES_DECODER.decrypt(full_message).decode('utf-8')
                print(f"full_message: {full_message}")
                break
            
    finally:
        connection.close()