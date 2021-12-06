import os
import random

# We use a name table for generating fake names and their associated email
# addresses. One key element while generating fake names is `diversity` within
# the names. Therefore, we use the following resources to generate common names
# from around the world.
#
# The format is:
# __Country_Name__: __Common_First_Name__
#     __Common_Last_Name__
#
# American: https://www.ssa.gov/oact/babynames/decades/century.html
#     https://www.al.com/news/2019/10/50-most-common-last-names-in-america.html
# Chinese: https://improvemandarin.com/most-popular-chinese-names/
#     https://en.wikipedia.org/wiki/Chinese_surname
# Indian: https://forebears.io/india/forenames
#     https://forebears.io/india/surnames
# Arabic: https://parenting.firstcry.com/articles/100-arabic-last-names-or-surnames/
#     https://stepfeed.com/al-baik-is-finally-opening-in-riyadh-and-saudis-are-going-crazy-4616

# We will add more names for more including more diversity, while developing
# the honeypot framework.

# We need this list to generate `UC Davis` style email addresses. Every name
# must appear at the end of the reply mail, in order to demonstrate a signed
# email reply.

def getEmptyLists():
    # We return three lists: (a) male list, (b) female list, and, (c) surname
    # list.
    return [],[],[]

def getFileList():
    return os.listdir(os.path.join(os.getcwd(), "src/files"))

# We iterate over all the available name files in the src/files directory, and,
# generate a comprehensive list of names. Our honeypot system aims at
# generating real-like names, hence, the combination of first name and last
# name is important.

def readAndGetNameList(required):
    """
        Method readAndGetNameList(int) has one mandatory argument.
        required: The number of phantom names required.

        The method returns `names` as a list of names.
    """

    # We equally divide the names for better diversity.
    num_files = len(getFileList())
    factor = required/num_files
    PATH = "src/files/"
    # We create 3 empty lists
    male, female, surname = getEmptyLists()

    names = []
    for jdx,files in enumerate(getFileList()):

        # We iteratively open each name file in the src/files directory, and,
        # obtain the first, and, the last name.

        # Files are in the format:
        # 10,male_names,separated,by,commas\n
        # 10,female_names,separated,by,commas\n
        # 10,common,surnames,separated,by,commas

        f = open(PATH + files, "r")
        for idx, lines in enumerate(f.read().split()):
            for words in lines[:-1].split(","):
                if idx == 0:
                    male.append(words)
                elif idx == 1:
                    female.append(words)
                elif idx == 2:
                    surname.append(words)
                else:
                    print("warn: unexpected line encountered in {} \
                            file".format(files),file=sys.stderr)
        f.close ()
        
        # We now want to generate combinations of names here.
        # We generate 50% male names and other 50% female names.
    
    for i in range(0, int(factor/2)):
        offset = random.randint(0, jdx)
        names.append(male[random.randint(offset * 10, offset * 10 + 9)] \
                + " " \
                + surname[random.randint(offset * 10, offset * 10 + 9)])
        names.append(female[random.randint(offset * 10, offset * 10 + 9)] \
                + " " \
                + surname[random.randint(offset * 10, offset * 10 + 9)])

    # We double check whether we met the (factor * num_files) and required are
    # true.

    if len(names) != required:
        while(len(names) != required):
            # male, females, surname are filled
            names.append(male[random.randint(0, 9)] \
                    + " " \
                    + surname[random.randint(0, 9)])
            if(len(names) == required):
                break
            names.append(female[random.randint(0, 9)] \
                    + " " \
                    + surname[random.randint(0, 9)])

    # We have the required number of names.

    return names
