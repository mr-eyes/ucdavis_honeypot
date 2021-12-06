# UC Davis :: Email Honeypot Framework

> This project is for research purposes, it's not intended for production and it's not working in a production level.


![GMT20211206-080328_Recording_3742x1274 (online-video-cutter com)](https://user-images.githubusercontent.com/7165864/144810463-9818deb8-875b-4d8f-99b1-1bdbd5af68e7.gif)



## Abstract

This program creates a honeypot framework to disrupt malicious emails, often
targeting institutions. We create a honeypot mail server, which acts as a
real world entity, and, keeps the malicious scammer busy. In addition, there is
also a mail forwarding system kept in place, where suspected malicious emails
can be forwarded and the honeypot initiates a scripted communication sequence.
The end goal is to waste time and resources of the scammers.

## Structure of the Framework

In this section, we describe the proposed framework, and, explain each of the
components in a detailed manner. We have a primary mail server. The mail server
manager is a python program which instantiates objects of the honeypot
framework to create phantom identities, within the working environment. Based
on prior experience on the receiving end of malicious emails, we found that
such emails are usually sent in bulks, covering nearly all of a certain user
group. In the context of an university, these user groups are usually the
various departments. We ensure that phantom email ids are present in each of
such user groups. These phantom emails should be the first ones to reply back
to the scamming party. This ensures two things: (a) time and resources of the
scamming organization is ensured to be wasted first, and, (b) enough time is
available of the institution to aware its employees or students. There will be
a mail address available within the institution, where any suspected scam mails
can be forwarded.

In addition to the user based interaction, we also propose to add a
machine-learning based model to filter out `most` scam mails. We use a similar
model to generate replies for the scammers. When this filter is triggered, the
primary division for spearding awareness is also notified. Figure 1 depicts the
entire proposal holistically.
```
                          ┌──────────────────────────────────────────────────┐
                        ┌─┼─ v0 ──┐ all potential    1. If the volume of 'f' │
┌──────────────┐  out   ├─┼─ v1 ──┤ victims forward     rises sharply, the   │
│ Scamming     ├────────┼─┼─ v2 ──┤ any suspicious      management can issue │
│ Organization ├────┐   │ │  .    │ emails to the       awareness emails.    │
└──────────────┘ in │   │ │  .    │ 'f' forwarding   2. p,f starts to waste  │
 sends malicious    │   ├─┼─ vn ──┤ email address.      time and resources   │
 employment emails  │   └─┼─ p,f ─┘                     of the scammers.     │ 
┌───────────────────┘     └──┼─┼─────────────────────────────────────────────┘
│                            │ │
│ ┌──────────────────────────┴─┴─────────────────────────────────────────────┐
│ │ 1. We use a ma-  p is the phantom email address, and, it                 │
│ │    chine learn-  starts to reply back to the scamming o-                 │
│ │    ing model to  rganzation. f receives the same suspic-                 │
│ │    filter  spam  ious email from all the potential vict-                 │
│ │    mails.        ims. f spawns n number of phantom email                 │
└─┤ 2. We use anot-  ids, and, all of these emails start re-                 │
  │    her ML model  lying back to the scamming organization                 │
  │    to reply ba-                                                          │
  │    ck.                                                                   │
  └──────────────────────────────────────────────────────────────────────────┘
```

## Installation and running

#### 1. Clone
```sh
git clone https://github.com/mr-eyes/ucdavis_honeypot.git
cd ucdavis_honeypot
```

#### 2. Create conda enviornment

> wanna things install faster? use mamba instead of conda.

```sh
conda env create -f environment.yml
conda activate honeypot
```

#### 3. Run the broker system for handling emails queue

From a separate terminal, run the following command.

```sh
rabbitmq-server start
```

#### 4. Run the SMTP server

From a separate terminal, run the following command.

```sh
cd src
python mail_server.py
```

#### 5. Run the honeyot system

num_phantom: number of fake emails to use for the honeypot
set_filter: True if Machine Learning mode, False if Generic mode.
set_reply_mech: The autoreply on the scammer. True if Machine Learning mode, False if Generic mode.

```sh
python main.py --num_phantom 10 --set_filter True --set_reply_mech True
```

#### 6. Send emails to the system

You can edit and run the script `src/send_emails.py` to send emails to the system.



