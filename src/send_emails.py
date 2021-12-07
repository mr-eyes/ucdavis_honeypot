from smtplib import SMTP as Client
import time

client = Client('127.0.0.1', 10025)


for i in range(1, 11, 1):
    r = client.sendmail(f"scammer_{i}@gmail.com", ['recipient@ucdavis.edu'], f"""\
        Hi, this is a job offer for you! you will get paid $45/hr! Apply now!
    """)
    time.sleep(1)