# UC Davis :: Email Honeypot Framework

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

## Development Environment

We have implemented a simple Python module that works on a local SMTP server for sending and receiving emails on the local network. The server will be used to test our spam filtration/identification module and the honeypot afterward.
For the Spam Filter, we have used python's antispam library. It provides a pretrained spam filter which will categorize a string(e-mail content) as spam or not. Further, we have used python's nltk library for text tokenization and processing. To implement the reply generator, we have used python's transformers and torch libraries.


##Dependencies
Use the pip command to download and install the libraries:-
pip3 install {package_name}

Have the following libraries of python installed before executing our code:-
1. transformers - pip3 install transformers
2. nltk - pip3 install nltk
3. torch - pip3 install torch




