import base64
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

# Security constants
SALT_SIZE = 16
NONCE_SIZE = 16
MAC_SIZE = 16
KEY_SIZE = 32  # 256-bit key for AES-256
PBKDF2_ITERATIONS = 1000_000

class Encryptor:
    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """
        Derives a cryptographic 256-bit key from a given password and salt using PBKDF2.
        """
        key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=PBKDF2_ITERATIONS)
        return key

    @staticmethod
    def encrypt_data(password: str, plaintext: bytes) -> bytes:
        """
        Encrypts plaintext bytes using AES-256 GCM.
        Returns the encrypted payload format: [SALT][NONCE][TAG][CIPHERTEXT]
        """
        # Generate random salt and derive key
        salt = get_random_bytes(SALT_SIZE)
        key = Encryptor.derive_key(password, salt)

        # Create AES GCM cipher
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce

        # Encrypt the data
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        # Construct final payload
        payload = salt + nonce + tag + ciphertext
        return payload

    @staticmethod
    def decrypt_data(password: str, encrypted_payload: bytes) -> bytes:
        """
        Decrypts an AES-256 GCM encrypted payload.
        Expects payload format: [SALT][NONCE][TAG][CIPHERTEXT]
        """
        try:
            # Extract components from the payload
            salt = encrypted_payload[:SALT_SIZE]
            nonce = encrypted_payload[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
            tag = encrypted_payload[SALT_SIZE + NONCE_SIZE:SALT_SIZE + NONCE_SIZE + MAC_SIZE]
            ciphertext = encrypted_payload[SALT_SIZE + NONCE_SIZE + MAC_SIZE:]

            # Derive key from password and extracted salt
            key = Encryptor.derive_key(password, salt)

            # Create AES GCM cipher for decryption
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

            # Decrypt and verify the data
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext
        except (ValueError, KeyError) as e:
            raise ValueError("Decryption failed. Incorrect password or corrupted data.") from e
