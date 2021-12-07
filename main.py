# This is the server-side script to start the `ucdavis_honeypot`. This starts
# server and spawns n number of phantom identities.

import sys
import os
import argparse
import pika
import time
import json

DECRYPTION_PASSWORD = "mo"

sys.path.append(os.path.join(os.getcwd(),"src"))

from src.UtilFunctions import *
from src.DetectClass import *
from src.AES import AES_Cipher


# We take the input parameters from the user here. All the parameters are
# taken while starting the server.

parser = argparse.ArgumentParser(
    description = "This program starts the `ucdavis_honeypot` program. The \
        project is described in details in the README.md document. It takes \
        the following parameters as input while starting the program. We \
        assume that the network administrator starts this program."
)

# We obtain the number of honeypot class objects to instantiate. Each such
# object is associated with a `fake` email address.

parser.add_argument(
    "--num_phantom",
    type = int,
    required = True,
    help = "Input the number of phantom users to spawn. Each phantom is a \
            class object of __ class which consumes __ bytes on \
            initialization."
)

# One of the prominent features of the `ucdaivs_honeypot` project is that it
# can filter out scam mails and generate reply emails using a machine
# learning model. This ensures a lower false-positive and better effectiveness
# in the case of scamming mails.

parser.add_argument(
    "--set_filter",
    type = str,
    required = True,
    help = "Mail Checking mode or Spam Detection Filter to use. ML to enable\
     a machine learning based filter. Generic means otherwise.",
    choices=["ML", "Generic"]
)
parser.add_argument(
    "--set_reply_mech",
    type = str,
    required = True,
    help = "Reply mode or reply mail generation. ML to enable\
     a machine learning based reply mechanism. Generic means otherwise.",
    choices=["ML", "Generic"]
)

# Definition of __main__


if __name__ == "__main__":
    
    AES_DECRYPTOR = AES_Cipher(DECRYPTION_PASSWORD)
    
    def callback(ch, method, properties, body):
        full_email = body.decode()

        """
        All the processing goes here
        """
        payload = json.loads(body.decode())
        
        sender = payload["sender"]
        recipients = payload["recipient"][0]
        ciphered_body = payload["body"]
        
        # deciphered_body = AES_DECRYPTOR.decrypt(ciphered_body)
        print(f"[DEBUG]\nsender:{sender}\nrecipient: {recipients}\nbody{ciphered_body}\n______________________")
        
        SPAM_DETECTOR = DetectClass(ciphered_body)
        is_spam = SPAM_DETECTOR.checkSpamMailWithSeparatedValues(receiver=
                recipients, sender= sender, message_list=
                ciphered_body.split('\n'), mode = args.set_reply_mech)
        if is_spam:
            print(f"SPAM DETECTED")
        else:
            print(f"NOT SPAM")
        
        time.sleep(body.count(b'.'))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # First we check whether all the input parameters are correctly placed. If
    # not, then we exit the program.
    args = parser.parse_args()

    
    # Starting the rabbitmq consumer
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='honeypot_emails_queue', durable=True)
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='honeypot_emails_queue', on_message_callback=callback)
    channel.start_consuming()
    

