# Copyright (c) 2021 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Imports
import binascii
import unittest
from bip_utils import Base58ChecksumError, Bip38Decrypter, Bip38Encrypter
from tests.ecc.test_ecc import (
    TEST_VECT_SECP256K1_PRIV_KEY_INVALID,
    TEST_ED25519_PRIV_KEY, TEST_ED25519_BLAKE2B_PRIV_KEY, TEST_ED25519_MONERO_PRIV_KEY,
    TEST_NIST256P1_PRIV_KEY, TEST_SR25519_PRIV_KEY
)


# Tests from BIP38 page (without EC multiplication)
# https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki
TEST_VECT = [
    {
        "passphrase": "TestingOneTwoThree",
        "priv_key_bytes": b"cbf4b9f70470856bb4f40f80b87edb90865997ffee6df315ab166d713af433a5",
        "encrypted": "6PYNKZ1EAgYgmQfmNVamxyXVWHzK5s6DGhwP4J5o44cvXdoY7sRzhtpUeo",
    },
    {
        "passphrase": "Satoshi",
        "priv_key_bytes": b"09c2686880095b1a4c249ee3ac4eea8a014f11e6f986d0b5025ac1f39afbd9ae",
        "encrypted": "6PYLtMnXvfG3oJde97zRyLYFZCYizPU5T3LwgdYJz1fRhh16bU7u6PPmY7",
    },
]

# Tests for encrypted strings with invalid checksum
TEST_VECT_DEC_CHKSUM_INVALID = [
    "6PYRZqGd3ecBNWQhrkyJmJGcTnUv7pmiDRxQ3ipJjenAHBNiokh2HTV1BU",
    "6PYV1dQkF66uex9TVxW9JQhjsr4bHkwu1zfjHtvZD7VcJssY4awDjGgc26",
]

# Tests for encrypted strings with invalid encoding
TEST_VECT_DEC_ENCODING_INVALID = [
    # Invalid base58 encoding
    "6PYNKZ1EAgYgmQfmNVamxyXVWHzK5s6DGhwP4J5o44cvXdoY7sRzhtpUeO",
    "6PYltMnXvfG3oJde97zRyLYFZCYizPU5T3LwgdYJz1fRhh16bU7u6PPmY7",
    # Invalid length
    "H3VYWSrgqLzqdXreTTfkL83ZJASYVFvy78q7j69nnt5WAcgMfq3eX2i",
    "cGAd8AVkr5wZEQpJ7wzyc4BKerkEwiyGVPUnJ2cV6wgLhpVuXPr71eh1G1Hm7Gu",
    # Invalid prefix
    "6SSstNWVoV33gBrLYEbxUDj7xdnWcX6SNZvCedM3812j7vLysouLGzeFz9",
    # Invalid flagbyte
    "6PJQrGM5jUZ2mSug3ZKcy6W72T54dbu1wZSD8Q2TWRJ3q9qHiQPEBkafwL",
    # Invalid address hash
    "6PYTRmk5E6ddFqtiPZZu6BpZ1LXAVazbvkmUys9R2qz6o3eSsW9GDknHNu",
    # Invalid private key

]


#
# Tests
#
class Bip38NoEcTests(unittest.TestCase):
    # Run all tests in test vector
    def test_vector(self):
        for test in TEST_VECT:
            # Test encryption
            enc = Bip38Encrypter.EncryptNoEc(binascii.unhexlify(test["priv_key_bytes"]), test["passphrase"])
            self.assertEqual(test["encrypted"], enc)
            # Test decryption
            dec = Bip38Decrypter.DecryptNoEc(test["encrypted"], test["passphrase"])
            self.assertEqual(test["priv_key_bytes"], binascii.hexlify(dec))

    # Test invalid checksum for decoding
    def test_dec_invalid_checksum(self):
        for test in TEST_VECT_DEC_CHKSUM_INVALID:
            # "with" is required because the exception is raised by Base58 module
            with self.assertRaises(Base58ChecksumError):
                Bip38Decrypter.DecryptNoEc(test, "")

    # Test invalid encoding for decoding
    def test_dec_invalid_encoding(self):
        for test in TEST_VECT_DEC_ENCODING_INVALID:
            # "with" is required because the exception is raised by Base58 module
            with self.assertRaises(ValueError):
                Bip38Decrypter.DecryptNoEc(test, "")

    # Tests invalid keys for encrypting
    def test_enc_invalid_keys(self):
        self.assertRaises(TypeError, Bip38Encrypter.EncryptNoEc, TEST_ED25519_PRIV_KEY, "")
        self.assertRaises(TypeError, Bip38Encrypter.EncryptNoEc, TEST_ED25519_BLAKE2B_PRIV_KEY, "")
        self.assertRaises(TypeError, Bip38Encrypter.EncryptNoEc, TEST_ED25519_MONERO_PRIV_KEY, "")
        self.assertRaises(TypeError, Bip38Encrypter.EncryptNoEc, TEST_NIST256P1_PRIV_KEY, "")
        self.assertRaises(TypeError, Bip38Encrypter.EncryptNoEc, TEST_SR25519_PRIV_KEY, "")

        for test in TEST_VECT_SECP256K1_PRIV_KEY_INVALID:
            self.assertRaises(ValueError, Bip38Encrypter.EncryptNoEc, binascii.unhexlify(test), b"\x00")
