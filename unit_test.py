#!/bin/python3
from clean_pc import *
import unittest

class FirstUnitTest(unittest.TestCase):
    def test_nb_one(self):
        self.assertEqual(5, len("hello"))
        print("prout")

if __name__ == '__main__':
    unittest.main()
