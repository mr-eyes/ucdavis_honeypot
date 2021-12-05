import os
# TODO
from UtilFunctions import *
import antispam
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import nltk

class DetectClass:
    def __init__(self, message):
        self.message = message

    def _getListOfFreeEmailList(self):
        list_of_free_email_providers = [
            "gmail.com",
            "yahoo.com",
            "rediffmail.com",
            "icloud.com",
            "outlook.com",
            "hotmail.com"
        ]
        return list_of_free_email_providers

    def _traditionalDetectMethod(self, message, domain):
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
        flag_mail_list = self._getListOfFreeEmailList()

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
            if "thanks" in lines.lower() or "regards" in lines.lower() or \
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

    def _modernDetectMethod(self, message, domain):

        """
            private method _modernDetectMethod(..) accepts a message
            string and determines whether the message is a spam mail or not
            using a ML based filter. It also accepts a domain name
            "@domain.com" for verification.
        """
        if(antispam.is_spam(getBodyAsString(message))):
           return True
        return False

    # The public methods to access the private methods of DetectClass class.
   
    def _traditionalReplyGenerator(self, message):
        """
            This function generates replies based on IF ELSE statements.
        """
        generic_greet = ["Hi,", "Respected Sir,", "Respected Madam,",
            "Respected Sir/Madam,", "Dear Sir,", "Dear Madam,",
            "Dear Sir/Madam,", "Hello,", "Hello Sir,", "Hello Madam,",
            "Hello Sir/Madam,"]
        generic_reply_body = ["I'm interested in the offer. Please tell me \
more about it!", "The offer seems nice, can you tell me more about it?", "I \
interested in this offer. How can I apply for it?", "The pay seems too less. \
I may become interested if the pay increases.", "I'm interested!!! I'll get \
back with my CV soon."]
        generic_thanks = ["Thanks,", "Thank You,", "Regards,",
                "Yours Sincerely,"]
        import random
        h_idx = random.randint(0, len(generic_greet) - 1)
        b_idx = random.randint(0, len(generic_reply_body) - 1)
        t_idx = random.randint(0, len(generic_thanks) - 1)

        filler = "\n\n\n"
        head = generic_greet[h_idx]
        body = generic_reply_body[b_idx]
        tail = generic_thanks[t_idx]

        return head + filler + body + filler + tail + "\n"

    def _mlReplyGenerator(self, message):
            def _mlReplyGenerator(self, message):
        """
            private method mlReplyGenerator(..) accepts a message
            string and generates a reply to that string and returns that string
        """
        nltk.download("punkt")
        model_name = "microsoft/DialoGPT-large"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        message = message[3:-9]
        for step in range(1):
            reply = ""
            for sentence in message:
                input_ids = tokenizer.encode(
                        sentence + tokenizer.eos_token, return_tensors="pt")
                # concatenate new user input with chat history (if there is)
                bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids
                # generate a bot response
                chat_history_ids = model.generate(
                    bot_input_ids,
                    max_length=1000,
                    do_sample=True,
                    top_p=0.95,
                    top_k=0,
                    temperature=0.75,
                    pad_token_id=tokenizer.eos_token_id
                    )
                #print the output
                output = tokenizer.decode(
                        chat_history_ids[:, bot_input_ids.shape[-1]:][0],
                        skip_special_tokens=True
                        )
                reply = reply + output + ' '
             break

            #print(reply)
         return reply


    def getReply(self, message, mode):
        """
            Public method to generate reply.
            message: input message in plain text.
            mode: True for ML mode, False for IF ELSE mode.
        """
        if mode == "ML":
            return self._mlReplyGenerator(message)
        else:
            return self._traditionalReplyGenerator(message)
        
    
    def checkSpamMailWithSeparatedValues(self, receiver, sender, message_list, mode):
        # Merge the receiver, sender, message_list.
        # TODO: fix this
        message = utilMergeMessage(receiver, sender, message_list)
        global_domain = utilGetDomain()

        if mode == "ML":
            # This means that we need to invoke the ML based detection filter.
            return self._modernDetectMethod(message, global_domain)
            # TODO
        else:
            # We use the traditional detection method.
            return self._traditionalDetectMethod(message, global_domain)

    def checkSpamMail(message_string, mode):
        # Mostly same as the above function, but better ^_^
        global_domain = utilGetDomain()

        if mode == True:
            # This means that we need to invoke the ML based detection filter.
            return _modernDetectMethod(message_string, global_domain)
        else:
            # We use the traditional detection method.
            return _traditionalDetectMethod(message_string, global_method)

