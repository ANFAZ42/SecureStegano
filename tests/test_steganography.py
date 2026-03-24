import unittest
import os
import cv2
import numpy as np
from src.steganography import SteganographyEngine

class TestSteganography(unittest.TestCase):
    def setUp(self):
        self.password = "secure_password_123"
        self.message = "This is a secret message hidden in an image!"
        self.image_path = "tests/test_image.png"
        self.output_path = "tests/test_stego_image.png"
        
        # Create a dummy image for testing
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:] = 128 # gray image
        cv2.imwrite(self.image_path, img)

    def tearDown(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_encode_decode(self):
        # Encode
        success = SteganographyEngine.encode(self.image_path, self.password, self.message, self.output_path)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.output_path))
        
        # Decode
        decoded_message = SteganographyEngine.decode(self.output_path, self.password)
        self.assertEqual(self.message, decoded_message)
        
    def test_wrong_password(self):
        SteganographyEngine.encode(self.image_path, self.password, self.message, self.output_path)
        
        with self.assertRaises(ValueError):
            SteganographyEngine.decode(self.output_path, "wrong_password")

if __name__ == '__main__':
    unittest.main()
