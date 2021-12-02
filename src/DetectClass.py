import os
# TODO
from UtilFunctions import *


class DetectClass():
    def __init__(self, message):
        self.message = message

    def _getListOfFreeEmailList():
        raise NotImplementedError

    def _traditionalDetectMethod(message, domain):
        """
            private method _traditionalDetectMethod(..) accepts a message
            string and determines whether the message is a spam mail or not
            using IF ELSE statements. It also accepts a domain name
            "@domain.com" for verification.
        """

        # We use common recurring patterns in spam emails.
        # 
        #
        # 1. It is common that scam mails are usually sent from free mailing
        # services including but not limited to gmail.com, outlook.com,
        # yahoo.com etc. Therefore, we flag all such mails offering jobs. The
        # other detecting mechanism kept in place is the fact that all or some
        # part of the domain name must be present in a job letter, when it is
        # an internal job offer.
        #
        # 2. This is specific to University job offers. We know that that
        # maximum that a student can make is $42/hr ($21/hr for 50% employeed)
        # students. Any value exceeding it will automatically flag a mail if
        # the above point is false.
        #
        # 3. Detecting signatures at the end of the mail.

        flag_score = 0
        flag_mail_list = _getListOfFreeEmailList()

        # Checking Pt. 1
        # We get the receiver, sender and the of the message body.
        # Note that body is a list of strings.

        receiver, sender, body = utilBreakMessageIntoSegments(message)

        # Free mail list comparison
        
        sender_domain = sender.split("@")[1]
        if len(sender_domain) == 0 or "." not in sender_domain:
            raise Exception("Error while parsing sender_domain \
                    {}".format(sender_domain))
            exit(-1)
        
        for elements in flag_mail_list:
            if elements in sender_domain:
                flag_score = flag_score + 1
                break

        # Next we look for rate of money.

        amount = -1.0
        for lines in message:
            if "$" in lines:
                # This script only works for per hour rates at the moment. We
                # plan on increacing this in the future.
                amount = float(lines.split("$")[1].split("/")[0])
                break

        if amount > -1.0:
            # $42.0/hr is taken from the UC policy for employment
            if amount > 42.0:
                flag_score = flag_score + 1

        else:
            # We could not detect a pay rate in the mail.
            print("info: no payrate found on the mail.")

        # We look for a signature at the end. This may not work always :)

        for lines in body:
            if "thanks" in lines.lower() or "regards" in lines.lower() or
            "sincerely" in lines.lower():
                # Basically do nothing.
                # TODO: We need to improve this bit here.
                print("info: signature found!")
            else:
                flag_score = flag_score + 1

        # We are done testing. If `flag_score` > 0, we call it a scam mail.

        if flag_score > 0:
            return True
        return False

    def _modernDetectMethod(message, domain):
        """
            private method _modernDetectMethod(..) accepts a message
            string and determines whether the message is a spam mail or not
            using a ML based filter. It also accepts a domain name
            "@domain.com" for verification.
        """
        raise NotImplementedError

    # The public methods to access the private methods of DetectClass class.
    
    def checkSpamMailWithSeparatedValues(receiver, sender, message_list, mode):
        # Merge the receiver, sender, message_list.
        # TODO: fix this
        
        message = utilMergeMessage(receiver, sender, message_list)
        global_domain = utilGetDomain()

        if mode == True:
            # This means that we need to invoke the ML based detection filter.
            return _modernDetectMethod(message, global_domain)
        else:
            # We use the traditional detection method.
            return _traditionalDetectMethod(message, global_method)

    def checkSpamMail(message_string, mode):
        # Mostly same as the above function, but better ^_^
        global_domain = utilGetDomain()

        if mode == True:
            # This means that we need to invoke the ML based detection filter.
            return _modernDetectMethod(message_string, global_domain)
        else:
            # We use the traditional detection method.
            return _traditionalDetectMethod(message_string, global_method)

