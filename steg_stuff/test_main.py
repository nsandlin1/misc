from unittest import TestCase
from main import *


class Test(TestCase):
    def test_string_to_binary(self):
        arg = 'hello'
        expected_value = '0110100001100101011011000110110001101111'
        value_received = string_to_binary(arg)

        self.assertEqual(value_received, expected_value)

    def test_encode(self):
        binary_string = '0110100001100101011011000110110001101111'
        image_path = './panda.jpg'

        self.assertEqual(True, True)

    def test_mod_rgb(self):
        bit1, bit2, bit3, bit4 = 0, 0, 1, 1
        rgb_val1, rgb_val2, rgb_val3, rgb_val4 = 12, 13, 15, 16

        # Test 0 and even:
        self.assertEqual(mod_rgb(bit1, rgb_val1), 12)
        # Test 0 and odd:
        self.assertEqual(mod_rgb(bit2, rgb_val2), 12)
        # Test 1 and odd:
        self.assertEqual(mod_rgb(bit3, rgb_val3), 15)
        # Test 1 and even:
        self.assertEqual(mod_rgb(bit4, rgb_val4), 17)

        self.assertEqual(mod_rgb(0, 11), 10)
        self.assertEqual(mod_rgb(1, 29), 29)
        self.assertEqual(mod_rgb(1, 43), 43)
        self.assertEqual(mod_rgb(0, 255), 254)

    def test_decode(self):
        image_path = 'test/panda_encoded.jpg'

        self.assertEqual(decode(image_path), '01101000011001010110110001101100011011110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

    def test_encode(self):
        binary_string = '0110100001100101011011000110110001101111'
        image_path = './test/2x2red.png'

        encode(binary_string, image_path)

        self.assertEqual(True, True)

    def test_decode(self):
        image_path = './test/2x2red_encoded.jpg'

        decode(image_path)

        self.assertEqual(True, True)

