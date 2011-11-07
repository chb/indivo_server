from indivo.tests.internal_tests import InternalTests
import random, string

class TokenModelUnitTests(InternalTests):
    """ Base class for unit tests of token-derived models. Provides basic utilities
        for generating tokens. """

    def generate_random_string(self, length=20):
        return "".join([random.choice(string.printable[0:62]) for i in range(length)])

    def generate_token_and_secret(self):
        return self.generate_random_string(), self.generate_random_string()
