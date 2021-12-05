import os

def utilBreakMessageIntoSegments(message):
    receiver = message[0]
    sender = message[1]
    body = message[2]
    return receiver, sender, body

def utilGetDomain():
    return "ucdavis.edu"

def utilMergeMessage(recv, sender, message):
    one_list = []
    one_list.append(recv)
    one_list.append(sender)
    one_list.append(message)
    return one_list

def getBodyAsString(message):
    outstr = ""
    for lines in message[2]:
        outstr = outstr + lines + "\n"
    return outstr

# @Mo, please add your changes

