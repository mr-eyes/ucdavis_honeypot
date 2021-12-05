#from DetectClass import DetectClass

# We use HoneySpawnClass as the forwarding destination for all suspicious
# emails. 
# We create a class which accepts an email body 

class HoneySpawnClass(DetectClass):
    def __init__(self, name, domain, instance_id):
        self.name = name
        self.domain = domain
        self.instance_id = instance_id
    
    def _generateEmailID(name, domain):
        """
            method generateEmailID(str, domain) accepts a name string separated
            by a space and a domain name which should be in the format
            domain.com.
        """
        # We use the name -> email format used at UC Davis.
        #
        # UC Davis uses the format stated below for emails.
        # If the person's name is John Doe, his email address will be:
        #           jdoe@ucdavis.edu
        #
        # If jdoe@ucdavis.edu is taken, then we arrive at the following
        # scenario:
        # The person's name is Jane Doe, we will resolve this conflict by:
        #           jadoe@ucdavis.edu
        # Conflicts are resolved by the HoneyUtil class.

        assert "@" not in domain

        first_name = name.split(" ")[0]
        last_name  = name.split(" ")[len(name.split(" ")) - 1]

        # Check whether the first and the last names are valid.

        if first_name == "" or last_name == "":
            raise Exception("Incorrect names detected!")
            exit(-1)

        # Otherwise resume the program.

        return first_name[0] + last_name + "@" + domain 

    def setPhantomEmailID(self, name, domain):
        return self._generateEmailID(name, domain)

    def _generateMLReply(message):
        raise NotImplementedError

    def _generateTraditionalReply(message):
        raise NotImplementedError

    def _generatePrivateKey(public_key):
        raise NotImplementedError

    def _encryptText(text, key):
        raise NotImplementedError

    def _decryptText(text, key):
        raise NotImplementedError

    def _setupMailServer(host, port):
        raise NotImplementedError

    def _testSendMail(src, dest, message):
        raise NotImplementedError

    def _testRecvMail(src, dest, message):
        raise NotImplementedError
