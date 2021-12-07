# This is the testing script to start the `ucdavis_honeypot` and test the
# detection and reply mechanisms.

import sys
import os
import argparse

# We import the python classes from the `src` directory

sys.path.append(os.path.join(os.getcwd(),"src"))

from DetectClass import DetectClass
from const_name_table import *

from UtilFunctions import *

# We take the input parameters from the user here. All the parameters are
# taken while starting the server.

parser = argparse.ArgumentParser(
    description = "This program runs tests for `ucdavis_honeypot` program."
)

# We obtain the number of honeypot class objects to instantiate. Each such
# object is associated with a `fake` email address.

parser.add_argument(
    "--type",
    type = str,
    required = True,
    help = "Input the type of test to execute.",
    choices=["sample", "namegen", "emailgen"]
)

parser.add_argument(
    "--cmode",
    type = str,
    required = True,
    help = "Mail Checking mode or Spam Detection Filter to use. ML to enable\
     a machine learning based filter. Generic means otherwise.",
    choices=["ML", "Generic"]
)

parser.add_argument(
    "--rmode",
    type = str,
    required = True,
    help = "Reply mode or reply mail generation. ML to enable\
     a machine learning based reply mechanism. Generic means otherwise.",
    choices=["ML", "Generic"]
)

if __name__ == "__main__":

    # We first check the input arguments. Then we continue the program.

    args = parser.parse_args()
    test_cases = 0
    test_result = 0

    if args.type == "sample":
        # We execute the "sample" test using the spam mails in the tests/sample
        # directory.

        PATH = "tests/sample"
        for files in os.listdir(os.path.join(os.getcwd(), PATH)):
            
            # We keep a count of all the tests.
            test_cases = test_cases + 1

            # We open each of the files present in the aforementioned directory
            f = open(PATH + "/" + files, "r")

            # We keep the contents stored in a separate file.
            contents = []
            str_content = f.read()
            for lines in str_content.split("\n"):
                contents.append(lines)

            # We close the file.
            f.close()

            # We parse the file for important information.
            receiver = ""
            sender = ""
            body_start_idx = -1
            body_start = False
            body_lines = []

            for idx, lines in enumerate(contents):
#                print(lines)
                if "Delivered-To: " in lines:
                    receiver = lines.split(": ")[1]
                if "Return-Path: " in lines:
                    sender = lines.split(": ")[1]
                if "Content-Type: text/plain; charset=\"UTF-8\"" in lines:
                    body_start_idx = idx
                    body_start = True

                # This may create false positive cases.

                if "--0000" in lines and "Content-Type: text/html; \
charset=\"UTF-8\"" in contents[idx + 1]:
                    body_start = False
                if body_start == True:
                    body_lines.append(lines)
            
            # Verify once that we have the correct values for the sender,
            # the receiver and the body of the message.

            if receiver == "":
                raise Exception("Incorrect format encountered! receiver name \
is empty!")
                exit(-1)

            if sender == "":
                raise Exception("Incorrect format encountered! sender name \
is empty!")
                exit(-1)

            if len(body_lines) == 0:
                raise Exception("Incorrect format encountered! body lines are\
                    empty!")
                exit(-1)

            # We have all our required values.
            # Now we need to pass these values to verify whether this mail is a
            # spam mail or not.

            detect_object = DetectClass(str_content)

            # We need to ensure that a given mail is DEFINITELY a spam mail.
            # We don't want to bother genuine mail senders.
            spam_checker = detect_object.checkSpamMailWithSeparatedValues(
                receiver,
                sender,
                body_lines,
                args.cmode
            )

            # We cannot perform an interactive test without performing a
            # social experiment. Therefore, our sample tests are simple 1 -> 1
            # mails, where we feed in a spam mail, and, the test generates a
            # reply mail for the same.
            # TODO: We would write interactive tests in the future.

            # If and only if the mail is detected as a spam, we proceed.
            # In the  test/sample directory, we know that all of the files
            # present are spam mails. Therefore, we expect all tests to return
            # True for checkSpamMail(..) function.

            # TODO: Add genuine mails as well.

            if spam_checker == True:
                # TODO: TODO:  Work this thing out.
                reply = detect_object.getReply(body_lines, args.rmode)
                print(
                    "Printing the reply mail for test file {}.".format(files)
                )
                print(reply)
                test_result = test_result + 1
            else:
                # The test failed!
                print("{} is NOT detected as a spam. \
Therefore, this test FAILED!".format(files))

            # The testing for the given file `files` is complete. We continue
            # the parent loop.

            # We prrint a line here
            print()
            print("=========================================================")
            print()

        # We iterated over all the files present in the tests/sample directory
        # for the `sample` tests.
    elif args.type == "namegen":
        # In this test, we try to generate names based off constant files.
        # Names have three lists: male, female and surname/last name

        full_names = readAndGetNameList(10)
        print(full_names)
        test_cases = 1
        test_result = 1

    elif args.type == "emailgen":
        # We test email generation using this method

        print(constWriteNameEmailPair(10))
        test_cases = 1
        test_result = 1

    else:
        # All other tests are not implemented currently.
        # TODO: Implement other tests
        raise Exception("We currently support \"sample\" tests only!")
        exit(-1)
    # We print the testing statistics here
    print("== Results ==")
    print()
    print("  Number of tests executed: {}".format(test_cases))
    print("  Number of pass:           {}".format(test_result))
    print("  Number of fail:           {}".format(test_cases-test_result))
    print()

    # Done
    exit(0)



