import cv2
import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.steganography import SteganographyEngine
from src.analysis import detect_steganography_lsb

# 1. Create a dummy test image
os.makedirs('data/temp', exist_ok=True)
clean_img_path = 'data/temp/test_clean.png'
stego_img_path = 'data/temp/test_stego.png'

# Create a random image
print("Creating a test image...")
img = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
cv2.imwrite(clean_img_path, img)

# 2. Analyze clean image
print("Analyzing clean image...")
prob_clean = detect_steganography_lsb(clean_img_path)
print(f"Clean image LSB probability: {prob_clean * 100:.2f}%")

# 3. Encode a large message to see progress and create stego image
print("\nEncoding message...")
message = "A" * 10000  # Large payload
def my_progress(pct):
    print(f"Encode Progress: {pct}%")
    
SteganographyEngine.encode(clean_img_path, "password123", message, stego_img_path, progress_callback=my_progress)

# 4. Analyze stego image
print("\nAnalyzing stego image...")
prob_stego = detect_steganography_lsb(stego_img_path)
print(f"Stego image LSB probability: {prob_stego * 100:.2f}%")

# 5. Decode
print("\nDecoding message...")
def my_decode_progress(pct):
    print(f"Decode Progress: {pct}%")

decoded = SteganographyEngine.decode(stego_img_path, "password123", progress_callback=my_decode_progress)
if decoded == message:
    print("\nDecode successful! Message matches.")
else:
    print("\nDecode failed.")
