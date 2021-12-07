import os
from HoneyClass import HoneyClass
from const_name_table import *

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

def constWriteNameEmailPair(required):
    # We generate a list of name email pair
    names = readAndGetNameList(required)
    dic = {}
    honey_class_obj = HoneyClass(0)
    for idx, elements in enumerate(names):
        dic[elements] = honey_class_obj.setPhantomEmailID(elements, utilGetDomain())
    return dic
    

# @Mo, please add your changes

