import asyncio
from aiosmtpd.controller import Controller
import sys
import pika
import json
from AES import AES_Cipher

AES_PASSWORD = "mo"  # temporarly
IP_ADDR = "127.0.0.1"
PORT = 10025


class MessageQueue:
    ROUTING_KEY = "honeypot_emails_queue"

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.ROUTING_KEY, durable=True)

    def send_dict(self, message_d):
        json_message = json.dumps(message_d)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.ROUTING_KEY,
                                   body=json_message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                   ))

    def close_connection(self):
        self.connection.close()


class UCDAVIS_Handler:
    
    AES_ENCRYPTOR = AES_Cipher(AES_PASSWORD)
    PRODUCER = MessageQueue()
    phantom_list = []
    
    def __init__(self) -> None:
        with open("files/const_name_list.txt") as PHANTOMS:
            for line in PHANTOMS:
                line = line.strip().split(',')
                self.phantom_list.append(line[1])

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        
        sender = envelope.mail_from
        recipient = envelope.rcpt_tos
        body = envelope.content.decode('utf-8', errors='replace')

        payload = {
            "sender": sender,
            "recipient": recipient,
            "body": body, #self.AES_ENCRYPTOR.encrypt(),
        }
        
        print(payload)
        if set(recipient).intersection(set(self.phantom_list)):    
            self.PRODUCER.send_dict(payload)
        else:
            # Will not be passed to the honeypot
            pass
        
        return '250 Message accepted for delivery'


if __name__ == '__main__':
    handler = UCDAVIS_Handler()
    controller = Controller(handler, hostname=IP_ADDR, port=PORT)
    controller.start()
    # Wait for the user to press Return.
    input('UC DAVIS Honeypot SMTP server running. Press Return to stop server and exit.')
    controller.stop()
