import cv2
import numpy as np
import zlib
import struct
import random
import hashlib
from src.encryptor import Encryptor

class SteganographyEngine:
    @staticmethod
    def _create_prng(password: str, num_pixels: int):
        """
        Creates a reproducible sequence of pixel indices based on the password.
        Uses a seeded PRNG to scatter the bits uniformly.
        """
        # Hash the password to create a stable integer seed
        seed_hash = hashlib.sha256(password.encode()).hexdigest()
        seed = int(seed_hash, 16) % (2**32)
        
        # Use a local random instance so we don't affect global state
        rng = random.Random(seed)
        
        # Generate sequence of indices
        indices = list(range(num_pixels))
        rng.shuffle(indices)
        return indices

    @staticmethod
    def encode(image_path: str, password: str, message: str, output_path: str):
        """
        Encodes a secret message into an image.
        Pipeline: Compress -> Encrypt -> Prefix Length -> LSB Embed
        """
        # 1. Read Image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image at {image_path}")
            
        height, width, channels = img.shape
        max_bytes = (height * width * channels) // 8
        
        # 2. Prepare payload
        plaintext = message.encode('utf-8')
        compressed_data = zlib.compress(plaintext)
        encrypted_payload = Encryptor.encrypt_data(password, compressed_data)
        
        # Structure: 4 bytes length (unsigned int) + encrypted_payload
        payload_length = len(encrypted_payload)
        final_payload = struct.pack('>I', payload_length) + encrypted_payload
        
        if len(final_payload) > max_bytes:
            raise ValueError(f"Message too large. Max capacity: {max_bytes} bytes, Payload: {len(final_payload)} bytes.")
            
        # 3. Convert payload to bits
        bits = ''.join(format(byte, '08b') for byte in final_payload)
        
        # 4. Get random pixel sequence
        flat_img = img.flatten()
        indices = SteganographyEngine._create_prng(password, len(flat_img))
        
        # 5. Embed bits into LSB
        for i, bit in enumerate(bits):
            idx = indices[i]
            # Clear the LSB and set to the bit
            flat_img[idx] = (flat_img[idx] & 254) | int(bit)
            
        # 6. Reconstruct image and save
        stego_img = flat_img.reshape((height, width, channels))
        # Ensure it's saved as PNG to prevent lossy compression
        cv2.imwrite(output_path, stego_img)
        return True

    @staticmethod
    def decode(image_path: str, password: str) -> str:
        """
        Decodes a secret message from a stego-image.
        Pipeline: LSB Extract -> Read Length -> Read Payload -> Decrypt -> Decompress
        """
        # 1. Read Image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read stego-image at {image_path}")
            
        flat_img = img.flatten()
        indices = SteganographyEngine._create_prng(password, len(flat_img))
        
        # 2. Extract first 32 bits to get payload length
        length_bits = ''
        for i in range(32):
            idx = indices[i]
            length_bits += str(flat_img[idx] & 1)
            
        payload_length = int(length_bits, 2)
        
        # Sanity check on length
        if payload_length > len(flat_img) // 8 or payload_length <= 0:
            raise ValueError("Corrupted image or incorrect password (length extraction failed).")
            
        # 3. Extract payload bits
        payload_bits = ''
        total_bits_to_read = 32 + (payload_length * 8)
        
        if total_bits_to_read > len(flat_img):
            raise ValueError("Payload length exceeds image capacity.")
            
        for i in range(32, total_bits_to_read):
            idx = indices[i]
            payload_bits += str(flat_img[idx] & 1)
            
        # Convert bits to bytes
        payload_bytes = bytearray()
        for i in range(0, len(payload_bits), 8):
            byte = int(payload_bits[i:i+8], 2)
            payload_bytes.append(byte)
            
        # 4. Decrypt and decompress
        try:
            decrypted_compressed_data = Encryptor.decrypt_data(password, bytes(payload_bytes))
            plaintext = zlib.decompress(decrypted_compressed_data)
            return plaintext.decode('utf-8')
        except Exception as e:
            raise ValueError("Failed to extract data. Wrong password or corrupted image.") from e
