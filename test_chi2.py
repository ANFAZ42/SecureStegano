import cv2
import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.steganography import SteganographyEngine
from src.analysis import detect_steganography_lsb

# Let's create a natural-looking image (gradient) instead of pure noise
img = np.zeros((500, 500, 3), dtype=np.uint8)
for i in range(500):
    for j in range(500):
        img[i, j] = [i % 256, j % 256, (i+j) % 256]

os.makedirs('data/temp', exist_ok=True)
clean_path = 'data/temp/grad_clean.png'
stego_small_path = 'data/temp/grad_small.png'
stego_large_path = 'data/temp/grad_large.png'

cv2.imwrite(clean_path, img)

print("Clean Image Prob:", detect_steganography_lsb(clean_path))

SteganographyEngine.encode(clean_path, "pass", "Hello world!", stego_small_path)
print("Small Payload Prob:", detect_steganography_lsb(stego_small_path))

large_message = "A" * 200000  # 200,000 bytes
try:
    SteganographyEngine.encode(clean_path, "pass", large_message, stego_large_path)
    print("Large Payload Prob:", detect_steganography_lsb(stego_large_path))
except Exception as e:
    print("Error encoding large payload:", e)
