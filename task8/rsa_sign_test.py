import unittest
from rsa_sign import *
import random


class Rsa_Sign_Test(unittest.TestCase):
    # Setup method (optional)
    def setUp(self):
        # This method runs before each test method
        pass

    # Teardown method (optional)
    def tearDown(self):
        # This method runs after each test method
        pass

    def test_key_pair_N(self):
        public_key, private_key = generate_key_pair()
        N_public, e = public_key
        N_private, d = private_key
        self.assertEqual(N_public, N_private)

    def test_key_pair(self):
        public_key, private_key = generate_key_pair()
        N, e = public_key
        _, d = private_key
        message = random.randint(0, N - 1)

        self.assertEqual(pow(message, e * d, N), message)

    def test_sign_design(self):
        public_key, private_key = generate_key_pair()
        N, _ = public_key
        message = random.randint(0, N - 1)
        signature = rsa_sign(message, private_key)
        is_valid = rsa_verify(message, signature, public_key)
        self.assertTrue(is_valid)
