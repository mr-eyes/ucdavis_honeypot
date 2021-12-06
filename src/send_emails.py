from smtplib import SMTP as Client

client = Client('127.0.0.1', 10025)


for i in range(1, 11, 1):
    r = client.sendmail('mahussien@ucdavis.edu', ['bishop@ucdavis.edu'], f"""\
        Hi Matt, this is the email number {i}
    """)