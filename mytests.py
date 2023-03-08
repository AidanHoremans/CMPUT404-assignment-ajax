import unittest
import json
# your server
import server
import random

BASEHOST = '127.0.0.1'
BASEPORT = 5000

def utf8(utf8bytes):
    return utf8bytes.decode("utf-8")

class OtherTests(unittest.TestCase):
    def setUp(self):
        '''Check this out: we're not actually doing HTTP we're just calling the webservice directly'''
        self.app = server.app.test_client()

    def tearDown(self):
        '''nothing'''
        
    def testNothing(self):
        '''nothing'''