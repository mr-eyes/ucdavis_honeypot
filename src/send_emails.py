from smtplib import SMTP as Client
import time

client = Client('127.0.0.1', 10025)


r = client.sendmail('student@gmail.com', ['someone@ucdavis.edu'], f"""\
        Hi someone...
    """)

# Note that rrodriguez@ucdavis.edu is a phantom email
r = client.sendmail('spammer@gmail.com', ['someone@ucdavis.edu', 'rrodriguez@ucdavis.edu'], f"""\
        Hi rrodriguez, this is job offer ....
    """)
