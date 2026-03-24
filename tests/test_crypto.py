import unittest
from src.encryptor import Encryptor

class TestEncryptor(unittest.TestCase):
    def setUp(self):
        self.password = "secure_password_123"
        self.data = b"This is a secret message."

    def test_encryption_decryption(self):
        # Encrypt the data
        encrypted_payload = Encryptor.encrypt_data(self.password, self.data)
        
        # Ensure ciphertext is different from plaintext
        self.assertNotEqual(encrypted_payload, self.data)
        
        # Decrypt the data
        decrypted_data = Encryptor.decrypt_data(self.password, encrypted_payload)
        
        # Ensure decrypted data matches original
        self.assertEqual(self.data, decrypted_data)

    def test_incorrect_password(self):
        encrypted_payload = Encryptor.encrypt_data(self.password, self.data)
        
        with self.assertRaises(ValueError):
            Encryptor.decrypt_data("wrong_password", encrypted_payload)

    def test_corrupted_data(self):
        encrypted_payload = bytearray(Encryptor.encrypt_data(self.password, self.data))
        
        # Corrupt one byte of the ciphertext
        encrypted_payload[-1] ^= 0xFF
        
        with self.assertRaises(ValueError):
            Encryptor.decrypt_data(self.password, bytes(encrypted_payload))

if __name__ == '__main__':
    unittest.main()
